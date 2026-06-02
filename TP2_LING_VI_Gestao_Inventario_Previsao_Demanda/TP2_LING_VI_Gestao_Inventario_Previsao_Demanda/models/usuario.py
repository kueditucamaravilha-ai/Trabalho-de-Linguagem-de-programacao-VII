import hashlib
from core.base_interfaces import ErroDominio

class Usuario:
    def __init__(self, username: str, senha_pura: str, perfil: str = "Operador"):
        self.username = username
        self.senha_hash = self._criptografar_senha(senha_pura)
        self.perfil = perfil  
 
    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, valor):
       
        valor_str = str(valor).strip()
        
        # 2. Faz a validação correta do texto limpo
        if not valor_str or len(valor_str) == 0:
            raise ErroDominio("O nome de utilizador não pode estar vazio.")
            
        self._username = valor_str

    @property
    def perfil(self) -> str:
        return self._perfil

    @property
    def perfil(self) -> str:
        return self._perfil

    @perfil.setter
    def perfil(self, valor: str):
        perfis_validos = ["Administrador", "Operador"]
        if valor not in perfis_validos:
            raise ErroDominio(f"Perfil inválido. Escolha entre: {', '.join(perfis_validos)}")
        self._perfil = valor
    def _criptografar_senha(self, senha: str) -> str:
        if not senha or len(senha) < 4:
            raise ErroDominio("A senha deve conter pelo menos 4 caracteres.")
    
        return hashlib.sha256(senha.encode('utf-8')).hexdigest()

    def verificar_senha(self, senha_pura: str) -> bool:
        """Verifica se a senha digitada corresponde ao hash guardado."""
        return self.senha_hash == hashlib.sha256(senha_pura.encode('utf-8')).hexdigest()

    def __str__(self) -> str:
        return f"Usuario(username='{self.username}', perfil='{self.perfil}')"