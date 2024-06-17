import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import time

st.title('LoL Counter Pick Recommender')

enemy_champion1 = st.text_input('Enter the first enemy champion:')
enemy_champion2 = st.text_input('Enter the second enemy champion:')

def run_and_wait(client, assistant, thread):
  run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
  )
  while True:
    run_check = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )
    print(run_check.status)
    if run_check.status in ['queued','in_progress']:
      time.sleep(2)
    else:
      break
  return run

api_key = st.text_input('Enter your OpenAI API key:', type='password')
client = OpenAI(api_key=api_key)

github_url = "https://github.com/hyunnn24/-/blob/main/counter_pick.txt"
url = github_url.replace("/blob/", "/raw/")

def download_and_save(url, filename):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  text = soup.get_text(separator=' ', strip=True)
  with open(filename,'w') as fo:
    fo.write(text)

filename = 'data.txt'

download_and_save(url, filename) 

with open(filename) as fi:
  text = fi.read()

#st.write(text) #TEST 

my_file = client.files.create(
    file = open(filename,'rb'),
    purpose='assistants'
)

assistant = client.beta.assistants.create(
  instructions="당신은 리그오브레전드 전문가 입니다 첨부파일의 정보를 이용해 카운터 챔피언을 알려주세요.",
  model="gpt-4o",
  tools=[{"type": "retrieval"}],
  file_ids=[my_file.id]
)
if enemy_champion1 and enemy_champion2 and api_key:
    query = f"{enemy_champion1}, {enemy_champion2}"

    thread = client.beta.threads.create(
    messages=[
        {
        "role": "user",
        "content": query,
        #"file_ids": [my_file.id]
        }
    ]
    )
    run_and_wait(client, assistant, thread)

    for msg in thread_messages.data:
        st.write(f"{msg.role}: {msg.content[0].text.value}")
