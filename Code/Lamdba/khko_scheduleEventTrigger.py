from json import load, dumps
import boto3


ec2_client = boto3.client("ec2")
rds_client = boto3.client("rds")


def lambda_handler(event, context):
    if event["resources"][0].split("_")[-1].startswith("i-"):
        ec2_target = event["resources"][0].split("_")[-1]
        ec2_client.start_instances(InstanceIds=[ec2_target])
        ec2_client.delete_tags(
            Resources=[ec2_target],
            Tags=[
                {
                    'Key': 'Schedule',
                },
            ]
        )
    else:
        rds_target = event["resources"][0].split("_")[-1]
        get_rds = rds_client.describe_db_instances(
            DBInstanceIdentifier=rds_target
        )["DBInstances"][0]
        rds_client.remove_tags_from_resource(
            ResourceName=get_rds["DBInstanceArn"],
            TagKeys=[
                'Schedule',
            ]
        )
