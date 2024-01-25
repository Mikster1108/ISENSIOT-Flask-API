import os
import paramiko

attempting_connect = False


# Returns True if camera is recording
# Returns False if it failed to start recording
# Returns None if its in the process of starting the recording
def connect_ssh():
    global attempting_connect
    if attempting_connect:
        return
    attempting_connect = True

    host = os.getenv('RASPBERRY_PI_IP')
    username = os.getenv('PI_USERNAME')
    password = os.getenv('PI_PASSWORD')

    command = "./recordstream.sh"
    
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(host, username=username, password=password)
        _stdin, _stdout,_stderr = client.exec_command(command)
        if _stderr:
            client.close()
            return False
        print(_stdout.read().decode())
        client.close()

        del client, _stdin, _stdout, _stderr
        return True
    except Exception as e:
        return False
    finally:
        attempting_connect = False
