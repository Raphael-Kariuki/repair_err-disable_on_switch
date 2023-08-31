import paramiko
import time

ssh_client = paramiko.SSHClient()

'''
It's important to note that using AutoAddPolicy() can be risky in untrusted environments 
because it removes the protection that host key verification provides against man-in-the-middle attacks.
 In production or security-sensitive scenarios, 
 it's recommended to use policies that provide stronger security, 
 such as paramiko.RejectPolicy(), which rejects connections to servers with unknown host keys.

In summary, ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) sets the SSH client's behavior to automatically add missing host keys to the known hosts file, 
effectively skipping host key verification for those keys. This can be convenient in certain situations but should be used with caution, especially in untrusted environments.
'''
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())



def send_config(hostname, username, password, config_commands):
    

    try:
        ssh_client.connect(hostname, username=username, password=password)
        
        # Start an interactive shell session
        ssh_shell = ssh_client.invoke_shell()

        # Wait a bit for the shell to initialize
        time.sleep(1)

        # Send "conf t" command - Must be followed by a new line 
        ssh_shell.send("conf t\n")
        time.sleep(1)

        # Send configuration commands
        for cmd in config_commands:
            print(f"Executing {cmd}" )
        # the response for a #.send is the number of ( bytes or bits ) sent -> not sure about the unit of measurement. To confirm
            result = ssh_shell.send(cmd + "\n")
            print(f"Result of {cmd} is {result}" )
            time.sleep(1)

        # Exit configuration mode
        ssh_shell.send("end\n")
        time.sleep(1)

        # Close the shell
        ssh_shell.close()

    except paramiko.AuthenticationException:
        print("Authentication failed")
    except paramiko.SSHException as e:
        print("SSH connection error:", str(e))
    except Exception as e:
        print("Error:", str(e))
    finally:
        ssh_client.close()



def check_state(hostname, username, password, port):
    # ssh_client = paramiko.SSHClient()
    # ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname, username=username, password=password)
    try:
        # Start an interactive shell session
        ssh_shell = ssh_client.invoke_shell()


#.exec_command threw the error - paramiko.ssh_exception.SSHException: Invalid packet blocking
#The 'paramiko.ssh_exception.SSHException: Invalid packet blocking' error in Paramiko typically occurs 
#when there is a problem with the SSH connection, specifically related to packet synchronization or timing issues.
#Solution provided is to use #.invoke_shell then  #.send and #.receive rather than #.exec_command
        stdin, stdout, stderr = ssh_client.exec_command('sh int f3/0/' + str(port) +' status' + "\n")
        string_to_check = 'err-disable'
        string_to_check2 = 'connected'
        string_to_check3= 'disabled'
        string_to_check4= 'notconnect'

        output = stdout.read().decode()
        error = stderr.read().decode()

        if output.find(string_to_check) != -1:
            print(f'Port {port}  err-disable')
            return 1
        elif output.find(string_to_check2) != -1:
            print(f'Port {port}  Connected')
            return 2
        elif output.find(string_to_check3) != -1:
            print(f'Port {port}  disable')
            return 3
        elif output.find(string_to_check4) != -1:
            print(f'Port {port} notconnect')
            return 4
        else:
            print(f'Command: {command}\nError:\n{error}')
            return 5

    except paramiko.AuthenticationException:
        print('Authentication failed. Please check your credentials.')
    except paramiko.SSHException as ssh_exception:
        print(f'SSH connection failed: {ssh_exception}')
    finally:
        ssh_client.close()

# Replace these values with your switch details
hostname = ""
username = ""
password = ""



ports1 = [4,14,25,31]
ports2 = [8,9]

def main():
    for port in ports1:
        #Checks if port is errored, shuts it down and brings it back up
        if check_state(hostname, username, password,port) == 1:
            # Configuration commands to be sent
            config_commands = [
                f"int f3/0/{port}",
                "shutd",
                "no shutd",
                "end"
            ]
            send_config(hostname,username,password,config_commands)


while True:
    main()
    time.sleep(1)