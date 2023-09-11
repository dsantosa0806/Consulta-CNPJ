from datetime import datetime 
import json
import requests
import pandas as pd
import sqlite3


def cadastrar_demanda():
    conexao = sqlite3.connect('Bd_teste.db')
    c = conexao.cursor()

    #Inserir dados na tabela do BD:
    c.execute("INSERT INTO Cnpjs_Consultados VALUES (:cnpj,:TipoCnpj,:StatusMatrizFilial,:Situacao,:SituacaoMotivo,:Nome)",
              {
                  'cnpj': numeroCnpjFormatado,
                  'TipoCnpj': enteFederado,
                  'StatusMatrizFilial': matrizFilial,
                  'Situacao': situacaoCadastral,
                  'SituacaoMotivo': situacaoCadastralMotivo,
                  'Nome': razaoSociao
              })

    # Commit as mudanças:
    conexao.commit()

    # Fechar o banco de dados:
    conexao.close()


def exporta_dados():
    conexao = sqlite3.connect('Bd_teste.db')
    c = conexao.cursor()

    # Inserir dados na tabela:
    c.execute("SELECT *, oid FROM Cnpjs_Consultados")
    dados = c.fetchall()
    # print(usuarios_cadastrados)
    data = (datetime.today().strftime('%Y-%m-%d %H_%M'))
    dados = pd.DataFrame(dados, columns=['cnpj','TipoCnpj','StatusMatrizFilial','Situacao','SituacaoMotivo','Nome','id'])
    dados.to_excel(f'''dados_finalizados_{data}.xlsx''',sheet_name='Resultado',index=False)

    # Commit as mudanças:
    conexao.commit()

    # Fechar o banco de dados:
    conexao.close()


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
    url = f'https://minhareceita.org/{cnpj}'  # Substitua pela URL da API desejada

    # Realiza a requisição GET à API
    response = requests.get(url)

    # Verifica o código de status da resposta
    if response.status_code == 200:
        # Requisição bem-sucedida
        data = response.json()
        return data
    else:
        # Erro na requisição
        print(f'Erro {response.status_code}: {response.text}')
        return None


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
    cadastrar_demanda()


print('Cadastro Finalizado ! ')
