import os

# Pasta com os ficheiros individuais
PASTA_TEMAS = "conteudo_cmvc_por_tema"
FICHEIRO_SAIDA = "conteudo_cmvc_resumido.txt"

# Ordem desejada dos temas
ordem_temas = [
    "municipio", "turismo", "educacao", "juventude", "cultura",
    "desporto", "ambiente", "saude", "urbanismo", "acao_social"
]

conteudo_total = ""

def limpar_linhas(texto):
    linhas = texto.split("\n")
    novas = []
    for linha in linhas:
        linha = linha.strip()
        if linha and linha not in novas:
            novas.append(linha)
    return "\n".join(novas)

print(" A criar ficheiro final com conteúdo máximo possível...")

for tema in ordem_temas:
    caminho = os.path.join(PASTA_TEMAS, f"{tema}.txt")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
            conteudo_limpo = limpar_linhas(conteudo)
            conteudo_total += f"\n\n--- {tema.upper()} ---\n{conteudo_limpo}"
    else:
        print(f" Tema {tema} não encontrado.")

# Corta se ultrapassar 10000 palavras (~8K tokens)
palavras = conteudo_total.split()
if len(palavras) > 10000:
    print(f" Conteúdo excede 10000 palavras ({len(palavras)}). Será cortado.")
    conteudo_total = " ".join(palavras[:10000])

# Guardar ficheiro final
with open(FICHEIRO_SAIDA, "w", encoding="utf-8") as f:
    f.write(conteudo_total)

print(f" Ficheiro '{FICHEIRO_SAIDA}' gerado com sucesso.")
