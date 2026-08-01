import boto3
import datetime
import json

def lambda_handler(event, context):
    sagemaker = boto3.client('sagemaker')
    
    # Parse the body from API Gateway request safely
    try:
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
    except Exception:
        body = {}
        
    # Extract parameters from API request, or use your defaults if not provided
    input_s3_path = body.get('s3_input_path', 's3://customer-data-pushkar-khairnar-108372347/griffin_model/')
    output_s3_path = body.get('s3_output_path', 's3://customer-data-pushkar-khairnar-108372347/output/')
    
    # Unique name for every run
    job_name = f"griffin-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
    
    sagemaker.create_training_job(
        TrainingJobName=job_name,
        AlgorithmSpecification={
            'TrainingImage': '763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-training:2.3-cpu-py311',
            'TrainingInputMode': 'File'
        },
        RoleArn='arn:aws:iam::506715795496:role/AmazonSageMaker-ExecutionRole',
        InputDataConfig=[{
            'ChannelName': 'training',
            'DataSource': {'S3DataSource': {
                'S3DataType': 'S3Prefix',
                'S3Uri': input_s3_path,
                'S3DataDistributionType': 'FullyReplicated'
            }}
        }],
        OutputDataConfig={'S3OutputPath': output_s3_path},
        ResourceConfig={
            'InstanceType': 'ml.m4.xlarge',
            'InstanceCount': 1,
            'VolumeSizeInGB': 30
        },
        StoppingCondition={'MaxRuntimeInSeconds': 3600},
        HyperParameters={
            "sagemaker_program": "train.py",
            "sagemaker_submit_directory": "s3://training-pk/code/sourcedir.tar.gz"
        }
    )
    
    # Return structure formatted for API Gateway response
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "status": "Training Initiated",
            "job_name": job_name,
            "input_path": input_s3_path,
            "output_path": output_s3_path
        })
    }