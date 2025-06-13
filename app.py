import streamlit as st
import requests

# Lê o conteúdo da CMVC
with open("conteudo_cmvc_resumido.txt", "r", encoding="utf-8") as f:
    contexto = f.read()

st.set_page_config(page_title="Chatbot CMVC", page_icon="🏛️")
st.title("🏛️ Chatbot CMVC")
st.write("Faz-me perguntas sobre a Câmara Municipal de Viana do Castelo.")

pergunta = st.text_input("❓ Pergunta:")

if pergunta:
    prompt = f"""
Responde como se fosses um assistente oficial da Câmara Municipal de Viana do Castelo.
Usa apenas a informação que te dou a seguir para responder.

[CONTEÚDO]
{contexto}

[PERGUNTA]
{pergunta}
"""

    headers = {
        "Authorization": "Bearer tgp_v1_BllQx-qQ9kq0GfJwP_wp5lilRCHapnLhW9EIViraQrU",  # substitui pelo token da Together
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7
    }

    response = requests.post("https://api.together.xyz/inference", headers=headers, json=data)

    if response.status_code == 200:
        choices = response.json().get("choices")
        if choices and len(choices) > 0:
            resposta = choices[0].get("text", "").strip()
            st.write(f"💬 {resposta}")
        else:
            st.warning("⚠️ A API respondeu sem conteúdo.")
    else:
        st.error(f"❌ Erro {response.status_code}: {response.text}")
