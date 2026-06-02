
import functools
import sys
from core.base_interfaces import ErroDominio

def capturar_erros(func):
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[ERRO CRÍTICO SYSTEM]: {str(e)}", file=sys.stderr)
            raise ErroDominio(f"Falha na operação: {str(e)}")
    return wrapper

class GestorAuditoria:
    
    def __init__(self, acao):
        self.acao = acao

    def __enter__(self):
        print(f"[AUDITORIA - INÍCIO]: Executando '{self.acao}'...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"[AUDITORIA - FALHA]: Ocorreu um erro em '{self.acao}': {exc_val}")
        else:
            print(f"[AUDITORIA - SUCESSO]: '{self.acao}' concluída com êxito.")
        return False  # Permite a propagação de exceções tratadas