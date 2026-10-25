# Cost estimate (us-east-1, approximate on-demand prices, 730 hours per month)

| Item | Quantity | Approx. per month |
|---|---|---|
| EC2 t3.small (web) | 2 | 2 x 15 = 30 |
| EC2 t3.small (app) | 2 | 2 x 15 = 30 |
| RDS db.t4g.micro + 20 GB gp3 | 1 | 13 + 2 = 15 |
| Application Load Balancers | 2 | 2 x 17 = 34 |
| NAT Gateway (fixed part) | 1 | 33 |
| Secrets Manager | 1 secret | 0.4 |
| ECR, CloudWatch logs, dashboard | small | 4 |
| **Total if left running a full month** | | **about 145** |

Run only for the demo (about 4 hours), the cost is about **$1** (about $0.20 per hour).

## Optimization 1: right-size and scale in when idle
Keep 1 instance per tier at night (set desired capacity to 1) and use `t3.micro` for the app tier: saves about 35 per month. Use Savings Plans or Reserved Instances for the steady base load (up to about 40% less).

## Optimization 2: remove the largest fixed costs
Replace the NAT gateway (33) with VPC endpoints for ECR, S3 and Secrets Manager (about 15-20 for the interface endpoints) or share one internal ALB; and use a single ALB with path rules instead of two (saves about 17). Also stop the RDS instance outside working hours.

## Controls used in this project
Stack deleted right after the screenshots; budget alert enabled; 3-day log retention; no Multi-AZ database.
