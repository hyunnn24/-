import streamlit as st
import openai
import requests

# GitHub 파일 URL
file_url = "https://raw.githubusercontent.com/hyunnn24/-/main/counter_pick.txt"

# GitHub에서 counterpick.txt 파일 읽기
def load_counterpick_data(file_url):
    response = requests.get(file_url)
    response.raise_for_status()  # 요청이 성공했는지 확인
    return response.text

# Streamlit UI
st.title('LoL Counter Pick Recommender')

api_key = st.text_input('Enter your OpenAI API key:', type='password')

enemy_champion1 = st.text_input('Enter the first enemy champion:')
enemy_champion2 = st.text_input('Enter the second enemy champion:')

if st.button('Get Counter Picks'):
    if api_key:
        openai.api_key = api_key

        # GitHub에서 파일 내용 읽기
        try:
            counter_pick_data = load_counterpick_data(file_url)
        except requests.exceptions.RequestException as e:
            st.error(f"Error loading counter pick data: {e}")
            st.stop()
        
        # 프롬프트 생성
        prompt = f"Given the following counter pick data:\n\n{counter_pick_data}\n\n"
        prompt += f"Suggest counter picks for the following enemy champions:\n1. {enemy_champion1}\n2. {enemy_champion2}"

        # OpenAI API 호출
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=prompt
                max_tokens=1000
            )

            # API 응답 출력
            st.write(f"Counter picks for {enemy_champion1} and {enemy_champion2}:")
            st.write(response.choices[0].message.content)
        except openai.error.OpenAIError as e:
            st.error(f"OpenAI API error: {e}")
    else:
        st.error('Please enter your OpenAI API key.')

