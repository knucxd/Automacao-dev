# Automação Mercado Livre

Este script Python realiza automação no Mercado Livre, pesquisando produtos com base em um nicho fornecido pelo usuário, coletando informações sobre esses produtos, convertendo os valores para dólar e armazenando os dados em um banco de dados MySQL. Além disso, gera uma planilha Excel com os resultados.

## Pré-requisitos

Certifique-se de ter os seguintes requisitos instalados:

- [Python](https://www.python.org/) (versão utilizada: 3.x)
- [Selenium](https://www.selenium.dev/)
- [MySQL Connector](https://pypi.org/project/mysql-connector-python/)
- [Pandas](https://pandas.pydata.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) (ou outro WebDriver compatível)

## Configuração

1. Instale as dependências usando o seguinte comando:
   ```bash
   pip install selenium mysql-connector-python pandas
