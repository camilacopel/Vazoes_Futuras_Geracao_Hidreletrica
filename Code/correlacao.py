"""
# Verificar se o arquivo existe.

# Método Try
"""
from copy import deepcopy
from pathlib import Path
import pandas as pd
import numpy as np
from collections import deque



#%% classe
class Correlacao:
    """
    Parâmetros de entrada:
        
        path (Path): caminho do arquivo
        mes (int): mês que se encerra as previsões da Refinitiv
        posto (int): Número do posto da usina de acordo com arquivo confhd.dat
     
    ------
    
    A classe:
    
        1. Constroe uma tabela auxiliar
        2. Realiza a correlaçao de Pearson
        3. Preenche os valores nulos do último ano com o resultado da correlação
        4. Exporta o arquivo vazoes preenchido em txt ou csv 
        
    """
    MESES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    USINAS_PRINCIPAIS = ('FURNAS', 'GBM','SOBRADINHO', 'TUCURUÍ' )
    POSTOS_ = {
        '6': 'FURNAS',
        '74': 'GBM',
        '169': 'SOBRADINHO',
        '275': 'TUCURUÍ'
    }
    
    
    def __init__(self,
                 caminho_arquivo: str,
                 mes_referencia: int,
                 posto: int):
        
        
        self.path = Path(caminho_arquivo)
        self.mes_referencia = int(mes_referencia)
        self.posto = int(posto)
        
        #-------------------------------------------------------------------------
        if mes_referencia > 12:
            raise Exception
        #-------------------------------------------------------------------------
        #Leitura do arquivo
        df_vazoes = pd.read_csv(self.path, sep='\s+', header=None )
        cab = ['POSTO', 'ANOS'] + MESES
        df_vazoes.columns = cab
        df_vazoes.set_index(['POSTO'], drop=True, inplace=True)
        #-------------------------------------------------------------------------
        
        self.df_vazoes = df_vazoes


    #Construindo a tabela auxiliar para fazer a correlação
    def _reordenando_dados(self) -> pd.DataFrame :
        """
        Versiona e une dos dados com referência
        mês que finaliza a previsão da Refinitiv
        
        Seleciona em qual mês inicia, realocando os meses anteriores.
        No caso, inicia em Abril...
        """
        #--------------------------------------------------------------
        #Seleciona o primeiro e o último ano
        #Retorno em bool. '~ inverte True em False e vice-versa
        selecao1 = ~(self.df_vazoes.loc[:, 'ANOS'] == 2023).values
        selecao2 = ~(self.df_vazoes.loc[:, 'ANOS'] == 1931).values
        #--------------------------------------------------------------
        #Separando o arquivo em dois e realiza uma cópia
        df_aux_1 = deepcopy(self.df_vazoes[selecao1])
        df_aux_2 = deepcopy(self.df_vazoes[selecao2])
        #--------------------------------------------------------------
        #Renomeação da coluna
        df_aux_2.rename(columns={'ANOS': 'ANO_FIM'}, inplace=True)
        #--------------------------------------------------------------
        #Seleciona em qual mês inicia, realocando os meses
        #Une os DataFrames
        df_aux_1.loc[:, 1:self.mes_referencia] = df_aux_2.loc[:, 1:self.mes_referencia]
        
        return df_aux_1

    def _reordenando_cabecalho_meses(self) -> object:
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
        
    
    def tabela_auxiliar(self) -> pd.DataFrame: 
        """Digitar depois."""
        #--------------------------------------------------------------------------
        #Tabela organizada
        cabecalho_meses = self._reordenando_cabecalho_meses()
        dados = self._reordenando_dados()
        #--------------------------------------------------------------------------
        df_tabela_aux = dados.loc[:, ['ANOS'] + list(cabecalho_meses)]
        df_tabela_aux['ANOS'] = df_tabela_aux['ANOS'].astype(str) + '-' + (df_tabela_aux['ANOS'] + 1).astype(str)
        #--------------------------------------------------------------------------
        
        return df_tabela_aux
    
    
    #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    #Cálcular a correlação de devolver o ano selecionado
    
    def usina_selecionada(self) -> pd.DataFrame:
        """correlação é refente a uma usina.
        
        Código das maiores usinas de cada submercado de energia.
        """
        tabela_auxiliar = self.tabela_auxiliar()
        dados_usinas_selecionada = tabela_auxiliar.groupby("POSTO").get_group(self.posto)
        
        
        if self.posto == 6:
            print(USINAS_PRINCIPAIS[0])
        elif self.posto == 74:
            print(USINAS_PRINCIPAIS[1])
        elif self.posto == 169:
            print(USINAS_PRINCIPAIS[2])
        elif self.posto == 275:
            print(USINAS_PRINCIPAIS[3])
        else:
            print('Escolha entre as usinas cod:[6, 74, 169, 275]')
        
        return dados_usinas_selecionada
    
    
    def series_anos(self):
        """Escrever depois."""
        #-----------------------------------------------------------
        #Seleção da coluna com os anos da tabela auxiliar
        usina_sel = self.usina_selecionada()
        series_anos = usina_sel['ANOS']
        series_anos.reset_index(drop=True, inplace=True)
        #-----------------------------------------------------------
        # self.usina_selecionada.set_index('ANOS', inplace=True)
        #-----------------------------------------------------------
        return series_anos
    
    
