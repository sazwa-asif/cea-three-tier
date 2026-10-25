# Screenshot checklist (brief section 4)

Take each after the stack is running, then delete the stack.

| # | Screenshot | Where |
|---|---|---|
| 1 | VPC, subnets (6), route tables, internet gateway, NAT gateway | VPC console: Your VPCs, Subnets, Route tables, NAT gateways |
| 2 | Running EC2 instances (web and app, tagged by tier) | EC2 > Instances |
| 3 | Security groups for each tier with inbound rules | EC2 > Security Groups (cea-web-alb-sg, cea-web-sg, cea-app-alb-sg, cea-app-sg, cea-db-sg) |
| 4 | Load balancers and target groups (healthy targets) | EC2 > Load Balancers, Target Groups |
| 5 | RDS database, "Publicly accessible: No" | RDS > Databases > cea stack database |
| 6 | Docker build output | Local terminal: `docker compose build` |
| 7 | Registry listing with both images | ECR > cea-web, cea-app (tags: sha + latest) |
| 8 | Successful CI/CD run | GitHub > Actions > green run with all steps expanded |
| 9 | Running application in the browser | Open the `SiteUrl` output; add a note; show the page |

Extra (enhancement evidence): CloudWatch dashboard `cea-three-tier`, alarms, Auto Scaling group with policy, Secrets Manager secret (value hidden), CloudFormation stack Resources tab, local app at http://localhost:8080.
