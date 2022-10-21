# -*- coding: utf-8 -*-
"""
Ajuste de um arquivos de vazoes.txt preenchendo os valores que estavam zerados
até o final do ano, com dados históricos do período em que há uma maior
correlação com os últimos 12 meses preenchidos (!= 0) para uma determinada
usina.

Tudo rodado de maneira sequencial, será transformado em classe com métodos.
"""

from pathlib import Path

import pandas as pd
import numpy as np

# Leitura do arquivo
arquivo = Path('C:/Users/E805511/Downloads/VAZOES-AVG.txt')


# Transformação em dataframe.
# Pela quantidade de linhas, o read_csv com delim_whitespace
# tem melhor performance que o read_fwf com infer_nrows.
df_orig = pd.read_csv(arquivo, header=None, delim_whitespace=True)
df_orig.columns = ['posto', 'ano', *range(1, 13)]
df_orig.set_index(['posto', 'ano'], inplace=True)
df_orig.columns.name = 'mes'

# Empilha os meses e desempilha o posto
df_norm = df_orig.stack().unstack('posto')

# Transforma os indexes ano e mes em um index só que representa ambas
# as informações de uma melhor forma. O nome do index continua sendo 'mes'
df_norm.index = pd.PeriodIndex(df_norm.index.get_level_values('ano').astype(str)
                          + '/'
                          + df_norm.index.get_level_values('mes').astype(str),
                          freq='M')
df_norm.index.name = 'mes'

# se todas as colunas são 0, muda para NaN
df_norm.loc[(df_norm == 0).all(axis='columns')] = np.NaN
# exclui as colunas com NaN
df_norm.dropna(inplace=True)

# Trecho de 12 meses com o qual será calculada a correlação
df_trecho = df_norm.iloc[-12:]
# Espalha o trecho por uma cópia do dataframe respeitando os meses
df_other = df_norm.copy()
for month in range(1, 13):
    df_other[df_other.index.month == month] = df_trecho[df_trecho.index.month == month].iloc[0]

# Calcula a correlação
df_corr = df_norm.rolling(12).corr(df_other)
# Filtra os dados da correlação com o mês final
df_corr = df_corr[df_corr.index.month == df_trecho.index.month[-1]]
df_corr.index.name = 'mes_final'
# Separando os principais num outro dataframe
df_corr_principais = df_corr[[6, 74, 169, 275]]

# Escolhe um periodo
POS_RANK_CORR = 1
POSTO = 275
# 10 anos com maior correlação para este posto
top_corr = df_corr[POSTO].sort_values(ascending=False).head(10)

# Mês seguinte ao período escolhido
mes_escolhido_ini = top_corr.index[POS_RANK_CORR] + pd.offsets.MonthEnd()
# Trecho do período escolhido
df_escolhido = df_norm.loc[mes_escolhido_ini:str(mes_escolhido_ini.year)]
# Ajusta ano do periodo escolhido
# Verifica o próximo mês a ser preenchido
next_month = df_norm.index[-1] + pd.offsets.MonthEnd()
# Calcula a diferença entre o próximo mês e o primeiro do período escolhido
diff_months = next_month - df_escolhido.index[0]
df_escolhido_ajust = df_escolhido.copy()
df_escolhido_ajust.index = df_escolhido.index + diff_months

# Concatena com os dados originais
df_norm_modif = pd.concat([df_norm, df_escolhido_ajust])

# Desnormaliza
df_orig_modif = df_norm_modif.set_index([df_norm_modif.index.year, df_norm_modif.index.month])
df_orig_modif.index.names = ['ano', 'mes']
df_orig_modif = df_orig_modif.stack().unstack('mes').swaplevel()