#Cálculo da correlação
    def correlacao(self) -> np.array:
        """submiss."""
        #--------------------------------------------------------------------------
        #função é usada para acessar a última linha do dataframe
        #x = np.array(usina_sel.tail(1))
       
        usina_sel = self.usina_selecionada()
        usina_sel.set_index('ANOS', inplace=True)
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
        series_anos = self.series_anos()
        correlacao = self.correlacao()
        ano_escolhido = series_anos[correlacao.argmax()]
        print(f'período da correlação: {ano_escolhido}')
        #--------------------------------------------------------------------------
        ano_preenchimento = series_anos[correlacao.argmax()+1]
        #--------------------------------------------------------------------------

        return ano_preenchimento


    def dados_para_preencher(self) -> pd.DataFrame:
        """Seleciona o ano da resultante da correlação de Pearson.
        
        Retorna um tabela com o o ano da correlação para cada uma das usinas.
        """    
        #--------------------------------------------------------------------------
        tabela_aux = self.tabela_auxiliar()
        df = tabela_aux.groupby("ANOS").get_group(self.periodo_da_correlacao())
        #--------------------------------------------------------------------------
        # #Selecionando até Dezembro
        # Até o memento as previsões 
        df = df.loc[:, :12]
        return df



# Preenchimento dos valores NaN com o resultado da correlação
    def resuldado_correlacao(self)-> pd.DataFrame:
        """Retorna um DataFrame preenchido com as previsões."""
        #Realizar um maneira de identificar o último ano
        criterio_selecao = self.df_vazoes.loc[:, 'ANOS'] == 2023
        
        if self.mes_referencia < 12:
            self.df_vazoes.loc[criterio_selecao, self.mes_referencia+1: 12] = self.dados_para_preencher()
        else:
            print('Tenho que resolver! Quando o mês é 12')
        
        
        df_final = self.df_vazoes
        #--------------------------------------------------------------------------
        return df_final
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


    def converter_to_txt(self):
        """Retorna o arquivo no formato original do vazoes.dat.
        
        Para as simulações no Rolling Horizon.
        """
        df_final = self.resuldado_correlacao()
        lista_linhas = list()
        
        for idx, row in df_final.iterrows():
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
        df_final = self.resuldado_correlacao()
        df_final.to_csv(r'C:/Users/E805511/Downloads/vazoes_SOBRADINHO.csv',
                        header= None, 
                        index=True, 
                        sep=';',
                        mode='w',
                        encoding='utf-8')



# class Correlacao(Vazoes):
#        pass
#%% if name
if __name__ == '__main__':
    
    arq = Path("C:/Users/E805511/Downloads/VAZOES-P75.txt")
    mes = 4
    posto = 6
    
    # arq = str(input('Caminho do arquivo: '))
    # posto = int(input('Posto da usina: '))
    # mes = int(input('Més final da previsão: '))
    
    vazoes = Vazoes(caminho_arquivo=arq, mes_referencia=mes, posto=posto)
    resultado = vazoes.resuldado_correlacao()
