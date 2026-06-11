import boto3
import datetime

def lambda_handler(event, context):
    sagemaker = boto3.client('sagemaker')
    # Unique name for every run
    job_name = f"cats-dogs-training-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
    
    sagemaker.create_training_job(
        TrainingJobName=job_name,
        AlgorithmSpecification={
            'TrainingImage': '763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-training:2.3-gpu-py311',
            'TrainingInputMode': 'File'
        },
        RoleArn='arn:aws:iam::506715795496:role/AmazonSageMaker-ExecutionRole',
        InputDataConfig=[{
            'ChannelName': 'training',
            'DataSource': {'S3DataSource': {
                'S3DataType': 'S3Prefix',
                'S3Uri': 's3://customer-data-pushkar-khairnar-108372347/training/',
                'S3DataDistributionType': 'FullyReplicated'
            }}
        }],
        OutputDataConfig={'S3OutputPath': 's3://customer-data-pushkar-khairnar-108372347/output/'},
        ResourceConfig={
            'InstanceType': 'ml.m5.large', # Changed from ml.g4dn.xlarge
            'InstanceCount': 1,
            'VolumeSizeInGB': 30
        },
        StoppingCondition={'MaxRuntimeInSeconds': 3600},
        # These keys are required to tell the container to use your train.py
        HyperParameters={
            "sagemaker_program": "train.py",
            "sagemaker_submit_directory": "s3://training-pk/code/sourcedir.tar.gz"
        }
    )
    return {"status": "Training Initiated", "job_name": job_name}