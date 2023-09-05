# Correct err-disable on cisco switch
Ports on the switch connected to unifi ap's tend to err very frequently. Even with `power inline never` set on the port, err-disable occurs, very frequent.

Applying Paramiko to ssh to the switch, shutdown the port then re-activate it tends to repair the issue

```
int f3/0/{port}",

"shutd",

"no shutd",

"end"

```
Important to note that the commands need to escaped with a new line character.

After specifying the ports in a list, the ports are checked one by one, a port that returns the status as `err-disable` undergoes the above the commands to repair.
This worked like magic as looping the checks for minutes, ports that kept 'erring' disconnecting the ap's to an offline state, stopped to do so.

```
# Replace these values with your switch details

hostname = ""

username = ""

password = ""

```
then specify ports connected to the unifi ap's

Adjust sleep duration!

```
ports1 = [4,14,25,31]

ports2 = [8,9]

```
Execute the python script which will run in a loop till termination.
