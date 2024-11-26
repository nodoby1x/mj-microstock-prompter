import streamlit as sl
from controller import PrompterGenerator
from dotenv import load_dotenv
import os
import time

def GeminiPage():
    sl.title("Use Gemini API Key")

    api_key = sl.text_input("API Key", type="password")


    if api_key:
        sl.session_state.gemini_api = api_key
        sl.info(f"got key: {api_key}")