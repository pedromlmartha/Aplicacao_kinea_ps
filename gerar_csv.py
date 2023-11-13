import requests
from datetime import datetime
import pandas as pd

def fetch_historical_data():
    # Definindo o intervalo de datas
    start_date = "1994-07-01"  # Data inicial da série histórica do dólar
    end_date = datetime.now().strftime('%Y-%m-%d')  # Data atual

    # Formatar as datas para o formato esperado pela API
    start_date_formatted = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d/%m/%Y')
    end_date_formatted = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d/%m/%Y')

    # URL da API
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.10813/dados?formato=json&dataInicial={start_date_formatted}&dataFinal={end_date_formatted}"

    # Realizar a requisição à API
    response = requests.get(url)
    if response.status_code != 200:
        return None, "Erro ao buscar dados da API"

    # Converter a resposta em JSON
    data = response.json()

    # Transformar em DataFrame
    df = pd.DataFrame(data)
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df['valor'] = df['valor'].str.replace(',', '.').astype(float)
    return df, None

# Coletar os dados
historical_data, error = fetch_historical_data()

if error:
    print(error)
else:
    print(historical_data.head())  # Mostrar os primeiros registros para verificar
    print(f"Total de registros: {len(historical_data)}")
    historical_data.to_csv("historico_cotacoes_dolar.csv", index=False, decimal=",")