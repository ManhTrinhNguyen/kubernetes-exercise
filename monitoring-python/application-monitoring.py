import boto3, time
import schedule
import requests, paramiko

## SSH Private Key 

private_key = paramiko.RSAKey.from_private_key_file('/Users/trinhnguyen/.ssh/terraform.pem')

## Create SG and Open port 8080, 22

def create_sg():
  ec2_client = boto3.client('ec2')

  describe_sg = ec2_client.describe_security_groups(
    Filters=[
      {
        'Name': 'tag:Name',
        'Values': [
          'nginx-security-group'
        ]
      }
    ]
  )

  sg_already_exist = len(describe_sg['SecurityGroups']) != 0

  if sg_already_exist:
    print("SG_Already exist")
    return describe_sg['SecurityGroups'][0]["GroupId"]
  else:  
    create_sg = ec2_client.create_security_group(
      Description = "Security Group for Nginx Server",
      GroupName = "nginx-security-group",
      TagSpecifications=[
        {
          'ResourceType': 'security-group',
          'Tags': [
            {
              'Key': 'Name',
              'Value': 'nginx-security-group'
            }
          ]
        }
      ]
    )

    sg_id = create_sg['GroupId']

    print(f"Success created SG: {sg_id}")

    ## Open port 
    ingress = ec2_client.authorize_security_group_ingress(
      GroupId = sg_id,
      IpPermissions=[
        {
          'IpProtocol': 'TCP',
          'FromPort': 22,
          'ToPort': 22,
          'IpRanges': [
            {
              'Description': 'Allow SSH to anyone',
              'CidrIp': '0.0.0.0/0'
            }
          ]
        },
        {
          'IpProtocol': 'TCP',
          'FromPort': 8080,
          'ToPort': 8080,
          'IpRanges': [
            {
              'Description': 'Allow access to Nginx server',
              'CidrIp': '0.0.0.0/0'
            }
          ]
        },
      ]
    )
    
    if ingress["Return"]:
      print(f"Success opened Port 22 and 8080")
    else: 
      print("Failed to open port")

    return sg_id  

## Get Instance Public key 

def instance_public_ip():
  ec2_client = boto3.client('ec2')

  response = ec2_client.describe_instances(
    Filters=[
      {
        'Name': 'tag:Name',
        'Values': ['testInstance5']
      }
    ]
  )

  return (response["Reservations"][0]["Instances"][0]['PublicIpAddress'])

## Install Docker and Run nginx 

def install_docker_and_run_nginx():

  install_docker_and_run_nginx_command = [
  "sudo apt-get update -y",
  "sudo apt-get install ca-certificates curl",
  "sudo install -m 0755 -d /etc/apt/keyrings",
  "sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc",
  "sudo chmod a+r /etc/apt/keyrings/docker.asc",
  'echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null',
  "sudo apt-get update -y",

  "sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y",

  "sudo usermod -aG docker ubuntu"
  ]


  try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 

    
    ssh.connect(hostname=instance_public_ip(), username='ubuntu', pkey=private_key)

    for command in install_docker_and_run_nginx_command:

      stdin, stdout, stderr = ssh.exec_command(command)

      print(stdout.readlines())

    ssh.close()
  except Exception as e:
    print(f"Failed to install Docker {e}")

  ## Exit and back in to run nginx

  time.sleep(3)

  try:
    ssh.connect(hostname=instance_public_ip(), username='ubuntu', pkey=private_key)

    stdin, stdout, stderr = ssh.exec_command('docker run -d -p 8080:80 --name nginx nginx')

    print(stdout.readlines())

    ssh.close()
  except Exception as e:
    print(f"Falied to run Nginx {e}")
  


## Start EC2 instance in default VPC

def start_ec2_instance():

  ec2_client = boto3.client('ec2')

  describe_instance = ec2_client.describe_instances(
    Filters=[
      {
        'Name': 'tag:Name',
        'Values': ['testInstance5']
      }
    ]
  )

  instance_already_exist = len(describe_instance["Reservations"]) != 0 and len(describe_instance["Reservations"][0]["Instances"]) != 0

  if not instance_already_exist:
    create_ec2_instance = ec2_client.run_instances(
        ImageId="ami-00271c85bf8a52b84",
        InstanceType="t2.medium",
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds = [create_sg()],
        KeyName="terraform",
        TagSpecifications=[
          {
            'ResourceType': "instance",
            'Tags': [
              {"Key": "Name", "Value": "testInstance5"}
            ]
          }
        ]
    )

    instance_ID = (create_ec2_instance["Instances"][0]["InstanceId"])

    print(f"This is InstanceID: {instance_ID}")

    ## Wait until the EC2 server is fully initialized

    print("Wait for 120s")
    time.sleep(120)

    is_instance_ready = False 

    while is_instance_ready == False:

      describe_instance_status = ec2_client.describe_instance_status(
        InstanceIds = [instance_ID]
      )["InstanceStatuses"][0]
      
      instance_state = describe_instance_status["InstanceState"]["Name"]

      instance_status = describe_instance_status["InstanceStatus"]["Status"]

      if instance_state == "running" and instance_status == "ok":
        is_instance_ready = True
        print("Instance is ready to use")

      print(f"State: {instance_state} | Status: {instance_status}")

      ## Install Docker and Run Nginx 
      install_docker_and_run_nginx()
  else: 
    print("Instance already exist")

start_ec2_instance()


# Scheduled function to check nginx application status and reload if not OK 5x in a row

application_not_accessible_count = 0

def restart_nginx():
  global application_not_accessible_count

  try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=instance_public_ip(), username='ubuntu', pkey=private_key)

    stdin, stdout, stderr = ssh.exec_command('docker start nginx')

    print(stdout.readlines())

    ssh.close()
    application_not_accessible_count = 0
    print(f"Counter reset to : {application_not_accessible_count}")

  except Exception as e:
    print(f'Failed to restart Nginx {e}')


## Create a scheduled function that sends a request to the nginx application and checks the status is OK

def check_nginx_status():
  global application_not_accessible_count

  try:
    request = requests.get(f"http://{instance_public_ip()}:8080/")
    status_code = request.status_code

    if status_code == 200:
      print("Nginx is running !!!!!")
    else:
      print("Application not running !!!")
      application_not_accessible_count += 1
      print(f'Counter failure: {application_not_accessible_count}')
      if application_not_accessible_count == 5:
        print("Restarting Nginx")
        restart_nginx()

  except Exception as e:
    print(f"Connection error{e}")
    print("Application not accessible at all")
    application_not_accessible_count += 1
    print(f'Counter failure: {application_not_accessible_count}')
    if application_not_accessible_count == 5:
      print("Restarting Nginx")
      restart_nginx()


schedule.every(10).seconds.do(check_nginx_status)

while True:
  schedule.run_pending()












