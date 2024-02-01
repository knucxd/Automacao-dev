import mysql.connector
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import tkinter as tk
from tkinter import simpledialog

# Configuração do navegador
driver = webdriver.Chrome()

#Iniciando conexao com o BD, favor alterar conforme necessidade
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='automacao'
)

cursor = conexao.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS produtos(
               id INT AUTO_INCREMENT PRIMARY KEY)''') #Alerta de gambi

cursor.execute('''DROP TABLE produtos''') #Alerta de gambi

def Primeiro_Acesso():
    driver.get("https://www.mercadolivre.com.br")

# Acessar o Mercado Livre
Primeiro_Acesso()

# Função para obter a pesquisa do usuário via interface gráfica
root = tk.Tk()
root.withdraw()
pesquisa = simpledialog.askstring("Pesquisa", "Digite o nicho de produtos desejado:")

# Navegar até o Mercado Livre e pesquisar produtos
campo_pesquisa = driver.find_element(By.XPATH, "/html/body/header/div/div[2]/form/input")
campo_pesquisa.send_keys(pesquisa)
campo_pesquisa.send_keys(Keys.RETURN)

elementos_valores_reais =driver.find_elements(By.CLASS_NAME, "andes-money-amount__fraction")
valores_em_reais = []

for i in range(min(10, len(elementos_valores_reais))):
    valor_em_reais = elementos_valores_reais[i].text
    valores_em_reais.append(valor_em_reais)

driver.get("https://www.google.com/search?client=opera-gx&q=cotação+dolár&sourceid=opera&ie=UTF-8&oe=UTF-8")
cotacao = float(driver.find_element(By.CLASS_NAME, "SwHCTb").text.replace(',', '.'))

# Iterar sobre os primeiros 10 elementos da lista e calcular o valor em dólar para cada um
valores_em_dolar = []
for a in range(min(10, len(valores_em_reais))):
    valor_em_reais = valores_em_reais[a].replace('R$', '').replace(',', '')
    valor_em_dolar = float(valor_em_reais) / cotacao
    valores_em_dolar.append(valor_em_dolar)

# Adicionar prints para verificar os valores antes de iniciar o loop de inserção
print("Valores em reais:", valores_em_reais)
print("Valores em dólar:", valores_em_dolar)
    

# Criar a tabela se não existir
cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    valor_em_reais VARCHAR(50),
                    valor_em_dolar DECIMAL(10, 2)
                  )''')

# Adicionar um print para verificar se o loop de inserção está sendo alcançado
print("Iniciando loop de inserção no banco de dados...")

# Inserir os dados na tabela
for i, valor_em_reais in enumerate(valores_em_reais):
    valor_em_dolar = valores_em_dolar[i]

    # Adicionar um print dentro do loop de inserção
    print(f"Inserindo dados: {valor_em_reais}, {valor_em_dolar}")

    try:
        cursor.execute('INSERT INTO produtos (valor_em_reais, valor_em_dolar) VALUES (%s, %s)',
                       (valor_em_reais, valor_em_dolar))
        print("Dados inseridos com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro durante a inserção de dados: {err}")

# Commit para salvar as alterações
conexao.commit()

# Extrair dados do MySQL e retornar em uma planilha Excel
cursor.execute('SELECT * FROM produtos')
dados = cursor.fetchall()

# Criar um DataFrame pandas com os dados
df = pd.DataFrame(dados, columns=['id', 'Valor em Reais', 'Valor em Dólar'])

# Salvar o DataFrame em uma planilha Excel
df.to_excel('dados_mercado_livre.xlsx', index=False)
print("Planilha gerada com sucesso!")

# Fechar conexão com o banco de dados
conexao.close()

# Fechar o navegador
driver.quit()