from flask import Flask, render_template, request, session, redirect, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv

app = Flask(__name__)
app.secret_key = 'segredo_super_secreto'

API_KEY = os.getenv("API_KEY")

# Carrega conteúdo relevante com base na pergunta
def carregar_contexto_relevante(pergunta):
    contexto_total = ""
    tema_keywords = {
        "turismo": ["visitar", "turismo", "pontos turísticos", "praias"],
        "educacao": ["escolas", "educação", "bolsas", "ensino"],
        "cultura": ["museus", "eventos", "romarias", "cultura"],
        "desporto": ["desporto", "piscinas", "atividade física"],
        "ambiente": ["ambiente", "reflorestar", "ecovias"],
        "saude": ["saúde", "unidade de saúde", "vida"],
        "urbanismo": ["urbanismo", "ordenamento", "plano", "taxas"],
        "acao_social": ["apoio", "habitação", "inclusão", "social"],
        "juventude": ["jovens", "juventude", "cartão jovem", "podcast"],
        "municipio": ["câmara", "executivo", "contactos"]
    }

    for tema, palavras in tema_keywords.items():
        if any(p in pergunta.lower() for p in palavras):
            caminho = f"conteudo_cmvc_por_tema/{tema}.txt"
            if os.path.exists(caminho):
                with open(caminho, "r", encoding="utf-8") as f:
                    contexto_total += f"\n--- {tema.upper()} ---\n" + f.read()

    if not contexto_total:
        try:
            with open("conteudo_cmvc_resumido.txt", "r", encoding="utf-8") as f:
                contexto_total = f.read()
        except:
            contexto_total = "[Erro ao carregar contexto base]"

    return contexto_total

@app.route("/", methods=["GET", "POST"])
def index():
    if "historico" not in session:
        session["historico"] = []

    if request.method == "POST":
        pergunta = request.form["pergunta"]
        contexto_base = carregar_contexto_relevante(pergunta)

        # Monta histórico resumido
        bloco_historico = "\n".join(
            [f"{h['pergunta']} => {h['resposta']}" for h in session["historico"][-2:]]
        )

        # Prompt melhorado
        prompt = f"""
Responde como se fosses um assistente oficial da Câmara Municipal de Viana do Castelo.
Usa apenas a informação fornecida. Sê claro, direto e evita repetições.
Não inventes nem respondas a mais do que te for perguntado.

[CONTEÚDO]
{contexto_base}

[HISTÓRICO]
{bloco_historico}

[PERGUNTA]
{pergunta}

[INSTRUÇÃO]
Responde apenas à pergunta de forma clara e concisa.
"""

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "prompt": prompt,
            "max_tokens": 350,
            "temperature": 0.5
        }

        resposta = "Erro na resposta"
        try:
            response = requests.post("https://api.together.xyz/inference", headers=headers, json=data)
            if response.status_code == 200:
                resposta = response.json().get("output") or response.json().get("choices", [{}])[0].get("text", "").strip()
            else:
                resposta = f"Erro {response.status_code}: {response.text}"
        except Exception as e:
            resposta = f"Erro ao contactar API: {e}"

        session["historico"].append({"pergunta": pergunta, "resposta": resposta})
        session.modified = True

    return render_template("chat.html", historico=session.get("historico", []))

@app.route("/limpar")
def limpar():
    session.pop("historico", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
