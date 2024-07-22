# myPrecoTeto
# Parti 1
# Análise de Dividendos de Ativos

Este projeto tem como objetivo analisar o histórico de dividendos de ativos, calcular preços justos usando modelos financeiros, e recomendar ações ou fundos imobiliários (FII) com base em suas cotações atuais e modelos de valuation.

## Funcionalidades

- Coleta de dados históricos de dividendos de ativos usando a biblioteca `yfinance`.
- Cálculo do preço justo de ativos usando os modelos de Gordon e Bazin.
- Recomendação de compra com base nos preços calculados.
- Exibição dos resultados em um DataFrame do Pandas.

## Estrutura do Código

### Funções Principais

- `limpa_tela()`: Limpa a tela do terminal.
- `coleta_dividendos(ticker)`: Coleta o histórico de dividendos de um ativo e calcula o total de dividendos por ano.
- `modelo_gordon(dividendo, taxa_retorno=0.06, taxa_crescimento=0.005)`: Calcula o preço justo de um ativo usando o modelo de Gordon.
- `modelo_bazin(dividendo, taxa_retorno=0.06)`: Calcula o preço justo de um ativo usando o modelo de Bazin.
- `calcula_dividendos(dividendos_ano, anos=5)`: Calcula o total e a média dos dividendos para um número específico de anos.
- `verificar_tipo(ticker)`: Verifica o tipo de ativo (Ação ou FII) com base na descrição do ativo no Yahoo Finance.

### Parâmetros

- `ticker`: Símbolo do ativo no Yahoo Finance.
- `taxa_retorno`: Lista de taxas de retorno esperadas para ações e FIIs.
- `taxa_crescimento`: Taxa de crescimento esperada dos dividendos.
- `anos_solicitados`: Número de anos para análise de dividendos.

### Exemplo de Uso

```python
# Lista de tickers para análise
tickers = ["BBSE3.SA", "PORD11.SA"]

# Parâmetros
taxa_retorno = [0.08, 0.10]
taxa_crescimento = 0.005
anos_solicitados = 5

# Criação de uma lista para armazenar os dados de todos os tickers
dados_ativos = []

# Processa cada ticker
for ticker in tickers:
    dividendos = coleta_dividendos(ticker)
    if dividendos is not None:
        tipo_ativo = verificar_tipo(ticker)
        total_dividendos, media_dividendos, anos_disponiveis = calcula_dividendos(dividendos, anos_solicitados)
        
        ativo = yf.Ticker(ticker)
        cotacao_atual = ativo.info.get('currentPrice', 0)
        dy_div = ativo.info.get('dividendYield', 0) * cotacao_atual
        
        gordon = modelo_gordon(media_dividendos, taxa_retorno[0], taxa_crescimento)
        bazin = modelo_bazin(media_dividendos, taxa_retorno[1])
        
        recomendacao_gordon = '🟢' if cotacao_atual < gordon else '🔴'
        recomendacao_bazin = '🟢' if cotacao_atual < bazin else '🔴'
        
        # Determina a taxa de retorno com base no tipo de ativo
        taxa_retorno_acao = taxa_retorno[0] * 100 if tipo_ativo == 'Ação' else taxa_retorno[1] * 100
        
        dados_ativos.append({
            'Ticker': ticker,
            'Tipo': tipo_ativo,
            'Preço Atual': f'R${cotacao_atual:.2f}',
            'Preço Teto (Gordon)': f'R${gordon:.2f}',
            'Margem Gordon': f'R${gordon - cotacao_atual:.2f}',
            'Preço Teto (Bazin)': f'R${bazin:.2f}',
            'Margem Bazin': f'R${bazin - cotacao_atual:.2f}',
            'Recomendação Gordon': recomendacao_gordon,
            'Recomendação Bazin': recomendacao_bazin,
            'Taxa de Retorno (%)': f'{taxa_retorno_acao:.2f}%',  # Taxa de retorno condicional
            'Taxa de Crescimento': f'{taxa_crescimento * 100:.2f}%',
            'Período Solicitado': anos_solicitados,
            'Período Disponível': anos_disponiveis,
            'Total Dividendos': f'R${total_dividendos:.2f}',
            'Média Dividendos': f'R${media_dividendos:.2f}',
            'Dividend Yield': f'R${dy_div:.2f}'
        })

# Cria o DataFrame com os dados coletados
df_ativos = pd.DataFrame(dados_ativos)

# Exibe o DataFrame
print(df_ativos)
```
Requisitos
Python 3.x
Bibliotecas: pandas, yfinance, datetime, os
Instalação
Clone o repositório:
```git clone https://github.com/SeuUsuario/nome-do-repositorio.git```
Instale as dependências:
```pip install -r requirements.txt```
Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.


# Part 2
Este projeto utiliza Flask para criar um servidor web que exibe dados financeiros em uma tabela HTML. O projeto também é configurado para ser implantado no Vercel para fácil acesso na web.

## Descrição

O objetivo deste projeto é coletar e exibir dados financeiros de ativos utilizando a biblioteca `yfinance`. A aplicação Flask lê esses dados, organiza-os em um DataFrame do pandas, e renderiza uma tabela HTML para visualização. 

## Funcionalidades

- Coleta de dividendos históricos de ativos financeiros.
- Cálculo de métricas financeiras usando modelos de precificação como Gordon e Bazin.
- Exibição dos dados em uma tabela HTML estilizada com Bootstrap.
- Implantação fácil no Vercel para acessibilidade online.

## Estrutura do Projeto
<br /> my-preco-teto/ 
<br />├── app.py
<br />├── ativos.csv
<br />├── templates/
<br />│ └── index.html
<br />└── vercel.json

- `app.py`: Contém o código do servidor Flask.
- `ativos.csv`: Arquivo CSV com os dados financeiros dos ativos.
- `templates/`: Diretório que contém os arquivos de template HTML.
- `vercel.json`: Arquivo de configuração para implantação no Vercel.

## Requisitos

- Python 3.x
- Flask
- pandas
- yfinance

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/my-preco-teto.git
    cd my-preco-teto
    ```

2. Crie um ambiente virtual e instale as dependências:
    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Execute o servidor Flask:
    ```sh
    flask run
    ```

    Ou, se estiver usando o `app.py` diretamente:
    ```sh
    python app.py
    ```

4. Acesse a aplicação em seu navegador:
    ```
    http://127.0.0.1:5000
    ```

## Configuração do Vercel

1. Instale o Vercel CLI:
    ```sh
    npm install -g vercel
    ```

2. Faça login no Vercel:
    ```sh
    vercel login
    ```

3. Faça o deploy:
    ```sh
    vercel
    ```

## Contribuição

1. Faça um fork do projeto.
2. Crie uma nova branch (`git checkout -b feature/nova-feature`).
3. Faça as suas alterações e commit (`git commit -am 'Adicionar nova feature'`).
4. Envie para o repositório remoto (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autor

Marcos Morais - [GitHub](https://github.com/marcosmoraisjr)
