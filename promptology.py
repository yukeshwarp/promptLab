import streamlit as st
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv() 


client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("API_KEY"),
    api_version=os.getenv("API_VERSION"),
)

st.title("promptLab")

model = st.selectbox(options=["gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "o1"], label="Select a model")
system_prompt = st.text_input("Enter your System prompt here:")
user_prompt = st.text_area("Enter your User prompt here:")

st.markdown(system_prompt)
st.markdown(user_prompt)

bot_response = ""  # Initialize outside the button block

if st.button("Test prompt"):
    response_stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        stream=True,
    )

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        for chunk in response_stream:
            if chunk.choices:
                bot_response += chunk.choices[0].delta.content or ""
                response_placeholder.markdown(bot_response)

# Download button appears after generating response
if bot_response:
    st.download_button(
        label="Download response as .txt",
        data=bot_response,
        file_name="assistant_response.txt",
        mime="text/plain"
    )
