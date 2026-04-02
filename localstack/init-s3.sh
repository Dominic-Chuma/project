
#!/bin/bash
set -e

awslocal s3 mb s3://comparison-reports
echo "✅ S3 bucket created: comparison-reports"
