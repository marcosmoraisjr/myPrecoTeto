# Importando Biblitecas
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import os
import warnings
import os
from termcolor import colored  # Para cores no terminal
from alive_progress import alive_bar

# Ignora as mensagens de aviso
warnings.filterwarnings('ignore')

# Definindo Funções


def limpa_tela():
    """
    Limpa a tela do terminal.

    Dependendo do sistema operacional, utiliza o comando apropriado para limpar a tela.
    """
    # Verifica o sistema operacional e executa o comando correspondente para limpar a tela
    comando_limpeza = 'cls' if os.name == 'nt' else 'clear'
    os.system(comando_limpeza)


def criar_ativos():
    conteudo = """ATENÇÃO: SE O TICKER FOR DO BRASIL ACRESCENTAR .SA E NÃO ESQUECER DE INFORMAR O TIPO (FII/AÇÃO)
KNCR11.SA;FII
GARE11.SA;FII
NEWL11.SA;FII
RZTR11.SA;FII
CPTS11.SA;FII
PORD11.SA;FII
MXRF11.SA;FII
VGHF11.SA;FII
BBSE3.SA;AÇÃO
TAEE3.SA;AÇÃO
KLBN4.SA;AÇÃO
ITSA3.SA;AÇÃO
BBDC4.SA;AÇÃO
"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'ativos.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(conteudo)
    print(f"Arquivo ativos.txt criado em: {file_path}")
    input("Pressione Enter para continuar...")


def ler_ativos():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'ativos.txt')
    if not os.path.exists(file_path):
        criar_ativos()

    tickers = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for linha in file:
            if not linha.startswith("ATENÇÃO") and linha.strip():
                ticker = linha.split(';')[0].strip()
                tickers.append(ticker)
    return tickers


def coleta_dividendos(ticker):
    """
    Coleta o histórico de dividendos de um ativo e calcula o total de dividendos por ano.

    Parâmetros:
    ticker (str): O símbolo do ativo.

    Retorna:
    Series ou None: Uma série com o total de dividendos por ano. Retorna None se não houver dados de dividendos.
    """
    # Obtém o objeto do ativo usando o yfinance
    ativo = yf.Ticker(ticker)

    # Coleta o histórico de dividendos e reseta o índice para ter uma coluna 'Date'
    historico_dividendos = ativo.dividends.reset_index()

    # Verifica se o histórico de dividendos está vazio
    if historico_dividendos.empty:
        return None

    # Extrai o ano da coluna 'Date' e cria uma nova coluna 'year'
    historico_dividendos['year'] = historico_dividendos['Date'].dt.year

    # Agrupa os dividendos por ano e calcula a soma dos dividendos para cada ano
    dividendos_por_ano = historico_dividendos.groupby('year')[
        'Dividends'].sum()

    return dividendos_por_ano


def calcula_dividendos(dividendos_ano, anos=5):
    """
    Calcula o total e a média dos dividendos para um número específico de anos.

    Parâmetros:
    dividendos_ano (Series): Série com dividendos anuais, com o ano como índice.
    anos (int): Número de anos a serem considerados no cálculo. Padrão é 5 anos.

    Retorna:
    tuple: Um tuplo contendo:
        - Total de dividendos acumulados nos anos considerados.
        - Média anual de dividendos.
        - Número de anos com dados disponíveis.
    """
    # Obtém o ano atual
    ano_atual = datetime.datetime.now().year
    # Define o ano de início para o cálculo
    ano_inicio = ano_atual - anos

    # Filtra os dividendos para o intervalo de anos desejado
    dividendos_filtrados = dividendos_ano[(
        dividendos_ano.index >= ano_inicio) & (dividendos_ano.index < ano_atual)]
    anos_disponiveis = len(dividendos_filtrados)

    if anos_disponiveis == 0:
        # Retorna 0 para todos os valores se não houver dados disponíveis
        return 0, 0, 0

    # Calcula o total e a média dos dividendos
    total_dividendos = dividendos_filtrados.sum()
    media_dividendos = total_dividendos / anos_disponiveis

    return total_dividendos, media_dividendos, anos_disponiveis


def modelo_gordon(dividendo, taxa_retorno=0.06, taxa_crescimento=0.005):
    """
    Calcula o preço justo de uma ação ou FII usando o modelo de Gordon.

    Parâmetros:
    dividendo (float): O valor do dividendo anual do ativo.
    taxa_retorno (float): A taxa de retorno esperada. Padrão é 0.06 (6%).
    taxa_crescimento (float): A taxa de crescimento dos dividendos esperada. Padrão é 0.005 (0.5%).

    Retorna:
    float: O preço justo do ativo com base no modelo de Gordon.
    """
    # Calcula o preço justo dividindo o dividendo pela diferença entre a taxa de retorno e a taxa de crescimento
    return dividendo / (taxa_retorno - taxa_crescimento)


def modelo_bazin(dividendo, taxa_retorno=0.06):
    """
    Calcula o preço justo de uma ação ou FII usando o modelo de Bazin.

    Parâmetros:
    dividendo (float): O valor do dividendo anual do ativo.
    taxa_retorno (float): A taxa de retorno esperada. Padrão é 0.06 (6%).

    Retorna:
    float: O preço justo do ativo com base no modelo de Bazin.
    """
    # Calcula o preço justo dividindo o dividendo pela taxa de retorno esperada
    return dividendo / taxa_retorno


def obter_dados(ticker):
    """
    Obtém dados financeiros de um ativo a partir do Yahoo Finance.

    Parâmetros:
    ticker (str): O símbolo do ativo.

    Retorna:
    dict: Um dicionário contendo o ticker e informações financeiras do ativo.
    """
    try:
        # Obtém as informações do ativo usando o yfinance
        ativo = yf.Ticker(ticker)
        informacoes = ativo.info

        # Retorna um dicionário com os dados financeiros do ativo
        return {
            'Ticker': ticker,
            'Preço Atual': informacoes.get('currentPrice', 'N/A'),
            'Fechamento Anterior': informacoes.get('regularMarketPreviousClose', 'N/A'),
            'Dividend Yield': informacoes.get('dividendYield', 'N/A'),
            # Exemplo de outro dado, ajuste conforme necessário
            'P/L': informacoes.get('forwardEps', 'N/A')
        }
    except Exception as e:
        # Em caso de erro, retorna um dicionário com o ticker e a mensagem de erro
        return {'Ticker': ticker, 'Erro': str(e)}


def verificar_tipo(ticker):
    """
    Verifica o tipo de ativo (Ação ou FII) com base na descrição do ativo no Yahoo Finance.

    Parâmetros:
    ticker (str): O símbolo do ativo.

    Retorna:
    str: 'FII' se o ativo for um Fundo de Investimento Imobiliário,
         'Ação' se for uma ação comum,
         'Informação indisponível' se a informação não estiver disponível.
    """

    # Obtém as informações do ativo usando o yfinance
    ativo = yf.Ticker(ticker)
    informacoes = ativo.info

    # Verifica se a descrição detalhada do negócio está disponível
    if 'longBusinessSummary' in informacoes:
        descricao = informacoes['longBusinessSummary'].lower()

        # Verifica se a descrição contém palavras-chave relacionadas a FIIs
        if 'real estate' in descricao or 'reit' in descricao:
            return 'FII'
        else:
            return 'Ação'
    else:
        # Retorna uma mensagem padrão se a descrição não estiver disponível
        return 'Informação indisponível'
# Gráficos


def plot_dividends(ticker, dividendos, periodo):
    """
    Plota os dividendos anuais de um determinado ticker para os últimos 'periodo' anos.

    Parâmetros:
    ticker (str): O símbolo do ativo.
    dividendos (DataFrame): DataFrame contendo os dividendos com índice de anos.
    periodo (int): Número de anos a serem considerados na plotagem.
    """

    # Obtém o ano atual
    ano_atual = datetime.datetime.now().year

    # Filtra e agrupa os dividendos pelos últimos 'periodo' anos, somando os valores por ano
    dividendos_ultimos_anos = dividendos[dividendos.index >=
                                         ano_atual - periodo].groupby(level=0).sum()

    # Configura o tamanho da figura do gráfico
    plt.figure(figsize=(12, 6))

    # Define um colormap para as barras do gráfico
    paleta_cores = plt.cm.get_cmap('tab10', len(dividendos_ultimos_anos))

    # Plotagem das barras com cores diferentes para cada ano, sendo o ano atual em preto
    for i, (ano, valor) in enumerate(dividendos_ultimos_anos.items()):
        if ano == ano_atual:
            plt.bar(ano, valor, color='black')  # Ano atual em preto
        else:
            # Outros anos com cores da paleta
            plt.bar(ano, valor, color=paleta_cores(i))
        # Adiciona o valor do dividendo acima de cada barra
        plt.text(ano, valor, f'{valor:.2f}', ha='center', va='bottom')

    # Define o título e os rótulos dos eixos do gráfico
    plt.title(f'Dividendos Anuais de {
              ticker} (últimos {periodo} anos - ano atual)')
    plt.xlabel('Anos')
    plt.ylabel('Dividendos por Ano')

    # Adiciona uma grade ao gráfico
    plt.grid(True)

    # Mostra o gráfico
    plt.show()


def plot_cotacoes(ticker, periodo):
    # Baixe os dados de cotações de um período longo
    # Baixa dados dos últimos 5 anos para exemplo
    dados = yf.download(ticker, period='5y')

    # Obtém o ano atual
    ano_atual = datetime.datetime.now().year

    # Filtra os dados pelos últimos 'periodo' anos
    dados_ultimos_anos = dados[dados.index.year >= ano_atual - periodo]

    # Verifique se os dados foram filtrados corretamente
    if dados_ultimos_anos.empty:
        print("Nenhum dado encontrado para o período especificado.")
    else:
        # Encontre as cotações máxima e mínima no período filtrado
        max_price = dados_ultimos_anos['Close'].max()
        min_price = dados_ultimos_anos['Close'].min()

        # Crie o gráfico
        plt.figure(figsize=(12, 6))
        plt.plot(dados_ultimos_anos['Close'],
                 label='Cotação Fechamento', color='blue')

        # Adicione linhas horizontais na maior e menor cotação
        plt.axhline(y=max_price, color='green', linestyle='--',
                    label=f'Máxima: {max_price:.2f}')
        plt.axhline(y=min_price, color='red', linestyle='--',
                    label=f'Mínima: {min_price:.2f}')

        # Adicione título e rótulos
        plt.title(f'Gráfico de Cotações de {
                  ticker} (Últimos {periodo} ano(s))')
        plt.xlabel('Data')
        plt.ylabel('Cotação de Fechamento')
        plt.legend()

        # Exiba o gráfico
        plt.show()


def principal():
    tickers = ler_ativos()

    # Parâmetros de entrada
  # Solicitação dos parâmetros de entrada ao usuário
    tra = input("Digite a taxa de retorno para ações (padrão 0.08)...: ")
    tra = float(tra) if tra else 0.08
    trf = input("Digite a taxa de retorno para FIIs (padrão 0.10)....: ")
    trf = float(trf) if trf else 0.10
    taxa_retorno = (tra, trf)
    taxa_crescimento = input(
        "Digite a taxa de crescimento (padrão 0.005).........: ")
    taxa_crescimento = float(taxa_crescimento) if taxa_crescimento else 0.005
    anos_solicitados = input(
        "Digite o número de anos solicitados (padrão 5)......: ")
    anos_solicitados = int(anos_solicitados) if anos_solicitados else 5

    # Criação de uma lista para armazenar os dados de todos os tickers
    dados_ativos = []

    # Processa cada ticker
    with alive_bar(len(tickers), title="Analisando Tickers") as bar:
        for ticker in tickers:

            dividendos = coleta_dividendos(ticker)

            if dividendos is not None:
                tipo_ativo = verificar_tipo(ticker)
                ativo = yf.Ticker(ticker)
                total_dividendos, media_dividendos, anos_disponiveis = calcula_dividendos(
                    dividendos, anos_solicitados)
                cotacao_atual = ativo.info.get('currentPrice', 0)
                dy_div = ativo.info.get('dividendYield', 0) * cotacao_atual

                gordon = modelo_gordon(
                    media_dividendos, taxa_retorno[0], taxa_crescimento)
                bazin = modelo_bazin(media_dividendos, taxa_retorno[1])

                recomendacao_gordon = '🟢' if cotacao_atual < gordon else '🔴'
                recomendacao_bazin = '🟢' if cotacao_atual < bazin else '🔴'
                retorno = taxa_retorno[0] if tipo_ativo == 'Ação' else taxa_retorno[1]

                dados_ativos.append({
                    'Data': f'{datetime.datetime.now()}',
                    'Ticker': ticker,
                    'Tipo': tipo_ativo,
                    'Preço Atual': f'R${cotacao_atual:.2f}',
                    'Preço Teto (Bazin)': f'R$ {bazin:.2f}{recomendacao_bazin}',
                    'Preço Teto (Gordon)': f'R$ {gordon:.2f}{recomendacao_gordon}',
                    'Margem Bazin': f'R${bazin - cotacao_atual:.2f}',
                    'Margem Gordon': f'R${gordon - cotacao_atual:.2f}',
                    # 'Recomendação Gordon': recomendacao_gordon,
                    # 'Recomendação Bazin': recomendacao_bazin,
                    'Taxa de Retorno': f'{retorno*100:.2f}%',
                    'Taxa de Crescimento': f'{taxa_crescimento * 100:.2f}%',
                    'Período Solicitado': anos_solicitados,
                    'Período Disponível': anos_disponiveis,
                    'Total Dividendos': f'R$ {total_dividendos:.2f}',
                    'Média Dividendos': f'R$ {media_dividendos:.2f}',
                    'Dividend Yield': f'R$ {dy_div:.2f}'
                })
                bar()
    print("Processo concluído!")

    # Cria o DataFrame com os dados coletados
    df_ativos = pd.DataFrame(dados_ativos)

    # Ajusta as opções de exibição do Pandas
    pd.set_option('display.max_columns', None)  # Exibe todas as colunas
    # Não quebra linhas para exibir DataFrames
    pd.set_option('display.expand_frame_repr', False)

    # Exibe o DataFrame em formato HTML para melhor visualização no Google Colab
    from IPython.display import display
    display(df_ativos)

    # Exportar os Dados para um Arquivo CSV:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'ativosanalisados.csv')
    df_ativos.to_csv(file_path, index=False)


if __name__ == "__main__":

    tickers = ler_ativos()

    # Parâmetros de entrada
    taxa_retorno = (0.08, 0.10)
    taxa_crescimento = 0.005
    anos_solicitados = 5

    # Criação de uma lista para armazenar os dados de todos os tickers
    dados_ativos = []

    # Processa cada ticker
    with alive_bar(len(tickers), title="Analisando Tickers") as bar:
        for ticker in tickers:

            dividendos = coleta_dividendos(ticker)

            if dividendos is not None:
                tipo_ativo = verificar_tipo(ticker)
                ativo = yf.Ticker(ticker)
                total_dividendos, media_dividendos, anos_disponiveis = calcula_dividendos(
                    dividendos, anos_solicitados)
                cotacao_atual = ativo.info.get('currentPrice', 0)
                dy_div = ativo.info.get('dividendYield', 0) * cotacao_atual

                gordon = modelo_gordon(
                    media_dividendos, taxa_retorno[0], taxa_crescimento)
                bazin = modelo_bazin(media_dividendos, taxa_retorno[1])

                recomendacao_gordon = '🟢' if cotacao_atual < gordon else '🔴'
                recomendacao_bazin = '🟢' if cotacao_atual < bazin else '🔴'
                retorno = taxa_retorno[0] if tipo_ativo == 'Ação' else taxa_retorno[1]

                dados_ativos.append({
                    'Data': f'{datetime.datetime.now()}',
                    'Ticker': ticker,
                    'Tipo': tipo_ativo,
                    'Preço Atual': f'R${cotacao_atual:.2f}',
                    'Preço Teto (Bazin)': f'R$ {bazin:.2f}{recomendacao_bazin}',
                    'Preço Teto (Gordon)': f'R$ {gordon:.2f}{recomendacao_gordon}',
                    'Margem Bazin': f'R${bazin - cotacao_atual:.2f}',
                    'Margem Gordon': f'R${gordon - cotacao_atual:.2f}',
                    # 'Recomendação Gordon': recomendacao_gordon,
                    # 'Recomendação Bazin': recomendacao_bazin,
                    'Taxa de Retorno': f'{retorno*100:.2f}%',
                    'Taxa de Crescimento': f'{taxa_crescimento * 100:.2f}%',
                    'Período Solicitado': anos_solicitados,
                    'Período Disponível': anos_disponiveis,
                    'Total Dividendos': f'R$ {total_dividendos:.2f}',
                    'Média Dividendos': f'R$ {media_dividendos:.2f}',
                    'Dividend Yield': f'R$ {dy_div:.2f}'
                })
                bar()
    print("Processo concluído!")

    # Cria o DataFrame com os dados coletados
    df_ativos = pd.DataFrame(dados_ativos)

    # Ajusta as opções de exibição do Pandas
    pd.set_option('display.max_columns', None)  # Exibe todas as colunas
    # Não quebra linhas para exibir DataFrames
    pd.set_option('display.expand_frame_repr', False)

    # Exibe o DataFrame em formato HTML para melhor visualização no Google Colab
    from IPython.display import display
    display(df_ativos)

    # Exportar os Dados para um Arquivo CSV:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'ativosanalisados.csv')
    df_ativos.to_csv(file_path, index=False)