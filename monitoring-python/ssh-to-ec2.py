import paramiko 
import os

docker_image = os.environ["DOCKER_IMAGE"]
host_ip = os.environ["HOST_IP"]
ssh_path_key_file= os.environ["SSH_PATH_KEY_FILE"]
ecr_password = os.environ["ECR_PASSWORD"]
 
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

private_key = paramiko.RSAKey.from_private_key_file(ssh_path_key_file)

ssh.connect(hostname=host_ip, username="ubuntu", pkey=private_key)

stdin, stdout, stderr = ssh.exec_command(f"echo {ecr_password} |docker login --username AWS --password-stdin 660753258283.dkr.ecr.us-west-1.amazonaws.com")
print(stdout.readlines())

stdin, stdout, stderr = ssh.exec_command("docker run -p 8080:8080 -d ${docker_image}")
print(stdout.readlines())

ssh.close()