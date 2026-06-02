import customtkinter as ctk
from core.Bd import BdRepositorio
from gui.login_window import LoginWindow
from gui.main_dashboard import MainDashboard

class AplicacaoPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        

        self.title("Sistema de Gestão Agrícola - AGRO-STOCK IA")
        self.geometry("450x550")  
        self.bd = BdRepositorio()
        
        self.contentor = ctk.CTkFrame(self, fg_color="transparent")
        self.contentor.pack(fill="both", expand=True)
        
      
        self._carregar_tela_login()

    def _carregar_tela_login(self):
        """Monta o frame de login dentro da janela principal."""
 
        for filho in self.contentor.winfo_children():
            filho.destroy()
            
        # Altera o tamanho para o modo Login
        self.geometry("450x550")
        self.resizable(False, False)
        

        self.tela_login = LoginWindow(master=self.contentor, ao_autenticar_sucesso=self._carregar_painel_principal)
        self.tela_login.pack(fill="both", expand=True)

    def _carregar_painel_principal(self, usuario_autenticado):
        """Callback executado quando o login é validado com sucesso."""
        print(f"[Acesso] Sessão iniciada para o utilizador: {usuario_autenticado.username}")
        
     
        for filho in self.contentor.winfo_children():
            filho.destroy()
            
       
        self.resizable(True, True)
        self.geometry("1100x650")
        self.minimum_width = 1100
        self.minimum_height = 650
        self.title(f"Módulo de Gestão de Inventário Inteligente - [{usuario_autenticado.perfil}]")
        
   
        self.dashboard = MainDashboard(master=self.contentor, usuario_logado=usuario_autenticado)
        self.dashboard.pack(fill="both", expand=True)

if __name__ == "__main__":
   
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    app = AplicacaoPrincipal()
    app.mainloop()