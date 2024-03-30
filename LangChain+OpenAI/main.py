import os
from const import openai_Key
from langchain_community.llms import OpenAI
from langchain.llms import OpenAI

import streamlit as st

os.environ["OPENAI_API_KEY"] = openai_Key

st.title("LangChain + OpenAI")
input_text = st.text_input("Search something")

llm = OpenAI(temperature=0.8)

if input_text:
    st.write(llm(input_text))