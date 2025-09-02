import paramiko 

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

private_key = paramiko.RSAKey.from_private_key_file('/var/jenkins_home/terraform.pem')

ssh.connect(hostname="13.57.49.64", username="ubuntu", pkey=private_key)

stdin, stdout, stderr = ssh.exec_command("ls")

print(stdout.readlines())

ssh.close()