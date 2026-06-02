from core.base_interfaces import ErroDominio

class Produto:
    def __init__(self, nome: str, categoria: str, quantidade_atual: int, preco_custo: float):
        
        self.nome = nome
        self.categoria = categoria
        self.quantidade_atual = quantidade_atual
        self.preco_custo = preco_custo

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor):
        valor_str = str(valor).strip()
        if not valor_str or len(valor_str) == 0:
            raise ErroDominio("O nome do produto não pode estar vazio.")
        self._nome = valor_str

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        valor_str = str(valor).strip()
        if not valor_str or len(valor_str) == 0:
            raise ErroDominio("A categoria do produto não pode estar vazia.")
        self._categoria = valor_str

    @property
    def quantidade_atual(self) -> int:
        return self._quantidade_atual

    @quantidade_atual.setter
    def quantidade_atual(self, valor):
        try:
           
            valor_int = int(valor)
        except (ValueError, TypeError):
            raise ErroDominio("A quantidade atual deve ser um número inteiro válido.")
            
        if valor_int < 0:
            raise ErroDominio("A quantidade em stock não pode ser negativa.")
        self._quantidade_atual = valor_int

    @property
    def preco_custo(self) -> float:
        return self._preco_custo

    @preco_custo.setter
    def preco_custo(self, valor):
        try:
          
            valor_float = float(valor)
        except (ValueError, TypeError):
            raise ErroDominio("O preço de custo deve ser um número real válido.")
            
        if valor_float < 0:
            raise ErroDominio("O preço de custo não pode ser negativo.")
        self._preco_custo = valor_float