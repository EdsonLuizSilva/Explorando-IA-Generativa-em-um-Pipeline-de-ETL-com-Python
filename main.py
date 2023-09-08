
# Desafio Santader (ETL em Python)

# **Contexto:** Você é um cientista de dados no Santander e
# recebeu a tarefa de envolver seus clientes de maneira mais personalizada.
# Seu objetivo é usar o poder da IA Generativa para criar
# mensagens de marketing personalizadas que serão entregues a cada cliente por e-mail.
#
# **Condições do Problema:**
#
# 1. Você recebeu uma planilha simples do setor de marketing da Santander, em formato CSV ('data_cliente.csv'),
# com uma lista de cliente do banco.
#
# 2. O seu trabalho é fazer uma limpeza na planilha para obter os dados de cada cliente valido.
#
# 3. Após obter os dados dos clientes, você vai usar a API do ChatGPT (OpenAI)
# para gerar uma mensagem de marketing personalizada para cada cliente.
# Essa mensagem deve enfatizar a importância dos investimentos.
#
# 4. Uma vez que a mensagem para cada cliente esteja pronta,
# você vai enviar essas informações de volta para a um bando de dados onde o setor de marketing podera acessar.

# Importando as Bibliotecas
import pandas as pd
import openai
import sqlite3

## Fazendo a extração de dados da planilha. ##

# Lendo um arquivo CSV
df = pd.read_csv("data_cliente.csv")
df.head()

# Quantidades de Linhas e Colunas
df.info()

## Fazendo as Transformações dos dados. ##

# Selicionando as colunas necessarias.
df_clientes = df[['customer_id', 'first_name', 'last_name', 'email', 'gender', 'date_added']]

# Inserindo uma nova coluna que vai guardar a mensagem para cada cliente
df_clientes.insert(6,'Menssagem','')

# Selecionando as 5 primeiras linhas para teste
df_clientes = df_clientes.loc[0:2,['customer_id', 'first_name', 'last_name', 'email', 'gender', 'date_added', 'Menssagem']]
df_clientes.head(10)

# Usando API do ChatGPT para criar menssagem para cada cliente
openai_api_key = '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'


openai.api_key = openai_api_key

for i, row in df_clientes.iterrows():
    nome = df_clientes.first_name[i]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em markting bancário."
            },
            {
                "role": "user",
                "content": f"Crie uma mensagem para o cliente {nome} sobre a importância dos investimentos (máximo de 100 caracteres)"
            }
        ]
    )
    msg = completion.choices[0].message.content.strip('\"')
    df_clientes.at[i, 'Menssagem'] = msg


## Enviando para o Banco de Dados ##

connection = sqlite3.connect('DioSantander.db')
cursor = connection.cursor()

for i, row in df_clientes.iterrows():
    customer_id = df_clientes.customer_id[i]
    first_name = df_clientes.first_name[i]
    last_name = df_clientes.last_name[i]
    email = df_clientes.email[i]
    gender = df_clientes.gender[i]
    date_added = df_clientes.date_added[i]
    Menssagem = df_clientes.Menssagem[i]

    query = f"INSERT INTO clientes (customer_id, first_name, last_name, email, gender, date_added, Menssagem) VALUES ('{customer_id}', '{first_name}', '{last_name}', '{email}', '{gender}', '{date_added}', '{Menssagem}')"

    cursor.execute(query)

connection.commit()
connection.close()
