import os
import paramiko


def connect_ssh():
    host = os.getenv('RASPBERRY_PI_IP')
    username = os.getenv('PI_USERNAME')
    password = os.getenv('PI_PASSWORD')

    command = "./recordstream.sh"
    
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(host, username=username, password=password)
        _stdin, _stdout,_stderr = client.exec_command(command)
        print(_stdout.read().decode())
        client.close()
        del client, _stdin, _stdout, _stderr
    
    except Exception as e:
        print("error",str(e))

connect_ssh()