from flask import Flask, request, jsonify
import sqlite3
import requests
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Isso habilita o CORS para todas as rotas

def init_db():
    with sqlite3.connect('cotacoes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cotacoes (
                data TEXT PRIMARY KEY,
                valor REAL NOT NULL,
                variacao REAL
            )
        ''')
        conn.commit()

def get_cotacao_from_db(data):
    with sqlite3.connect('cotacoes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT data, valor FROM cotacoes WHERE data=?', (data,))
        result = cursor.fetchone()
    return result

def fetch_cotacao_from_api(data):
    data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.10813/dados?formato=json&dataInicial={data_formatada}&dataFinal={data_formatada}'
    response = requests.get(url)
    if response.status_code == 200:
        cotacao_data = response.json()
        if cotacao_data and cotacao_data[0]['data'] == data_formatada:
            valor = float(cotacao_data[0]['valor'].replace(',', '.'))
            return valor
        else:
            print(f"Nenhuma cotação encontrada para a data {data}")
    else:
        print(f"Erro ao buscar cotação: status code {response.status_code}, response: {response.text}")
    return None

def save_cotacao_to_db(data, valor):
    with sqlite3.connect('cotacoes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO cotacoes (data, valor) VALUES (?, ?)', (data, valor))
        conn.commit()

def fetch_and_save_cotacao_if_needed(data):
    valor = fetch_cotacao_from_api(data)
    if valor is not None:
        save_cotacao_to_db(data, valor)
    return valor

def calculate_variacao(data_atual_str, valor_atual):
    data_atual = datetime.strptime(data_atual_str, '%Y-%m-%d')
    dia_anterior = data_atual - timedelta(days=1)
    while dia_anterior.weekday() > 4:  # Ignora fins de semana
        dia_anterior -= timedelta(days=1)
    dia_anterior_str = dia_anterior.strftime('%Y-%m-%d')

    # Verifica se a cotação do dia anterior está no banco de dados
    cotacao_anterior = get_cotacao_from_db(dia_anterior_str)
    if not cotacao_anterior:
        # Se não estiver, tenta buscar da API e salvar no banco de dados
        valor_anterior = fetch_and_save_cotacao_if_needed(dia_anterior_str)
        if valor_anterior is None:
            return None  # Se não conseguir obter a cotação do dia anterior, retorna None
    else:
        valor_anterior = cotacao_anterior[1]

    variacao = ((valor_atual - valor_anterior) / valor_anterior) * 100
    return variacao

@app.route('/cotacao', methods=['GET'])
def get_cotacao():
    data = request.args.get('data')
    if not data:
        return jsonify({"error": "Data não fornecida"}), 400
    
    cotacao = get_cotacao_from_db(data)
    if cotacao:
        variacao = calculate_variacao(data, cotacao[1])
        return jsonify({
            "data": cotacao[0],
            "valor": cotacao[1],
            "variacao": variacao
        })

    valor = fetch_cotacao_from_api(data)
    if valor is not None:
        save_cotacao_to_db(data, valor)
        variacao = calculate_variacao(data, valor)
        return jsonify({
            "data": data,
            "valor": valor,
            "variacao": variacao
        })
    else:
        return jsonify({"error": "Cotação não encontrada na API"}), 404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)