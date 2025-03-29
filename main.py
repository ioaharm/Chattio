from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets['api_key'])

st.title("💬 Chattio")
st.caption("Chattio is your digital English speaking buddy.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Let's practice English together! ☺️"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if (prompt := st.chat_input()) is not None:  # Ensure user has entered input
    st.session_state.messages.append({"role": "user", "content": prompt})  # Save user input
    st.chat_message("user").write(prompt)  # Display user input

    if any(word in prompt.lower() for word in ["goodbye", "off"]):  
        st.write("Goodbye! Have a great day! 😊")
        st.stop()  # Stop execution AFTER displaying the user input

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Your name is Chattio and you are a tutor assisting students ages 8-10 on the spectrum of autism to practice their basic communication skills in English. Their native language is Greek, and they learn English as a Foreign Language (CEFR level A1-A2). If the student writes in Greek, **translate it to English before responding**. Always reply in **simple English**. The subjects you will be discussing are the following:Colors, Food, Hobbies. Your tone is enthusiastic, friendly, and playful. Your vocabulary level corresponds to the students’ English level. Avoid very long answers. Ask questions and keep the conversation flowing in English. If a question is irrelevant to the subjects above, respond: I don’t know about that."},
            {"role": "user", "content": prompt}
        ] + st.session_state.messages,
        stream=False,
        temperature=1,
        max_tokens=1024,
        top_p=0.95,
        frequency_penalty=0.2,
        presence_penalty=1.8,
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    
