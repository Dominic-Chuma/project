
## LocalStack S3 Report Generator

This project compares JSON resources, generates a comparison report, and uploads the final result to an S3 bucket running in LocalStack.

### Requirements
- Docker
- Docker Compose
- AWS CLI

### How to Run
```bash
docker-compose up --build

NOTE: Please make sure that you download the project from the github link, navigate to the project, via commandline/shell/gitbash, etc, and have docker installed and running before the running the above code. If you have a localstack account, this should work (Put your localstack token next to LOCALSTACK_AUTH_TOKEN=YOUR-TOKEN)