from  abc import ABC, abstractmethod

class ErroDominio(Exception):
    pass

class RepositorioAbstrato(ABC):
    @abstractmethod
    def salvar(self, entidade):
        pass
    @abstractmethod
    def listar_todos(self):
        pass

class ModeloIAAbstrato(ABC):
    @abstractmethod
    def treinar(self, dados_historicos):
        pass

    @abstractmethod
    def prever_demanda(self, dados_entrada):
        pass