import customtkinter as ctk
from tkinter import messagebox
from core.Bd import BdRepositorio
from core.base_interfaces import ErroDominio


ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, ao_autenticar_sucesso):
   
        super().__init__(master)
        
        self.ao_autenticar_sucesso = ao_autenticar_sucesso
        
        self.bd = BdRepositorio()
        
     
        self._construir_interface()

    def _construir_interface(self):
        # Título Principal
        self.label_titulo = ctk.CTkLabel(
            self, text="Bem-vindo", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.label_titulo.pack(pady=(40, 20))
        
        self.label_subtitulo = ctk.CTkLabel(
            self, text="Faça login para gerir o seu stock", font=ctk.CTkFont(size=14)
        )
        self.label_subtitulo.pack(pady=(0, 30))

       
        self.input_usuario = ctk.CTkEntry(
            self, width=280, placeholder_text="Nome de utilizador"
        )
        self.input_usuario.pack(pady=10)

        self.input_senha = ctk.CTkEntry(
            self, width=280, placeholder_text="Palavra-passe", show="*"
        )
        self.input_senha.pack(pady=10)

        self.botao_entrar = ctk.CTkButton(
            self, width=280, text="Entrar no Sistema", command=self._processar_login
        )
        self.botao_entrar.pack(pady=30)
        
   
        self.label_rodape = ctk.CTkLabel(
            self, text="IP-UNIKIVI • Departamento de Informática", font=ctk.CTkFont(size=10)
        )
        self.label_rodape.pack(side="bottom", pady=10)

    def _processar_login(self):
        username = self.input_usuario.get()
        senha = self.input_senha.get()

        
        if not username or not senha:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos.")
            return
            
        try:
       
            usuario = self.bd.buscar_usuario_por_username(username)
            
           
            if usuario and usuario.verificar_senha(senha):
                self.ao_autenticar_sucesso(usuario)
            else:
                messagebox.showerror("Acesso Negado", "Utilizador ou palavra-passe incorretos.")
                
        except ErroDominio as ed:
            messagebox.showerror("Erro de Domínio", str(ed))
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Ocorreu um erro inesperado: {e}")