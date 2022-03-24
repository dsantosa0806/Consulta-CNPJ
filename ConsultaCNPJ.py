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
    razaoSociao = resultado['razao_social']
    situacaoCadastral = resultado['descricao_situacao_cadastral']
    indicadorMatrizFilial = resultado['identificador_matriz_filial']
    situacaoCadastralMotivo = resultado['descricao_motivo_situacao_cadastral']
    enteFederado = resultado['ente_federativo_responsavel']

## Tratamento de Matriz / Filial
    if indicadorMatrizFilial == 1:
        indicadorMatrizFilial = 'Matriz'
    else:
        indicadorMatrizFilial = 'Filial'
## Tratamento de Situação cadastral sem motivo
    if situacaoCadastralMotivo == 'SEM MOTIVO':
        situacaoCadastralMotivo = ''
    else:
        situacaoCadastralMotivo

## Tratamento de Ente federado

    if enteFederado != '':
        enteFederado = 'PJ de direito Público'
    else:
        enteFederado = 'Pj de direito Privado'
        

    print(f'''{i},{cnpj} -  {razaoSociao} _ {situacaoCadastral} * {indicadorMatrizFilial} - {situacaoCadastralMotivo} ({enteFederado})''')

print('consulta finalizada ! ')

