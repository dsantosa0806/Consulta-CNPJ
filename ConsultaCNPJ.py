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


table = pd.read_excel('dados.xlsx')
for i, cnpj in enumerate(table['CNPJ1']):
    cnpj = {'cnpj': "%014d" % cnpj}
    resultado = get_cnpj_data(cnpj)
    print(i,cnpj,' - ', resultado['razao_social'],' _ ',resultado['descricao_situacao_cadastral'],' Status Matriz/Filial * ', resultado['identificador_matriz_filial'])

print('consulta finalizada ! ')

