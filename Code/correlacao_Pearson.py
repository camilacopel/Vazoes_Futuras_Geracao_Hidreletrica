
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 14:56:21 2022.

@author: E805511
"""

import pandas as pd
import numpy as np
from pathlib import Path
import seaborn as sns
from copy import deepcopy
from collections import deque

#%%
"""
ESTA´TISTICA DESCRITIVA

CORRELAÇÃO DE PEARSON:
    
    Quando uma hipótese de aumento ou queda de uma variável está associado à
    evolução de outra variável, aplica-se o coeficiente de correlação de Pearson
    com o intervalo de -1 a 1. O valor 0 indica que não há correlação entre as 
    duas variáveis
"""


meses = 'JAN FEV MAR ABR MAI JUN JUL AGO SET OUT NOV DEZ'.split()



def leitura_vazao(end) -> pd.DataFrame:
    """Leitura do arquivo vazões.dat."""
    tab = pd.read_csv(end, sep='\s+', header = None )
    cab = ['POSTO', 'ANOS'] + meses
    tab.columns = cab
    tab.set_index(['POSTO'], drop=True, inplace=True)
    return tab
    
end = Path(r'C:\Users\E805511\Downloads\vazoes 2022')
df_end = leitura_vazao(end)


#%% Manipulação dos dados

pivot2 = df_end.pivot_table(index = ['ANOS', 'POSTO'],
                            )
correlacao = df_end.corr(method='pearson')

#------------------------------------------------------------------------------

# %% 


def organizando_dados():
    """Digitar depois..."""
    #--------------------------------------------------------------
    selecao1 = ~(df_end.loc[:, 'ANOS'] == 2022).values
    selecao2 = ~(df_end.loc[:, 'ANOS'] == 1931).values
    #--------------------------------------------------------------
    df_end_1 = deepcopy(df_end[selecao1])
    df_end_2 = deepcopy(df_end[selecao2])
    #--------------------------------------------------------------
    df_end_1.rename(columns={'ANOS': 'ANO_INI'}, inplace=True)
    df_end_2.rename(columns={'ANOS': 'ANO_FIM'}, inplace=True)
    #--------------------------------------------------------------
    #Seleciona em qual mês inicia, realocando os meses anteriores
    #No caso, inicia em Abril
    df_end_1.loc[:, 'JAN':'MAR'] = df_end_2.loc[:, 'JAN':'MAR']
    
    return df_end_1

def organizando_colunas():
    """Para modificação do nome das colunas relacionada aos meses.
    Seleção da como começam a tabela atráves da biblioteca collections,
    classe deque.
    -------------------
    Exemplo:
    com o rotate=0
    imprime: deque(['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN',
                    'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'])
    
    com rotate= -3
    imprime: deque(['ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET',
                    'OUT', 'NOV', 'DEZ', 'JAN', 'FEV', 'MAR'])
    ------------------
    """
    anos_sel = deque(meses)
    anos_sel.rotate(-3)
    print(anos_sel)
    return anos_sel

anos_sel = organizando_colunas()
dados = organizando_dados()


df_final = dados.loc[:, ['ANO_INI'] + list(anos_sel)]
df_final['ANO_INI'] = df_final['ANO_INI'].astype(str) + '-' + (df_final['ANO_INI'] + 1).astype(str)
#df_final['ANO_INI'].astype(str)


#%% CORRELAÇÃO

teste_usinas = df_final.groupby("POSTO").get_group(74)
correlacao = teste_usinas.corr(method='pearson')

sns.heatmap(correlacao,
            cmap='ocean',
            annot=True,
            linewidths=0.5)

#%% SELECIONAR UMA OU MúlTIPLAS USINAS
# Código das maiores usinas de cada submercado de energia
#BUILDING A FUNCTION 

def selecione_usina(cod:int) -> pd.DataFrame:
    """Digite o código da usina."""
    teste_usinas = df_final.groupby("POSTO").get_group(cod)
    return teste_usinas

#------------------------------------------------------------------------------
def selecionar_multi_usinas(usinas: list):
    """
    Digite o código das usinas em uma lista.
    
    Exemplo:
       iusi = selecionar_multi_usinas([6, 74, 169, 275])
    """
    lista_usinas = usinas
    usinas_selec = df_final[df_final.index.isin(lista_usinas)]
    return usinas_selec

b = selecione_usina(6)
c = selecionar_multi_usinas([6, 74, 169, 275])

#%% CRIAR NOVA LINHA

# nova linha: 2022-2023 com os dados do comparativo da correlação
# para todas as usinas

# =============================================================================
# 
# =============================================================================
