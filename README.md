# avgtaxbacen-bot

O `avgtaxbacen-bot` é um script Python desenvolvido para obter e processar dados de taxa média de câmbio fornecidos pelo Banco Central do Brasil (Bacen). Ele automatiza a coleta de dados, gera relatórios visuais e pode preparar e-mails com anexos de relatórios para facilitar a análise das variações cambiais.

## Funcionalidades

- **Coleta de Dados**: Utiliza a API de dados abertos do Bacen para obter informações de taxas de câmbio.
- **Processamento de Dados**: Calcula a taxa média de câmbio para um período específico a partir dos dados obtidos.
- **Visualização**: Gera gráficos para visualizar a variação das taxas de câmbio ao longo do tempo.
- **Exportação de Relatórios**: Cria arquivos HTML e templates de e-mail para relatar as informações coletadas.
- **Automatização**: Capacidade de automatizar o envio de e-mails com relatórios anexados, se necessário.

## Pré-requisitos

- Python 3.x instalado.
- Bibliotecas necessárias listadas no arquivo `requirements.txt`.

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/sawdfer/avgtaxbacen-bot.git
   ```
2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Uso
1. Configure as datas de início e fim no arquivo `avgtaxbacen.py`.
2. Execute o script:
   ```bash
   python avgtaxbacen.py
   ```
3. Verifique os arquivos gerados na pasta do projeto:
    - variacao_dolar.png: Gráfico de variação do dólar.
    - email_rascunho.html: Rascunho do e-mail em HTML.
    - dashboard_variacao_dolar.msg: Arquivo .msg com o e-mail pronto para envio.

# Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias, correções de bugs ou novas funcionalidades.

# Licença
Este projeto está licenciado sob a [MIT License](https://github.com/sawdfer/avgtaxbacen-bot/blob/main/LICENSE).