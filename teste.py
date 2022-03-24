import json
import requests
import pandas as pd
import time


def get_cnpj_data(cnpj):

    # Dado um CNPJ, faz uma requisição para a API Minha Receita. Caso a requisição seja bem sucedida, retorna o conteúdo da requisição em formato json
    minha_receita_api_url = 'https://minhareceita.org/'
    requisicao = requests.post(minha_receita_api_url, data=cnpj, timeout=None)
    if requisicao.status_code == 200:

        return json.loads(requisicao.content)

    else:
        print('Falha na consulta !')

cnpj = {'cnpj': 18237440000122}
resultado = get_cnpj_data(cnpj)
razaoSociao = resultado['razao_social']

print(resultado)
print(razaoSociao)

print('consulta finalizada ! ')

