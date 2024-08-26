from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    aws_lambda as lambda_,
    
)
from constructs import Construct

class ServerlesspatternsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = dynamodb.Table(
            self,
            "serverless_workshop_intro",
            partition_key=dynamodb.Attribute(
                name="_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
            )
        
        lambda_function = lambda_.Function(
            self,
            "first_function",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset("lambda"),
        )
        
        batch_function = lambda_.Function(
            self,
            "m1-add-sample-data",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="m1-add-sample-data.lambda_handler",
            code=lambda_.Code.from_asset("lambda"),
            # environment
            environment={
                "TABLE_NAME": table.table_name
            }
        )
        
        table.grant_full_access(batch_function)
        