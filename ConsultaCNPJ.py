import json
import requests
import pandas as pd

def get_cnpj_data(cnpj):

    # Dado um CNPJ, faz uma requisição para a API Minha Receita. Caso a requisição seja bem sucedida, retorna o conteúdo da requisição em formato json
    minha_receita_api_url = 'https://minhareceita.org/'
    requisicao = requests.post(minha_receita_api_url, data=cnpj, timeout=None)
    if requisicao.status_code == 200:

        return json.loads(requisicao.content)

    else:
        print('Falha na consulta !')

## Instanciando a Tabela
## Os Cnpj's da tabela precisam estar sem formatação
table = pd.read_excel('dados.xlsx')

for i, cnpj in enumerate(table['CNPJ1']):
    cnpj = {'cnpj': "%014d" % cnpj}
    resultado = get_cnpj_data(cnpj)
    razaoSociao = resultado['razao_social']
    situacaoCadastral = resultado['descricao_situacao_cadastral']
    indicadorMatrizFilial = resultado['identificador_matriz_filial']
    situacaoCadastralMotivo = resultado['descricao_motivo_situacao_cadastral']
    enteFederado = resultado['ente_federativo_responsavel']
    numeroCnpj = resultado['cnpj']
    numeroCnpjFormatado = '{}.{}.{}/{}-{}'.format(numeroCnpj[:2], numeroCnpj[2:5], numeroCnpj[5:8], numeroCnpj[8:12], numeroCnpj[12:])

## Tratamento de Matriz / Filial
    if indicadorMatrizFilial == 1:
        indicadorMatrizFilial = 'MATRIZ'
    else:
        indicadorMatrizFilial = 'FILIAL'
## Tratamento de Situação cadastral sem motivo
    if situacaoCadastralMotivo == 'SEM MOTIVO':
        situacaoCadastralMotivo = ''
    else:
        situacaoCadastralMotivo
## Tratamento de Ente federado
    if enteFederado != '':
        enteFederado = 'PJ PÚBLICO'
    else:
        enteFederado = 'PJ PRIVADO'        

    print(f'''{numeroCnpjFormatado} - ({enteFederado}) - {indicadorMatrizFilial} - {situacaoCadastral} - {situacaoCadastralMotivo} - {razaoSociao} ''')

print('consulta finalizada ! ')

