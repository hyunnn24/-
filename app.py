import streamlit as st
import openai
import requests

# GitHub 파일 URL
file_url = "https://raw.githubusercontent.com/hyunnn24/-/main/counter_pick.txt"

# GitHub에서 counterpick.txt 파일 읽기
def load_counterpick_data(file_url):
    response = requests.get(file_url)
    response.raise_for_status()  # 요청이 성공했는지 확인
    return response.text.split('\n')

# 간단한 문서 검색 함수
def search_documents(query, docs):
    return [doc for doc in docs if query.lower() in doc.lower()]

# OpenAI API 호출 함수
def call_openai_api(query, context, api_key):
    openai.api_key = api_key
    if context:
        messages = [
            {"role": "system", "content": "문서만보고 입력된 바텀 챔피언의 카운터알려줘 ."},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
        ]
    else:
        messages = [
            {"role": "system", "content": "문서만보고 입력된 바텀 챔피언의 카운터알려줘 ."},
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
            try:
                documents = load_counterpick_data(file_url)
            except requests.exceptions.RequestException as e:
                st.error(f"Error loading counter pick data: {e}")
                st.stop()

            query = f"{enemy_champion1}, {enemy_champion2}"
            relevant_docs = search_documents(query, documents)
            context = " ".join(relevant_docs)

        with st.spinner('OpenAI API 호출 중...'):
            # 텍스트 생성 단계
            try:
                answer = call_openai_api(query, context, api_key)
                st.write("Counter picks for the given champions:")
                st.write(answer)
            except Exception as e:
                st.error(f"오류 발생: {e}")
