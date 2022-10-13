
# Verificar se o arquivo existe
# Método Try

from copy import deepcopy
from pathlib import Path
import os.path
import pandas as pd
import numpy as np
from collections import deque


MESES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
USINAS_PRINCIPAIS = ('FURNAS', 'GBM','SOBRADINHO', 'TUCURUÍ' )
POSTOS_ = {
    '6': 'FURNAS',
    '74': 'GBM',
    '169': 'SOBRADINHO',
    '275': 'TUCURUÍ'
}

class Vazoes:
    """
    Parâmetros de entrada:
        path (Path): caminho do arquivo
        mes (int): mês que se encerra as previsões da Refinitiv
        posto (int): Número do posto da usina de acordo com arquivo confhd
     
    ------
    Retorna:    
    """
    def __init__(self,
                 caminho_arquivo,
                 mes_referencia,
                 posto):
       
        self.path = Path(caminho_arquivo)
        self.mes_referencia = int(mes_referencia)
        self.posto = int(posto)
        self.df_vazoes = None
        self.df_final = None
        
        
    def leitura_vazao(self, arquivo: Path) -> pd.DataFrame:  # type: ignore
        """Leitura do arquivo vazões.dat."""
        
        
        df_vazoes = pd.read_csv(arquivo, sep='\s+', header=None )
        cab = ['POSTO', 'ANOS'] + MESES
        df_vazoes.columns = cab
        df_vazoes.set_index(['POSTO'], drop=True, inplace=True)
        self.df_vazoes = df_vazoes
        
        try:
            with open('vazoes', 'r') as f:
                verificar_arquivo(f)  # type: ignore
        
        except IOError:
            print ('Arquivo não encontrado!')  
        
        return df_vazoes
    
    def reordenando_dados(self) -> pd.DataFrame :
        """
        Versionamento dos dados.
        
        mes = mês que finaliza a previsão da Refinitiv
        
        Seleciona em qual mês inicia, realocando os meses anteriores.
        No caso, inicia em Abril...
        """
        df_vazoes = Vazoes.leitura_vazao(arquivo)  # type: ignore
        #--------------------------------------------------------------
        #Seleciona o primeiro e o último ano
        #Retorno em bool. '~ inverte True em False e vice-versa
        selecao1 = ~(df_vazoes.loc[:, 'ANOS'] == 2023).values
        selecao2 = ~(df_vazoes.loc[:, 'ANOS'] == 1931).values
        #--------------------------------------------------------------
        #Separando o arquivo em dois
        df_aux_1 = deepcopy(df_vazoes[selecao1])
        df_aux_2 = deepcopy(df_vazoes[selecao2])
        #--------------------------------------------------------------
        #Renomeação da coluna
        df_aux_2.rename(columns={'ANOS': 'ANO_FIM'}, inplace=True)
        #--------------------------------------------------------------
        #Seleciona em qual mês inicia, realocando os meses
        #Une os DataFrames
        df_aux_1.loc[:, 1:self.mes_referencia] = df_aux_2.loc[:, 1:self.mes_referencia]
    
        return df_aux_1
    
    def reordenando_cabecalho_meses(self, mes: int) -> object:
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
        meses_reordenandos.rotate(- self.mes_referencia)
        print(meses_reordenandos)
        return meses_reordenandos

    def tabela_auxiliar(self, mes:int) -> pd.DataFrame : 
        """Digitar depois."""
        mes = self.mes_referencia
        #--------------------------------------------------------------------------
        #Tabela organizada
        meses_reordenando = reordenando_cabecalho_meses(mes)
        dados = reordenando_dados(mes)
        #--------------------------------------------------------------------------
        df_tabela_aux = dados.loc[:, ['ANOS'] + list(meses_reordenando)]
        df_tabela_aux['ANOS'] = df_tabela_aux['ANOS'].astype(str) + '-' + (df_tabela_aux['ANOS'] + 1).astype(str)
        #--------------------------------------------------------------------------
        return df_tabela_aux
    
    def correlacao(self, usina_sel: pd.DataFrame) -> np.Array:
        """ submiss """
        #--------------------------------------------------------------------------
        #função é usada para acessar a última linha do dataframe
        #x = np.array(usina_sel.tail(1))
        posto = self.posto
        usina_sel = self.selecione_usina(posto)  
        x1 = np.array(usina_sel.iloc[-2, :])
        #--------------------------------------------------------------------------
        #Cálculo correlação
        correlacao = np.corrcoef(x=x1, y=usina_sel)[1: -2, 0]
        #--------------------------------------------------------------------------
        return correlacao


    def periodo_da_correlacao(self):
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


    def não_sei(self):
        """Imagine descrever o que eu não sei."""    
        #--------------------------------------------------------------------------
        teste = tabela_aux.groupby("ANOS").get_group(ano_preenchimento)
        #--------------------------------------------------------------------------
        # #Selecionando até Dezembro
        # Até o memento as previsões 
        teste = teste.loc[:, :12]
    
    def inserindo_resuldado_correlacao(self)-> pd.DataFrame:
        """Retorna um DataFrame preenchido com as previsões."""
     
        criterio_selecao = self.df_vazao.loc[:, 'ANOS'] == 2023
     
        df_vazao_original.loc[criterio_selecao, self.mes_referencia+1: 12] = teste
      
        df_final_previsoes = df_vazao_original
        #--------------------------------------------------------------------------
        return df_final_previsoes

    def selecione_usina(self, cod:int) -> pd.DataFrame:
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
# %%
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


    def converter_to_txt(self):
        """Retorna o arquivo no formato original do vazoes.dat.
        
        Para as simulações no Rolling Horizon.
        """
        lista_linhas = list()
        
        for idx, row in self.df_final.iterrows():
            lista_linhas.append(f"{idx:3} {row['ANOS']:4}"
                                f"{row[1]:6}{row[2]:6}{row[3]:6}"
                                f"{row[4]:6}{row[5]:6}{row[6]:6}"
                                f"{row[7]:6}{row[8]:6}{row[9]:6}"
                                f"{row[10]:6}{row[11]:6}{row[12]:6}")

        tudo = '\n'.join(lista_linhas)
        nome_novo_arquivo = 'vazoes_AVG_TUCURUÍ.txt'
        
        with open(nome_novo_arquivo, 'w') as file:
            file.write(tudo)

        
        

    def converter_to_csv(self):
        """Retorna o arquivo em csv com as alterações e acrescimos dos cenários de previsão.
        
        Para aplicação em Excel ou uso em Power BI.
        
        USINAS_PRINCIPAIS = ('FURNAS', 'GBM', 'SOBRADINHO', 'TUCURUÍ', )
        """
        self.df_final.to_csv(r'C:/Users/E805511/Downloads/vazoes_SOBRADINHO.csv',
                                header= None, 
                                index=True, 
                                sep=';',
                                mode='w',
                                encoding='utf-8')



class Correlacao(Vazoes):
       pass


