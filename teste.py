import json
from cv2 import split
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

cnpj = {'cnpj': 18237440000122} # 18.237.440/0001-22
resultado = get_cnpj_data(cnpj)
razaoSociao = resultado['razao_social']
numeroCnpj = resultado['cnpj']
numeroCnpjFormatado = '{}.{}.{}/{}-{}'.format(numeroCnpj[:2], numeroCnpj[2:5], numeroCnpj[5:8], numeroCnpj[8:12], numeroCnpj[12:])

#print(resultado)
#print(razaoSociao)
print(numeroCnpjFormatado)

print('consulta finalizada ! ')

