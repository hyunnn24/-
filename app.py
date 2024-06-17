import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

api_key = st.text_input('Enter your OpenAI API key:', type='password')
client = OpenAI(api_key=api_key)


def download_and_save(url, filename):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  text = soup.get_text(separator=' ', strip=True)
  with open(filename,'w') as fo:
    fo.write(text)

url = "https://github.com/hyunnn24/-/blob/main/counter_pick.txt"
filename = 'data.txt'

download_and_save(url, filename) 

with open(filename) as fi:
  text = fi.read()

st.write(text)