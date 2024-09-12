
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 14:56:21 2022.

@author: E805511

ESTATÍSTICA DESCRITIVA


"""

import pandas as pd
import numpy as np
from pathlib import Path
from copy import deepcopy
from collections import deque



#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

MESES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
USINAS_PRINCIPAIS = ('FURNAS', 'GBM','SOBRADINHO', 'TUCURUÍ' )

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        
def leitura_vazao(end: Path) -> pd.DataFrame:
    """Leitura do arquivo vazões.dat."""
    tab = pd.read_csv(end, sep='\s+', header = None )
    cab = ['POSTO', 'ANOS'] + MESES
    tab.columns = cab
    tab.set_index(['POSTO'], drop=True, inplace=True)
    return tab
    

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# %% GERANDO TABELA AUXILIAR
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

def reordenando_dados(mes: int) -> pd.DataFrame :
    """Versionamento dos dados.
    
    mes = mês que finaliza a previsão da Refinitiv
    
    Seleciona em qual mês inicia, realocando os meses anteriores.
    No caso, inicia em Abril...
    """
    #--------------------------------------------------------------
    #Seleciona o primeiro e o último ano
    #Retorno em bool. '~ inverte True em False e vice-versa
    selecao1 = ~(df_vazao_original.loc[:, 'ANOS'] == 2023).values
    selecao2 = ~(df_vazao_original.loc[:, 'ANOS'] == 1931).values
    #--------------------------------------------------------------
    #Separando o arquivo em dois
    df_end_1 = deepcopy(df_vazao_original[selecao1])
    df_end_2 = deepcopy(df_vazao_original[selecao2])
    #--------------------------------------------------------------
    #Renomeação da coluna
    df_end_2.rename(columns={'ANOS': 'ANO_FIM'}, inplace=True)
    #--------------------------------------------------------------
    #Seleciona em qual mês inicia, realocando os meses
    #Une os DataFrames
    df_end_1.loc[:, 1:mes] = df_end_2.loc[:, 1:mes]
    
    return df_end_1

def reordenando_cabecalho_meses(mes: int) -> list:
    """Para modificação do nome das colunas relacionada aos meses.
    
    Seleção da como começam a tabela atráves da biblioteca collections,
    classe deque.
    -------------------
    Exemplo:
    com o rotate=0
    imprime: deque([ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    
    Com rotate = -3
    imprime: deque([4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3])
    equivalente: deque(['ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET',
                        'OUT', 'NOV', 'DEZ', 'JAN', 'FEV', 'MAR'])
    ------------------
    """
    meses_reordenandos = deque(MESES)
    meses_reordenandos.rotate(- mes)
    print(meses_reordenandos)
    return meses_reordenandos

def tabela_auxiliar(mes:int) -> pd.DataFrame : 
    """Digitar depois."""
    mes = mes_previsao
    #--------------------------------------------------------------------------
    #Tabela organizada
    meses_reordenando = reordenando_cabecalho_meses(mes)
    dados = reordenando_dados(mes)
    #--------------------------------------------------------------------------
    df_tabela_aux = dados.loc[:, ['ANOS'] + list(meses_reordenando)]
    df_tabela_aux['ANOS'] = df_tabela_aux['ANOS'].astype(str) + '-' + (df_tabela_aux['ANOS'] + 1).astype(str)
    #--------------------------------------------------------------------------
    return df_tabela_aux
    
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#%% SELEÇÃO DA USINA
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

def selecione_usina(cod:int) -> pd.DataFrame:
    """Digite o código da usina.
    
    Código das maiores usinas de cada submercado de energia.
    """
    dados_usinas_selecionada = tabela_aux.groupby("POSTO").get_group(cod)
    if cod == 6:
        print(USINAS_PRINCIPAIS[0])
    elif cod == 74:
        print(USINAS_PRINCIPAIS[1])
    elif cod == 169:
        print(USINAS_PRINCIPAIS[2])
    elif cod == 275:
        print(USINAS_PRINCIPAIS[3])
    else:
        print('Escolha entre as usinas cod:[6, 74, 169, 275]')
    
    return dados_usinas_selecionada


#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# %% CÁLCULO FABIANO
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

def series_anos():
    """Escrever depois."""
    #-----------------------------------------------------------
    #Seleção da coluna com os anos da tabela auxiliar
    series_anos = usina_sel['ANOS']
    series_anos.reset_index(drop=True, inplace=True)
    #-----------------------------------------------------------
    usina_sel.set_index('ANOS', inplace=True)
    #-----------------------------------------------------------
    return series_anos

    
def correlacao():
    r"""Milhões de coisa em uma função.
    
    .. math:: R_{ij}=\frac{ C_{ij} }{ \\sqrt{ C_{ii} * C_{jj}}}
    
    The values of `R` are between -1 and 1, inclusive.
    """
    #--------------------------------------------------------------------------
    #função é usada para acessar a última linha do dataframe
    #x = np.array(usina_sel.tail(1))
    x1 = np.array(usina_sel.iloc[-2, :])
    #--------------------------------------------------------------------------
    #Cálculo correlação
    correlacao = np.corrcoef(x=x1, y=usina_sel)[1: -2, 0]
    #--------------------------------------------------------------------------
    return correlacao

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#%% Preenchimento
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

def periodo_da_correlacao():
    """descrever.
    
    imprime: período da correlação: 2001-2002
    Usando as saídas das funções series_anos e resultado_correlação
    """
    # Preenchimento
    #--------------------------------------------------------------------------
    #
    ano_escolhido = series_anos[resultado_correlacao.argmax()]
    print(f'período da correlação: {ano_escolhido}')
    #--------------------------------------------------------------------------
    #
    ano_preenchimento = series_anos[resultado_correlacao.argmax()+1]
    #--------------------------------------------------------------------------

    return ano_preenchimento


def não_sei():
    """Imagine descrever o que eu não sei."""    
    #--------------------------------------------------------------------------
    teste = tabela_aux.groupby("ANOS").get_group(ano_preenchimento)
    #--------------------------------------------------------------------------
    # #Selecionando até Dezembro
    # Até o memento as previsões 
    teste = teste.loc[:, :12]
    
    return teste


def inserindo_resuldado_correlacao(mes:int)-> pd.DataFrame:
    """Retorna um DataFrame preenchido com as previsões."""
    #--------------------------------------------------------------------------
    #
    criterio_selecao = df_vazao_original.loc[:, 'ANOS'] == 2023
    #--------------------------------------------------------------------------
    #
    df_vazao_original.loc[criterio_selecao, mes+1:12] = teste
    #--------------------------------------------------------------------------
    #
    df_final_previsoes = df_vazao_original
    #--------------------------------------------------------------------------
    return df_final_previsoes

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# %%Exportar para texto ou CSV
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


def converter_to_txt():
    """Retorna o arquivo no formato original do vazoes.dat.
    
    Para as simulações no Rolling Horizon.
    """
    lista_linhas = list()
    
    for idx, row in df_final_previsoes.iterrows():
        lista_linhas.append(f"{idx:3} {row['ANOS']:4}"
                            f"{row[1]:6}{row[2]:6}{row[3]:6}"
                            f"{row[4]:6}{row[5]:6}{row[6]:6}"
                            f"{row[7]:6}{row[8]:6}{row[9]:6}"
                            f"{row[10]:6}{row[11]:6}{row[12]:6}")

    tudo = '\n'.join(lista_linhas)
    nome_novo_arquivo = 'vazoes_AVG_TUCURUÍ.txt'
    
    with open(nome_novo_arquivo, 'w') as file:
        file.write(tudo)

     
    

def converter_to_csv():
    """Retorna o arquivo em csv com as alterações e acrescimos dos cenários de previsão.
    
    Para aplicação em Excel ou uso em Power BI.
    
    USINAS_PRINCIPAIS = ('FURNAS', 'GBM', 'SOBRADINHO', 'TUCURUÍ', )
    """
    df_final_previsoes.to_csv(r'C:/Users/E805511/Downloads/vazoes_SOBRADINHO.csv',
                              header= None, 
                              index=True, 
                              sep=';',
                              mode='w',
                              encoding='utf-8')


#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
def main():
    """Descrever."""
    pass
   

#------------------------------------------------------------------------------
#Parâmetros
caminho = Path("C:/Users/E805511/Downloads/VAZOES-P75.txt")
cod = 6
mes_previsao = 4
#------------------------------------------------------------------------------

#df_vazao_original = leitura_vazao(caminho)
    
#tabela_aux = tabela_auxiliar(mes=mes_previsao)

usina_sel = selecione_usina(cod=cod)

series_anos = series_anos()

resultado_correlacao = correlacao()

ano_preenchimento = periodo_da_correlacao()

teste = não_sei()

df_final_previsoes = inserindo_resuldado_correlacao(mes_previsao)

#converter_to_txt()


#%%
#mes_previsao = input(f'Digito do mês que termina a previsão da Refinitiv: ')
# saida_pandas_string = df_final_previsoes.to_string(r'C:/Users/E805511/Downloads/vazoes_teste_sob.csv',
#                                      index=True,
#                                      header=None,
                                     
#                                      