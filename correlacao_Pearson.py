# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 14:56:21 2022

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
    
    Quando uma hipótesede aumento ou queda de uma variável está associado à
    evolução de outra variável, aplica-se o coeficiente de correlação de Pearson
    com o intervalo de -1 a 1. O valor 0 indica que não há correlação entre as 
    duas variáveis
"""


anos = 'JAN FEV MAR ABR MAI JUN JUL AGO SET OUT NOV DEZ'.split()
cab = ['POSTO', 'ANOS'] + anos


def leitura_vazao(end) -> pd.DataFrame:
    """Leitura do arquivo vazões.dat."""
    tab = pd.read_csv(end, sep='\s+', header = None )
    tab.columns = cab
    tab.set_index(['POSTO'], drop=True, inplace=True)
    return tab
    
end = Path(r'C:\Users\E805511\Downloads\vazoes 2022')
df_end = leitura_vazao(end)

teste_usinas = df_end.groupby("POSTO").get_group(74)

teste_usinas2 = df_end.groupby("POSTO").indices('POSTO' -> '74', '275')



#%% Manipulação dos dados

pivot2 = df_end.pivot_table(index = ['ANOS', 'POSTO'],
                            )
correlacao = df_end.corr(method='pearson')

#%% MANEIRAS DE ORGANIZAR AS INFORMAÇÃO
#Para separar por período do ano como abr/2022 a mar/2023
#E poder calcular o coeficiente de Pearson com as colunas geradas

# def reshape(inf, sup, data):
#     """Criando a própria função."""
#     return [float(i) for i in data.iloc[inf:sup,:].values]

# pd.DataFrame({'A': reshape(0,10, obs) ,'B': reshape(10,20, obs), 
#               'C': reshape(20,30, obs), 'D': reshape(30,40, obs)}, index = range(10))


# #Refatoração da função acima
# pd.DataFrame(obs.values.reshape(-1, 10).T, columns=['A','B', 'C', 'D'])




#%% PLOT

# sns.heatmap(correlacao,
#             cmap='ocean',
#             annot=True,
#             linewidths=0.5)

# #Definir x e y
#sns.scatterplot(data = df_end, x='name1', y='name2')


#%% FILTRANDO AS DATAS

# def filtro_datas():
#     """Filtragem por um intervalo de anos."""
#     #serie1 = df_end.query('ANOS==2020'&'POSTO==74')
#     #serie2 = df_end[(df_end['ANOS']=='2020')]
#     serie3 = df_end.query('ANOS=="2020"')
#     return serie3

# a = filtro_datas()

# def selecao_datas():
#     """Selecionando as datas."""
#     #filtro = (df_end['ANOS']>'2020') & (df_end['ANOS']<='2021')
#     #selecao = teste_usinas.loc[2002:2003]
#     #selecao1 = df_end["ANOS"].isin(pd.date_range(start='2020', end='2021'))
#     selecao2 = teste_usinas[teste_usinas.columns[3:12]]
#     #teste_usinas.loc[1:3, selecao2]
#     return selecao2


# a1 = selecao_datas()
#------------------------------------------------------------------------------

# %% CONSTRUIR UMA FUNÇÃO

def 
selecao1 = ~(df_end.loc[:, 'ANOS'] == 2022).values
selecao2 = ~(df_end.loc[:, 'ANOS'] == 1931).values

df_end_1 = deepcopy(df_end[selecao1])
df_end_2 = deepcopy(df_end[selecao2])

df_end_1.rename(columns={'ANOS': 'ANO_INI'}, inplace=True)
df_end_2.rename(columns={'ANOS': 'ANO_FIM'}, inplace=True)

# df_end_1.set_index('ANO_INI', append=True, inplace=True)
# df_end_2.set_index('ANO_FIM', append=True, inplace=True)

df_end_1.loc[:, 'JAN':'MAR'] = df_end_2.loc[:, 'JAN':'MAR']

# df_final = pd.concat([df_end_1, df_end_2], axis="columns")

anos_sel = deque(anos)
anos_sel.rotate(-3)
print(anos_sel)

df_final = df_end_1.loc[:, ['ANO_INI'] + list(anos_sel)]
df_final['ANO_INI'] = df_final['ANO_INI'].astype(str) + '-' + (df_final['ANO_INI'] + 1).astype(str)


#%%