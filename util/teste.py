import requests


def consultar_cnpj(cnpj):
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


# Exemplo de uso
cnpj = '05054929000117'  # Substitua pelo CNPJ desejado
resultado = consultar_cnpj(cnpj)
if resultado:
    razaoSociao = resultado['razao_social']
    print(razaoSociao)