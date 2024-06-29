import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import base64
from datetime import datetime

def get_cotacao(data_inicio, data_fim):
    url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='{data_inicio}'&@dataFinalCotacao='{data_fim}'&$top=100&$format=json&$select=cotacaoCompra,dataHoraCotacao,cotacaoVenda"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('value', [])
    else:
        print(f"Erro ao obter cotações: {response.status_code}")
        return None

def get_image_base64(data_inicio, data_fim):
    cotacoes = get_cotacao(data_inicio, data_fim)
    if cotacoes:
        df = pd.DataFrame(cotacoes)
        df['dataHoraCotacao'] = pd.to_datetime(df['dataHoraCotacao'])
        df = df.set_index('dataHoraCotacao')
        
        # Plotar gráfico
        plt.figure(figsize=(10, 5))
        plt.plot(df.index.strftime('%d/%m/%Y'), df['cotacaoCompra'], marker=',', linestyle='-', color='#6a0dad', label='Compra', linewidth=2)
        plt.plot(df.index.strftime('%d/%m/%Y'), df['cotacaoVenda'], marker=',', linestyle='-', color='#9370DB', label='Venda', linewidth=2)
        
        plt.style.use('seaborn-v0_8')
        plt.title('Variação do Dólar', fontsize=16, fontweight='bold', color='#6a0dad')
        plt.ylabel('Valor (R$)', fontsize=12, fontweight='bold', color='#6a0dad')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Salvar o gráfico como imagem temporária
        image_file = 'variacao_dolar.png'
        plt.savefig(image_file)
        plt.close()
        
        # Ler o arquivo de imagem e codificar em base64
        with open(image_file, 'rb') as f:
            image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        return image_base64
    else:
        return None

def main():
    data_inicio = "06-01-2024"
    data_fim = "06-28-2024"
    image_base64 = get_image_base64(data_inicio, data_fim)
    
    if image_base64:
        cotacoes = get_cotacao(data_inicio, data_fim)
        df = pd.DataFrame(cotacoes)
        df['dataHoraCotacao'] = pd.to_datetime(df['dataHoraCotacao'])
        df['Data'] = df['dataHoraCotacao'].dt.strftime('%d/%m/%Y')
        df = df[['Data', 'cotacaoCompra', 'cotacaoVenda']].rename(columns={
            'cotacaoCompra': 'Compra',
            'cotacaoVenda': 'Venda'
        })
        
        # Gerar tabela de precificação diária
        tabela_html = df.to_html(index=False, justify='center', classes='table table-striped')

        # Construir o corpo do e-mail com melhor design
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }}
                .container {{
                    width: 80%;
                    margin: 20px auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #6a0dad;
                    text-align: center;
                }}
                h2 {{
                    color: #9370DB;
                    border-bottom: 2px solid #6a0dad;
                    padding-bottom: 5px;
                }}
                .chart {{
                    text-align: center;
                }}
                .chart img {{
                    max-width: 100%;
                    height: auto;
                    border: 1px solid #6a0dad;
                    border-radius: 8px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    padding: 12px;
                    border: 1px solid #dddddd;
                    text-align: center;
                }}
                th {{
                    background-color: #6a0dad;
                    color: #ffffff;
                }}
                tr:nth-child(even) {{
                    background-color: #f4f4f4;
                }}
                tr:hover {{
                    background-color: #e0e0e0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    color: #999999;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Dashboard de Variação do Dólar</h1>
                <h2>Variação do Dólar</h2>
                <div class="chart">
                    <img src="data:image/png;base64,{image_base64}" alt="Variação do Dólar">
                </div>
                <h2>Precificação Diária</h2>
                {tabela_html}
                <div class="footer">
                    <p>Este é um e-mail automático, por favor, não responda.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Criação do arquivo .eml
        file_path = os.path.join(os.getcwd(), "dashboard_variacao_dolar.eml")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("Subject: Dashboard de Variação do Dólar\n")
            file.write("Date: {}\n".format(datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')))
            file.write("Content-Type: text/html; charset=utf-8\n")
            file.write("Content-Transfer-Encoding: 8bit\n")
            file.write("\n")
            file.write(html)
        
        print(f"Arquivo .eml gerado com sucesso em: {file_path}")
        print("Rascunho do e-mail gerado com sucesso!")

    else:
        print("Não foi possível obter as cotações ou gerar o gráfico.")

if __name__ == "__main__":
    main()
