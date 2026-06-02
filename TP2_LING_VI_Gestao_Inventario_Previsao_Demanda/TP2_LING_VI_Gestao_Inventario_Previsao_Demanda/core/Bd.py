import sqlite3
from core.base_interfaces import RepositorioAbstrato, ErroDominio
from models.produto import Produto
from models.usuario import Usuario

class BdRepositorio(RepositorioAbstrato):
    def __init__(self, db_name="inventario_inteligente.db"):
        self.db_name = db_name
        self._criar_tabelas()

    def _conectar(self):
        """Retorna uma conexão ativa com o banco de dados."""
        try:
            conn = sqlite3.connect(self.db_name)
            conn.execute("PRAGMA foreign_keys = ON;")  
            return conn
        except sqlite3.Error as e:
            raise ErroDominio(f"Erro ao conectar à base de dados: {e}")

    def _criar_tabelas(self):
        """Cria as tabelas necessárias no banco de dados se elas não existirem."""
        conexao = None
        try:
            conexao = sqlite3.connect(self.db_name)
            cursor = conexao.cursor()
            
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    username TEXT PRIMARY KEY,
                    senha_hash TEXT NOT NULL,
                    perfil TEXT NOT NULL
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    nome TEXT PRIMARY KEY,
                    categoria TEXT NOT NULL,
                    quantidade_atual INTEGER NOT NULL,
                    preco_custo REAL NOT NULL
                );
            """)
            
            conexao.commit()
        except sqlite3.Error as e:
            from core.base_interfaces import ErroDominio
            raise ErroDominio(f"Erro ao inicializar tabelas do banco: {e}")
        finally:
            if conexao:
                conexao.close()
    

    def salvar(self, entidade):
        """Salva ou atualiza uma entidade (Produto ou Usuario) na base de dados."""
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            if isinstance(entidade, Usuario):
                cursor.execute(
                    """
                    INSERT INTO usuarios (username, senha_hash, perfil)
                    VALUES (?, ?, ?)
                    ON CONFLICT(username) DO UPDATE SET
                        senha_hash=excluded.senha_hash,
                        perfil=excluded.perfil;
                    """,
                    (entidade.username, entidade.senha_hash, entidade.perfil)
                )
                
            elif isinstance(entidade, Produto):
                cursor.execute(
                    """
                    INSERT INTO produtos (nome, categoria, quantidade_atual, preco_custo)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(nome) DO UPDATE SET
                        categoria=excluded.categoria,
                        quantidade_atual=excluded.quantidade_atual,
                        preco_custo=excluded.preco_custo;
                    """,
                    (entidade.nome, entidade.categoria, entidade.quantidade_atual, entidade.preco_custo)
                )
            else:
                raise ErroDominio("Tipo de entidade desconhecido para persistência.")
            
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            raise ErroDominio(f"Erro ao salvar registro: {e}")
        finally:
            conn.close()

    def listar_todos(self) -> list:
        """Exemplo genérico solicitado pela interface (retorna dicionário com listas)."""
        return {
            "usuarios": self.listar_usuarios(),
            "produtos": self.listar_produtos()
        }


    def listar_usuarios(self) -> list:
        """Busca todos os utilizadores do banco de dados de forma segura."""
        from models.usuario import Usuario
        usuarios = []
        conexao = None
        try:
            conexao = sqlite3.connect(self.db_name)
            cursor = conexao.cursor()
            
            cursor.execute("SELECT username, senha_hash, perfil FROM usuarios")
            linhas = cursor.fetchall()
            
            for linha in linhas:
            
                user = Usuario(username=linha[0], senha_pura="1234", perfil=linha[2])
                
              
                user._senha_hash = linha[1] 
                usuarios.append(user)
                
            return usuarios
        except sqlite3.Error as e:
            from core.base_interfaces import ErroDominio
            raise ErroDominio(f"Erro ao listar utilizadores: {e}")
        finally:
            if conexao:
                conexao.close()

    def listar_produtos(self) -> list:
        """Busca todos os produtos do banco de dados e reconstrói os objetos Produto."""
        from models.produto import Produto
        produtos = []
        conexao = None
        try:
            conexao = sqlite3.connect(self.db_name) # Usa o nome dinâmico aqui
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, categoria, quantidade_atual, preco_custo FROM produtos")
            linhas = cursor.fetchall()
            
            for linha in linhas:
                prod = Produto(
                    nome=linha[0],
                    categoria=linha[1],
                    quantidade_atual=int(linha[2]),
                    preco_custo=float(linha[3])
                )
                produtos.append(prod)
            return produtos
        except sqlite3.Error as e:
            from core.base_interfaces import ErroDominio
            raise ErroDominio(f"Erro ao ler produtos do banco de dados: {e}")
        finally:
            if conexao:
                conexao.close()
    def buscar_usuario_por_username(self, username: str) -> Usuario:
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT username, senha_hash, perfil FROM usuarios WHERE username = ?", (username,))
            linha = cursor.fetchone()
            if linha:
                u = Usuario(linha[0], "temporaria", linha[2])
                u.senha_hash = linha[1]
                return u
            return None
        finally:
            conn.close()