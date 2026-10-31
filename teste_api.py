#CONSUMO API

import requests
import os
from dotenv import load_dotenv

# CARREGANDO AS CONFIGURACOES
load_dotenv()

# OBTENDO A URL DA API
link_API = os.getenv("NASA_API_URL")

# REALIZANDO A REQUISICAO
resposta = requests.get(link_API)

# VERIFICANDO O STATUS DA REQUISICAO
print("Status HTTP:", resposta.status_code)

if resposta.status_code == 200:

    dados = resposta.json()

    print("Requisição realizada com sucesso!")
    print("Quantidade de publicações:", len(dados))

    # MOSTRANDO OS DADOS
    for publicacao in dados:

        print("--------------------------")
        print("Título:", publicacao.get("title"))
        print("Data:", publicacao.get("date"))
        print("Tipo:", publicacao.get("media_type"))

else:

    print("Erro na requisição.")
    print(resposta.text)
