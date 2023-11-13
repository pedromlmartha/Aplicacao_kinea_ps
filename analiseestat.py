import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import os
cwd = os.getcwd().replace("\\", "/") # This fn will return the Current Working Directory
print("Trabalhando no diretório:", cwd)

# Carregar os dados do arquivo CSV
df = pd.read_csv(f'{cwd}/historico_cotacoes_dolar.csv')

# Verificando as primeiras linhas dos dados
print(df.head())

df['valor'] = pd.to_numeric(df['valor'].str.replace(',', '.'), errors='coerce')
df.dropna(subset=['valor'], inplace=True)  # Remove linhas com valores nulos

df['variacao'] = df['valor'].pct_change() * 100
df.dropna(subset=['variacao'], inplace=True)  # Remove a primeira linha que terá variação nula
print(df.head())

media = df['variacao'].mean()
print(f"Média da variação: {media}")
desvio_padrao = df['variacao'].std()
print(f"Desvio padrão da variação: {desvio_padrao}")

limite_normal = desvio_padrao
limite_moderado = 2 * desvio_padrao
limite_significativo = 3 * desvio_padrao

print("Variação Muito Relevante: Até ±{:.2f}%".format(limite_normal))
print("Variação Relevante: Até ±{:.2f}%".format(limite_moderado))
print("Variação Pouco Relevante: Até ±{:.2f}%".format(limite_significativo))

plt.figure(figsize=(10, 6))
sns.histplot(df['variacao'], kde=True, bins=30)
plt.title('Distribuição da Variação Diária do Dólar')
plt.xlabel('Variação Percentual')
plt.ylabel('Frequência')
plt.show()