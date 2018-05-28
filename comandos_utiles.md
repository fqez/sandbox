# SSH

## · ssh session timeout increase

```/etc/ssh_config``` is the client side configuration file not the server side config file.

To prevent all your clients from timing out you need to edit /etc/sshd_config which is the server side configuration file add these two options:
```
ClientAliveInterval 120
ClientAliveCountMax 720
````
The first one configures the server to send null packets to clients each 120 seconds and the second one configures the server to close the connection if the client has been inactive for 720 intervals that is ```720*120 = 86400 seconds = 24 hours```
