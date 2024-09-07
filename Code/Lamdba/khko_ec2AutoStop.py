from json import loads, dumps
import boto3

# AWS 인터페이스
client = boto3.client("ec2")
resource = boto3.resource("ec2")

# Schedule 설정 대상 EC2 List
ec2_list = []

# AutoStop 대상 EC2 찾기
def autostop_ec2_find():
    for i in resource.instances.all():
        if "stopped" == i.state["Name"] and "DEV" in str(i.tags):
            for tag in i.tags:
                if tag["Key"] == "AutoStop" and tag["Value"].upper() == "Y":
                    ec2_list.append(i.id)

# Lambda Handler 통한 EC2 Start 수행
## Stop 테스트 영향도 생길것 우려하여 Start로 설정하였음
def lambda_handler(event, context):
  autostop_ec2_find()
  for target_ec2 in ec2_list:
      client.start_instances(InstanceIds=[target_ec2])