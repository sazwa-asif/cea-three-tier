# CEA: Three-tier web application on AWS with CI/CD

Nginx web tier, Flask application tier, PostgreSQL (RDS) database tier. Docker containers, CloudFormation infrastructure, GitHub Actions pipeline.

```
web/            Nginx Dockerfile, config template, static page
app/            Flask API, Dockerfile, tests
docker-compose.yml   run all three tiers locally
infra/cea-stack.yaml CloudFormation: VPC, subnets, gateways, security groups, ALBs, ASGs, RDS, ECR, secrets, IAM, monitoring
.github/workflows/deploy.yml   test, build, push, deploy
docs/           architecture, NFR, cost, screenshot checklist
```

## Run locally
```bash
cp .env.example .env
docker compose up --build
```
Open http://localhost:8080 (the page talks to the API through Nginx; the database is only on the private `backend` network).

## Deploy to AWS
1. One time: IAM > Identity providers > Add provider > OpenID Connect, URL `https://token.actions.githubusercontent.com`, audience `sts.amazonaws.com`.
2. CloudFormation > Create stack with `infra/cea-stack.yaml`; set `GitHubRepo` to `owner/repo`; tick the IAM acknowledgement.
3. When complete, copy output `GitHubDeployRoleArn` into GitHub > Settings > Secrets and variables > Actions > secret `AWS_ROLE_ARN`.
4. Push to `main` (or run the workflow manually). The first run pushes the images; instances retry until the images exist, then the site opens at the `SiteUrl` output.
5. After screenshots: delete the CloudFormation stack to stop charges.
