import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup

def get_text_from_github(url):
    # GitHub raw 파일의 URL에서 접근
    raw_url = url.replace("/blob/", "/raw/")
    
    # requests를 사용하여 HTML 가져오기
    response = requests.get(raw_url)
    
    # HTTP 요청이 성공했는지 확인
    response.raise_for_status()
    
    # HTML 문서 파싱
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 텍스트 추출
    text = soup.get_text()
    
    return text

# 테스트용 GitHub URL
github_url = "https://github.com/hyunnn24/-/blob/main/counter_pick.txt"

try:
    # 텍스트 가져오기
    text = get_text_from_github(github_url)
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
# OpenAI API 호출 함수
def call_openai_api(query, context, api_key):
    openai.api_key = api_key
    if context:
        messages = [
            {"role": "system", "content": "입력된 바텀 챔피언의 카운터알려줘 ."},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
        ]
    else:
        messages = [
            {"role": "system", "content": "입력된 바텀 챔피언의 카운터알려줘 ."},
            {"role": "user", "content": f"Query: {query}"}
        ]
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1000
    )
    return response.choices[0].message.content

# Streamlit UI
st.title('LoL Counter Pick Recommender')

api_key = st.text_input('Enter your OpenAI API key:', type='password')

enemy_champion1 = st.text_input('Enter the first enemy champion:')
enemy_champion2 = st.text_input('Enter the second enemy champion:')

if st.button('Get Counter Picks'):
    if not api_key:
        st.error("API 키를 입력하세요.")
    elif not enemy_champion1 or not enemy_champion2:
        st.error("두 챔피언 이름을 모두 입력하세요.")
    else:
        with st.spinner('문서 검색 중...'):
            # 문서 로딩 및 검색 단계
            

            query = f"{enemy_champion1}, {enemy_champion2}"
            relevant_docs = text
            context = " ".join(relevant_docs)

        with st.spinner('OpenAI API 호출 중...'):
            # 텍스트 생성 단계
            try:
                answer = call_openai_api(query, context, api_key)
                st.write("Counter picks for the given champions:")
                st.write(answer)
            except Exception as e:
                st.error(f"오류 발생: {e}")
