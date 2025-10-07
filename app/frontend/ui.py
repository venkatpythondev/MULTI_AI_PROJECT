import streamlit as st
import requests

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="MULTI-AI AGENT", layout="centered",page_icon=":robot_face:")
st.title("MULTI-AI AGENT using Groq and Tavily")

system_prompt=st.text_area("Define your Agent", height=100)
selected_model=st.selectbox("Select AI Model", settings.ALLOWED_MODELS)

allow_web_search=st.checkbox("Allow Web Search")
user_query=st.text_area("Enter your message", height=150)

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent"):
    payload = {
        "model_name" : selected_model,
        "system_prompt" : system_prompt,
        "messages" : [user_query],
        "allow_search" : allow_web_search
    }
    try:
        logger.info("Sending request to backend API")
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            agent_response = response.json().get("response","")
            logger.info("Sucesfully Received response from backend API")

            st.subheader("Agent Response:")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)
        else:
            logger.error(f"Error from backend API")
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        
        st.error(str(CustomException("Failed to get response from the AI agent.")))