import json
import requests
import pandas as pd

def formata_cnpj(numeroCnpj):
    
    # Formata o Cnpj com pontos e barras
    cnpj = '{}.{}.{}/{}-{}'.format(numeroCnpj[:2], numeroCnpj[2:5], numeroCnpj[5:8], numeroCnpj[8:12], numeroCnpj[12:])

    return cnpj

def tratamento_Matriz_Filial(indicadorMatrizFilial):
    ## Tratamento de Matriz / Filial
    if indicadorMatrizFilial == 1:
        return 'MATRIZ'
    else:
        return 'FILIAL'

def tratamento_Situacao_Cadastral_Motivo(situacaoCadastralMotivo):
    ## Tratamento de Situação cadastral sem motivo
    if situacaoCadastralMotivo == 'SEM MOTIVO':
        return ''
    else:
        return situacaoCadastralMotivo

def tratamento_Ente_Federado(enteFederado):

    ## Tratamento de Ente federado
    if enteFederado != '':
        return 'PJ PÚBLICO'
    else:
        return 'PJ PRIVADO'   

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
    matrizFilial = tratamento_Matriz_Filial(resultado['identificador_matriz_filial'])
    situacaoCadastralMotivo = tratamento_Situacao_Cadastral_Motivo(resultado['descricao_motivo_situacao_cadastral'])
    enteFederado = tratamento_Ente_Federado(resultado['ente_federativo_responsavel'])
    numeroCnpjFormatado = formata_cnpj(resultado['cnpj'])    
       
    print(f'''{numeroCnpjFormatado} - {enteFederado} - {matrizFilial} - {situacaoCadastral} - {situacaoCadastralMotivo} - {razaoSociao} ''')

print('consulta finalizada ! ')

