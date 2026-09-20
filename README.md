# SageMaker Image Classification Training Infrastructure

A fully automated CI/CD pipeline and CloudFormation infrastructure for launching SageMaker image classification training jobs dynamically via a single HTTP API Gateway endpoint.

---

## Repository Structure

Ensure your repository is structured as follows before pushing:

    your-repo/
    ├── .github/
    │   └── workflows/
    │       └── deploy.yml          # GitHub Actions CI/CD pipeline
    ├── aws/
    │   └── template_2.yaml         # CloudFormation infrastructure template
    └── src/
        └── aws_model_training/
            └── train.py            # Image classification script

---

## Step 1: Configure GitHub Secrets

Go to your GitHub repository **Settings > Secrets and variables > Actions** and add the following secrets:

* AWS_ACCESS_KEY_ID: Your AWS access key.
* AWS_SECRET_ACCESS_KEY: Your AWS secret key.

---

## Step 2: Configure Your Data Bucket in CI/CD

In your `.github/workflows/deploy.yml` file, find the CloudFormation `parameter-overrides` section. You must update **`DataS3BucketName`** to match your own unique S3 bucket where your training data is stored:

    parameter-overrides: |
      DataS3BucketName=YOUR-UNIQUE-DATA-BUCKET-NAME,
      TrainingCodeBucketName=training-pk,
      TrainingImageUri=763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-training:2.3-gpu-py311

*Why this matters:* The CloudFormation template uses this parameter to grant your SageMaker execution role read/write permissions to your data bucket, and uses it inside the Lambda function to set default input and output paths.

---

## Step 3: Deploying via CI/CD

When you push your code to the `main` branch, the GitHub Actions workflow (`deploy.yml`) will automatically:
1. Authenticate with AWS.
2. Ensure your training code S3 bucket (`training-pk`) exists.
3. Bundle your training script into `sourcedir.tar.gz` and upload it to S3.
4. Deploy/update the CloudFormation stack (`training-infrastructure-stack-7`).

---

## Step 4: Triggering Training Jobs via API