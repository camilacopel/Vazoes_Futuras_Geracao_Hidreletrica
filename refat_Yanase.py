# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 17:31:15 2022

@author: E805511
"""

from pathlib import Path
import pandas as pd
import numpy as np




class VazoesCorr:
    """Correlação de Pearson."""
    
    def __init__(self, arquivo: Path):
        
        self._arquivo = arquivo
        self.ler_df_original()
        
        # self.correlacao()
        # self.df_corr_principais()
        
    
    def ler_df_original(self) -> pd.DataFrame:
        """Transforma o arquivo vazoes.txt em dataframe."""
        # Pela quantidade de linhas, o read_csv com delim_whitespace
        # tem melhor performance que o read_fwf com infer_nrows.
        df_orig = pd.read_csv(self._arquivo, header=None, delim_whitespace=True)
        df_orig.columns = ['posto', 'ano', *range(1, 13)]
        df_orig.set_index(['posto', 'ano'], inplace=True)
        df_orig.columns.name = 'mes'
        self.df_orig = df_orig
        
        #return df_orig
 
    
    def df_normaliza(self) -> pd.DataFrame:
        """Definir."""
        df_norm = self.df_orig

        df_norm = df_norm.stack().unstack('posto')
        
        # df_norm.index.name = 'mes'
        df_norm.index = pd.PeriodIndex(df_norm.index.get_level_values(level='ano').astype(str)
                          + '/'
                          + df_norm.index.get_level_values(level='mes').astype(str),
                          freq='M')
        
       
        # se todas as colunas são 0, muda para NaN
        df_norm.loc[(df_norm == 0).all(axis='columns')] = np.NaN
        # exclui as colunas com NaN
        df_norm.dropna(inplace=True)
        #self.df_normalizado = df_norm
          
        return df_norm
       
        # Trecho de 12 meses com o qual será calculada a correlação
        df_trecho = self.normaliza()
        df_trecho = df_trecho.loc[-12:]        
        return df_trecho
        
        
    def correlacao(self) -> pd.DataFrame:
        
        df_trecho = self.periodo_referencia()
        # Espalha o trecho por uma cópia do dataframe respeitando os meses
        df_other = self.normaliza.copy()
        
        for month in range(1, 13):
            df_other[df_other.index.month == month] = df_trecho[df_trecho.index.month == month].iloc[0]

        # Calcula a correlação
        df_corr = self._normaliza.rolling(12).corr(df_other)
        # Filtra os dados da correlação com o mês final
        df_corr = df_corr[df_corr.index.month == self.df_trecho.index.month[-1]]
        df_corr.index.name = 'mes_final'
        return df_corr
        
    
    def df_corr_principais(self) -> pd.DataFrame:
        # Separando os principais num outro dataframe
        df_corr_principais = self.df_corr[[6, 74, 169, 275]]
        return df_corr_principais
    
    
    def top_correlacao(self) -> pd.DataFrame:
        """_summary_

        Returns:
            pd.DataFrame: _description_
        """
        POSTO = 'POSTO'
        # 10 anos com maior correlação para este posto
        correlacao = self.correlacao()
        top_corr = correlacao[POSTO].sort_values(ascending=False).head(10)
        return top_corr
        
    
    def df_posto_escolhido(self, posto: int, POS_RANK_CORR=1) -> pd.DataFrame:
        """Definir.

        Args:
            posto (int): _description_
            POS_RANK_CORR (int, optional): _description_. Defaults to 1.

        Returns:
            pd.DataFrame: _description_
        """
        # Mês seguinte ao período escolhido
        mes_escolhido_ini = self.top_correlacao.index[POS_RANK_CORR] + pd.offsets.MonthEnd()
        # Trecho do período escolhido
        df_escolhido = self._normaliza.loc[mes_escolhido_ini:str(mes_escolhido_ini.year)]
        # Ajusta ano do periodo escolhido
        # Verifica o próximo mês a ser preenchido
        next_month = self._normaliza.index[-1] + pd.offsets.MonthEnd()
        # Calcula a diferença entre o próximo mês e o primeiro do período escolhido
        diff_months = next_month - df_escolhido.index[0]
        df_escolhido_ajust = df_escolhido.copy()
        df_escolhido_ajust.index = df_escolhido.index + diff_months
        return df_escolhido_ajust
    
    def df_original_modificado(self) -> pd.DataFrame:
        """Concatena com os dados originais."""
        df_norm = self._normaliza()
        df_escolhido_ajust = self.df_posto_escolhido()
        df_norm_modif = pd.concat([df_norm, df_escolhido_ajust])

        # Desnormaliza
        df_orig_modif = df_norm_modif.set_index([df_norm_modif.index.year, df_norm_modif.index.month])
        df_orig_modif.index.names = ['ano', 'mes']
        df_orig_modif = df_orig_modif.stack().unstack('mes').swaplevel()
        return df_orig_modif
         
if __name__ == '__main__':
    
    arquivo = Path('C:/Users/E805511/Downloads/VAZOES-AVG.txt')
    vazoes = VazoesCorr(arquivo)
    
    # a = vazoes.df_original()
    b = vazoes.df_normaliza()
