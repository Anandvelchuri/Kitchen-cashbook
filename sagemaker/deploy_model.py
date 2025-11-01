# deploy_model.py
# Script to deploy the trained model to SageMaker

import boto3
import sagemaker
from sagemaker.sklearn import SKLearnModel
import os

def deploy_model(model_path="model.pkl", role_arn=None, endpoint_name="fraud-detection-endpoint"):
    sagemaker_session = sagemaker.Session(boto3.Session(region_name="us-east-1"))
    if role_arn is None:
        # You should set your SageMaker execution role ARN here
        raise ValueError("role_arn must be provided.")
    model = SKLearnModel(
        model_data=sagemaker_session.upload_data(model_path),
        role=role_arn,
        entry_point=None,  # If you have a custom inference script, provide its path here
        framework_version="0.23-1"
    )
    predictor = model.deploy(
        initial_instance_count=1,
        instance_type="ml.m5.large",
        endpoint_name=endpoint_name
    )
    print(f"Model deployed to endpoint: {endpoint_name}")

if __name__ == "__main__":
    # Example usage: update role_arn with your SageMaker execution role ARN
    deploy_model(role_arn="arn:aws:iam::YOUR_ACCOUNT_ID:role/service-role/AmazonSageMaker-ExecutionRole-xxxxxxx")
