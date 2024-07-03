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
        print(f"Detalhes do erro: {response.text}")  # Adicionado para depuração
        return None

def calcular_medias_mensais(cotacoes):
    if not cotacoes:
        return None
    
    df = pd.DataFrame(cotacoes)
    df['dataHoraCotacao'] = pd.to_datetime(df['dataHoraCotacao'], errors='coerce')
    df = df.dropna(subset=['dataHoraCotacao'])
    df['Mes'] = df['dataHoraCotacao'].dt.to_period('M')
    medias_mensais = df.groupby('Mes')[['cotacaoCompra', 'cotacaoVenda']].mean().reset_index()
    medias_mensais['Mês'] = medias_mensais['Mes'].dt.strftime('%B/%Y').str.upper()
    medias_mensais = medias_mensais.rename(columns={'Mês': 'Período', 'cotacaoCompra': 'Média Compra', 'cotacaoVenda': 'Média Venda'})
    medias_mensais['Média Compra'] = medias_mensais['Média Compra'].apply(lambda x: f"{x:.4f}".replace('.', ','))
    medias_mensais['Média Venda'] = medias_mensais['Média Venda'].apply(lambda x: f"{x:.4f}".replace('.', ','))
    return medias_mensais[['Período', 'Média Compra', 'Média Venda']]

def get_image_base64(data_inicio, data_fim):
    cotacoes = get_cotacao(data_inicio, data_fim)
    if cotacoes:
        df = pd.DataFrame(cotacoes)

        if 'dataHoraCotacao' not in df.columns:
            print("A chave 'dataHoraCotacao' não está presente nos dados.")
            return None
        
        # Verificar e remover espaços em branco ou caracteres especiais nos nomes das colunas
        df.columns = df.columns.str.strip()
        
        # Converter a coluna 'dataHoraCotacao' para datetime
        df['dataHoraCotacao'] = pd.to_datetime(df['dataHoraCotacao'], errors='coerce')
        if df['dataHoraCotacao'].isnull().any():
            print("Erro ao converter 'dataHoraCotacao' para datetime.")
            print(df['dataHoraCotacao'])  # Adicionado para depuração
            return None

        df = df.set_index('dataHoraCotacao')
        
        # Plotar gráfico maior
        plt.figure(figsize=(14, 7))  # Aumentando o tamanho do gráfico
        plt.plot(df.index.strftime('%d/%m/%Y'), df['cotacaoCompra'], marker=',', linestyle='-', color='#6a0dad', label='Compra', linewidth=2)
        plt.plot(df.index.strftime('%d/%m/%Y'), df['cotacaoVenda'], marker=',', linestyle='-', color='#9370DB', label='Venda', linewidth=2)
        
        plt.style.use('seaborn-v0_8')
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
    data_inicio = input("Digite a data de início (formato MM-DD-AAAA): ")
    data_fim = input("Digite a data de fim (formato MM-DD-AAAA): ")
    cotacoes = get_cotacao(data_inicio, data_fim)
    medias_mensais = calcular_medias_mensais(cotacoes)
    
    if cotacoes is not None and medias_mensais is not None:
        # Gerar tabela de médias mensais em formato vertical e menor
        medias_mensais_html = medias_mensais.to_html(index=False, justify='center', classes='table table-striped')
        
        # Gerar tabela de precificação diária
        df = pd.DataFrame(cotacoes)
        tabela_html = df[['dataHoraCotacao', 'cotacaoCompra', 'cotacaoVenda']].copy()
        tabela_html['dataHoraCotacao'] = pd.to_datetime(tabela_html['dataHoraCotacao'], errors='coerce')
        tabela_html['dataHoraCotacao'] = tabela_html['dataHoraCotacao'].dt.strftime('%d/%m/%Y')
        tabela_html = tabela_html.rename(columns={'dataHoraCotacao': 'Data', 'cotacaoCompra': 'Compra', 'cotacaoVenda': 'Venda'})
        tabela_html['Compra'] = tabela_html['Compra'].apply(lambda x: f"{x:.4f}".replace('.', ','))
        tabela_html['Venda'] = tabela_html['Venda'].apply(lambda x: f"{x:.4f}".replace('.', ','))
        tabela_html = tabela_html.to_html(index=False, justify='center', classes='table table-striped')

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
                    margin-bottom: 20px;
                }}
                .chart img {{
                    width: 100%;
                    border: 1px solid #6a0dad;
                    border-radius: 8px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                th, td {{
                    padding: 8px;
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
                <div class="table-container">
                    <h2>Médias Mensais</h2>
                    <table>
                        <tbody>
                            {medias_mensais_html}
                        </tbody>
                    </table>
                </div>
                <div class="chart">
                    <h2>Variação do Dólar</h2>
                    <img src="data:image/png;base64,{get_image_base64(data_inicio, data_fim)}" alt="Variação do Dólar">
                </div>
                <h2>Precificação Diária</h2>
                <table>
                    <tbody>
                        {tabela_html}
                    </tbody>
                </table>
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

        print(f"Email gerado com sucesso: {file_path}")
    else:
        print("Não foi possível obter as cotações ou gerar o gráfico.")

if __name__ == "__main__":
    main()
