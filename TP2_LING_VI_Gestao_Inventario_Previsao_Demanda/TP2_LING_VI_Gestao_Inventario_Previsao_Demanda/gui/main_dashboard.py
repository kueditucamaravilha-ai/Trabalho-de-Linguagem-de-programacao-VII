import customtkinter as ctk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np

from core.Bd import BdRepositorio
from ia.predictor import DemandaPredictor
from models.produto import Produto
from core.base_interfaces import ErroDominio

class MainDashboard(ctk.CTkFrame):
    def __init__(self, master, usuario_logado):
        
        super().__init__(master)
        

        self.usuario_logado = usuario_logado
        self.bd = BdRepositorio()
        self.predictor = DemandaPredictor()  
        self._construir_layout_principal()
        
        self._atualizar_tabela_produtos()

    def _construir_layout_principal(self):
     
        self.frame_lateral = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.frame_lateral.pack(side="left", fill="y")
        
        self.lbl_logo = ctk.CTkLabel(
            self.frame_lateral, text="AGRO-STOCK IA", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.lbl_logo.pack(pady=30)
        
        self.lbl_user = ctk.CTkLabel(
            self.frame_lateral, text=f"Operador: {self.usuario_logado.username}", font=ctk.CTkFont(size=12)
        )
        self.lbl_user.pack(pady=(0, 20))
        
        self.btn_atualizar = ctk.CTkButton(
            self.frame_lateral, text="Atualizar Dados", command=self._atualizar_tabela_produtos
        )
        self.btn_atualizar.pack(pady=10, padx=20)
        
        self.btn_prever = ctk.CTkButton(
            self.frame_lateral, text="Prever Demanda (IA)", fg_color="#2ecc71", hover_color="#27ae60",
            command=self._executar_previsao_ia
        )
        self.btn_prever.pack(pady=10, padx=20)
        
        self.btn_sair = ctk.CTkButton(
            self.frame_lateral, text="Terminar Sessão", fg_color="#e74c3c", hover_color="#c0392b",
            command=self.quit
        )
        self.btn_sair.pack(side="bottom", pady=20, padx=20)

  
        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_conteudo.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.lbl_secao_produtos = ctk.CTkLabel(
            self.frame_conteudo, text="Artigos em Stock Real", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.lbl_secao_produtos.pack(anchor="w", pady=(0, 10))
        
        estilo_tabela = ttk.Style()
        estilo_tabela.theme_use("clam")
        estilo_tabela.configure("Treeview", rowheight=25, font=("Arial", 11))
        
        self.tabela_produtos = ttk.Treeview(
            self.frame_conteudo, columns=("Nome", "Categoria", "Stock Atual", "Preço Custo"), show="headings", height=6
        )
        self.tabela_produtos.heading("Nome", text="Nome do Produto")
        self.tabela_produtos.heading("Categoria", text="Categoria")
        self.tabela_produtos.heading("Stock Atual", text="Stock Atual")
        self.tabela_produtos.heading("Preço Custo", text="Preço de Custo")
        
        self.tabela_produtos.pack(fill="x", expand=False, pady=5)

        # Inferior: Área do Gráfico Analítico (Matplotlib)
        self.frame_grafico = ctk.CTkFrame(self.frame_conteudo)
        self.frame_grafico.pack(fill="both", expand=True, pady=(20, 0))
        
        self._inicializar_grafico_vazio()

    def _inicializar_grafico_vazio(self):
        """Desenha ou limpa o gráfico para o estado inicial vazio."""
       
        if hasattr(self, 'ax'):
            self.ax.clear()
            self.ax.set_title("Tendência de Consumo & Previsão Logística")
            self.ax.set_xlabel("Meses de Análise")
            self.ax.set_ylabel("Unidades")
            self.canvas_grafico.draw()
        else:
           
            self.fig, self.ax = plt.subplots(figsize=(6, 3), dpi=100)
            self.ax.set_title("Tendência de Consumo & Previsão Logística")
            self.ax.set_xlabel("Meses de Análise")
            self.ax.set_ylabel("Unidades")
            self.fig.tight_layout()
            
            self.canvas_grafico = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
            self.canvas_grafico.get_tk_widget().pack(fill="both", expand=True)

    def _atualizar_tabela_produtos(self):
        """Busca os dados atualizados do banco, limpa a Treeview e faz reset ao gráfico."""

        for linha in self.tabela_produtos.get_children():
            self.tabela_produtos.delete(linha)
            
        self._inicializar_grafico_vazio()
            
        try:
            lista_produtos = self.bd.listar_produtos()
            for prod in lista_produtos:
                self.tabela_produtos.insert(
                    "", "end", values=(prod.nome, prod.categoria, prod.quantidade_atual, f"{prod.preco_custo:.2f} Kz")
                )
        except ErroDominio as ed:
            messagebox.showerror("Erro de Banco", str(ed))

    def _executar_previsao_ia(self):
        """Gera a previsão de demanda e atualiza dinamicamente o gráfico com dados baseados no produto."""
        item_selecionado = self.tabela_produtos.selection()
        if not item_selecionado:
            messagebox.showwarning("Seleção Necessária", "Selecione um produto na tabela para calcular a previsão.")
            return
            
        valores = self.tabela_produtos.item(item_selecionado, "values")
        nome_produto = valores[0]
        stock_atual = int(valores[2])
        preco_custo = float(valores[3].split()[0])
        
        try:
            # --- AJUSTE CRÍTICO: GERAÇÃO DE HISTÓRICO DINÂMICO ---
            # O histórico de consumo passa a ser calculado proporcionalmente ao stock e preço do produto
            base_vendas = max(40, stock_atual * 2)
            fator_preco = max(0.7, 1.3 - (preco_custo / 6000))
            
            historico_vendas = [
                int(base_vendas * 0.85 * fator_preco),
                int(base_vendas * 1.05 * fator_preco),
                int(base_vendas * 0.90 * fator_preco),
                int(base_vendas * 1.15 * fator_preco),
                int(base_vendas * 1.00 * fator_preco)
            ]
            
            dados_simulados = pd.DataFrame({
                'mes_ano': [1, 2, 3, 4, 5],
                'preco_custo': [preco_custo] * 5,
                'quantidade_vendida': historico_vendas
            })
            
            # Treina e executa o preditor inteligente
            self.predictor.treinar(dados_simulados)
            proximo_mes = 6
            quantidade_prevista = self.predictor.prever_demanda([proximo_mes, preco_custo])
            
            # --- ATUALIZAÇÃO DO GRÁFICO (Matplotlib) ---
            self.ax.clear()
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun (Previsto)']
            valores_vendas = historico_vendas + [quantidade_prevista]
            
            # Desenha as barras históricas (escuras) e a barra vermelha para a IA
            cores = ['#34495e'] * 5 + ['#e74c3c']
            self.ax.bar(meses, valores_vendas, color=cores)
            self.ax.set_title(f"Previsão de Reposição Inteligente para: {nome_produto}")
            self.ax.set_ylabel("Quantidade de Itens")
            
           
            self.ax.axhline(np.mean(valores_vendas[:-1]), color='orange', linestyle='--', label='Média Histórica')
            self.ax.legend()
            self.fig.tight_layout()
            
            # Renderiza as alterações na tela
            self.canvas_grafico.draw()
            
            messagebox.showinfo(
                "Cálculo Concluído", 
                f"O modelo preditivo sugere adquirir {quantidade_prevista} unidades de '{nome_produto}' para o próximo mês."
            )
            
        except ErroDominio as ed:
            messagebox.showerror("Erro na Predição", str(ed))