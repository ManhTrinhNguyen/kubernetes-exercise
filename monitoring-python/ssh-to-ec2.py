import paramiko 

commands = [
" "
]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

private_key = paramiko.RSAKey.from_private_key_file('/var/jenkins_home/terraform.pem')

ssh.connect(hostname="154.177.245.131", username="ubuntu", pkey=private_key)

stdin, stdout, stderr = ssh.exec_command("aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 660753258283.dkr.ecr.us-west-1.amazonaws.com")

print(stdout.readlines())

ssh.close()