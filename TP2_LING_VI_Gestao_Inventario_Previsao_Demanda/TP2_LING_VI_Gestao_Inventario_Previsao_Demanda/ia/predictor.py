import os
import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression
from core.base_interfaces import ModeloIAAbstrato, ErroDominio

class DemandaPredictor(ModeloIAAbstrato):
    def __init__(self, caminho_modelo="ia/modelo_treinado.pkl"):
        self.caminho_modelo = caminho_modelo
        self.modelo = None
        self._carregar_modelo_existente()

    def _carregar_modelo_existente(self):
        """Tenta carregar o modelo binário guardado em disco (exigência do enunciado)."""
        if os.path.exists(self.caminho_modelo):
            try:
                with open(self.caminho_modelo, 'rb') as f:
                    self.modelo = pickle.load(f)
            except Exception as e:
               
                print(f"Aviso: Não foi possível carregar o modelo salvo: {e}")

    def treinar(self, dados_historicos: pd.DataFrame):
        """
        Treina o modelo de regressão linear.
        dados_historicos deve conter as colunas: 
        ['mes_ano', 'preco_custo', 'quantidade_vendida']
        """
        if dados_historicos.empty:
            raise ErroDominio("Não existem dados históricos suficientes para treinar o modelo.")

        try:
          
            X = dados_historicos[['mes_ano', 'preco_custo']]
     
            y = dados_historicos['quantidade_vendida']

            self.modelo = LinearRegression()
            self.modelo.fit(X, y)

           
            os.makedirs(os.path.dirname(self.caminho_modelo), exist_ok=True)
            with open(self.caminho_modelo, 'wb') as f:
                pickle.dump(self.modelo, f)

        except Exception as e:
            raise ErroDominio(f"Erro durante o treino do modelo de IA: {e}")

    def prever_demanda(self, dados_entrada: list) -> int:
        """
        Prevê a quantidade ideal de stock para o próximo período.
        dados_entrada: lista contendo [mes_atual, preco_custo_produto]
        """
        if self.modelo is None:
           
            raise ErroDominio("O modelo de IA ainda não foi treinado. Por favor, realize o treino primeiro.")

        try:
           
            df_entrada = pd.DataFrame([dados_entrada], columns=['mes_ano', 'preco_custo'])
            previsao = self.modelo.predict(df_entrada)[0]

            
            quantidade_prevista = max(0, int(round(previsao)))
            return quantidade_prevista

        except Exception as e:
            raise ErroDominio(f"Erro ao processar a previsão da IA: {e}")