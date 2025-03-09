from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets['api_key'])

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a tutor assistant assisting students ages 8-10 on the spectrum of autism to practice their basic communication skills in English. Their native language is Greek and they learn English as a Foreign Language. Their English CEFR level is A1-A2. The subjects you will be discussing are the following: Colors, Food, Hobbies. Don't forget to ask questions back and keep the conversation flowing! You will present one subject at a time."},
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)