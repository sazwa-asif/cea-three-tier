import json
import os
import socket

from flask import Flask, jsonify, request

app = Flask(__name__)
_creds = None
_table_ready = False


def credentials():
    """DB user/password: from AWS Secrets Manager when DB_SECRET_ARN is set, else from env (local dev)."""
    global _creds
    if _creds is None:
        arn = os.environ.get("DB_SECRET_ARN")
        if arn:
            import boto3

            sm = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1"))
            secret = json.loads(sm.get_secret_value(SecretId=arn)["SecretString"])
            _creds = (secret["username"], secret["password"])
        else:
            _creds = (os.environ["DB_USER"], os.environ["DB_PASSWORD"])
    return _creds


def connect():
    import psycopg2

    user, password = credentials()
    return psycopg2.connect(
        host=os.environ["DB_HOST"], port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "ceadb"), user=user, password=password, connect_timeout=5)


def ensure_table():
    global _table_ready
    if not _table_ready:
        conn = connect()
        try:
            with conn, conn.cursor() as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS notes ("
                            "id SERIAL PRIMARY KEY, text TEXT NOT NULL, "
                            "created_at TIMESTAMPTZ DEFAULT now(), served_by TEXT)")
        finally:
            conn.close()
        _table_ready = True


@app.get("/health")
def health():
    return jsonify(status="ok", tier="app", host=socket.gethostname())


@app.get("/api/info")
def info():
    return jsonify(tier="app", host=socket.gethostname())


@app.get("/api/ready")
def ready():
    try:
        ensure_table()
        return jsonify(status="ready", database="reachable")
    except Exception as exc:  # noqa: BLE001
        return jsonify(status="not ready", error=type(exc).__name__), 503


@app.get("/api/notes")
def list_notes():
    ensure_table()
    conn = connect()
    try:
        with conn, conn.cursor() as cur:
            cur.execute("SELECT id, text, created_at, served_by FROM notes ORDER BY id DESC LIMIT 20")
            rows = cur.fetchall()
    finally:
        conn.close()
    return jsonify([{"id": r[0], "text": r[1], "created_at": r[2].isoformat(), "served_by": r[3]} for r in rows])


@app.post("/api/notes")
def add_note():
    text = ((request.get_json(silent=True) or {}).get("text") or "").strip()
    if not text or len(text) > 500:
        return jsonify(error="text must be 1-500 characters"), 400
    ensure_table()
    conn = connect()
    try:
        with conn, conn.cursor() as cur:
            cur.execute("INSERT INTO notes (text, served_by) VALUES (%s, %s) RETURNING id",
                        (text, socket.gethostname()))
            note_id = cur.fetchone()[0]
    finally:
        conn.close()
    return jsonify(id=note_id, served_by=socket.gethostname()), 201
