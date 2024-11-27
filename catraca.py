import tkinter as tk
from tkinter import messagebox
from enum import Enum
import random
import time
import threading

cores = {
    "botao_off": "#d3d3d3",
    "botao_on": "#4CAF50",
    "text_on": "white",
    "text_off": "black",
    "active_bg": "#45a049",
    "inactive_bg": "#a9a9a9"
}

class Estado(Enum):
    E0 = "E0"  # Estado inicial (sem ação, comanda não retirada)
    E1 = "E1"  # Pedido feito, esperando pagamento
    E2 = "E2"  # Pagamento realizado, pronto para sair
    E3 = "E3"  # Comanda retirada, catraca liberada para entrar
    E4 = "E4"  # Pedido sendo preparado
    E5 = "E5"  # Pedido pronto para retirada
    E6 = "E6"  # Entrou no restaurante

class CatracaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Catraca do Restaurante")
        self.root.geometry("600x500")
        
        self.estado = Estado.E0
        
        self.label = tk.Label(root, text="Bem-vindo ao Restaurante", font=("Arial", 16))
        self.label.pack(pady=20)

        self.cat_label = tk.Label(root, text="Catraca fechada", font=("Arial", 12), fg="red")
        self.cat_label.pack(pady=5) 

        self.instrucoes_label = tk.Label(root, text="Escolha uma opção:", font=("Arial", 12))
        self.instrucoes_label.pack(pady=10)

        self.retira_comanda_button = tk.Button(root, text="Retirar Comanda", command=self.retira_comanda, font=("Arial", 14),
                                               state=tk.NORMAL, bg=cores["botao_on"], fg=cores["text_on"], activebackground=cores["active_bg"])
        self.retira_comanda_button.pack(pady=5)

        self.entrar_button = tk.Button(root, text="Entrar no Restaurante", command=self.entrar, font=("Arial", 14),
                                       state=tk.DISABLED, bg=cores["botao_off"], fg=cores["text_off"], activebackground=cores["inactive_bg"])
        self.entrar_button.pack(pady=5)

        self.fazer_pedido_button = tk.Button(root, text="Fazer Pedido", command=self.fazer_pedido, font=("Arial", 14),
                                             state=tk.DISABLED, bg=cores["botao_off"], fg=cores["text_off"], activebackground=cores["inactive_bg"])
        self.fazer_pedido_button.pack(pady=5)

        self.retira_pedido_button = tk.Button(root, text="Retirar Pedido", command=self.retira_pedido, font=("Arial", 14),
                                              state=tk.DISABLED, bg=cores["botao_off"], fg=cores["text_off"], activebackground=cores["inactive_bg"])
        self.retira_pedido_button.pack(pady=5)

        self.pagar_button = tk.Button(root, text="Pagar", command=self.pagar, font=("Arial", 14),
                                      state=tk.DISABLED, bg=cores["botao_off"], fg=cores["text_off"], activebackground=cores["inactive_bg"])
        self.pagar_button.pack(pady=5)

        self.sair_button = tk.Button(root, text="Sair", command=self.sair, font=("Arial", 14),
                                      state=tk.DISABLED, bg=cores["botao_off"], fg=cores["text_off"], activebackground=cores["inactive_bg"])
        self.sair_button.pack(pady=5)

        self.resultado_label = tk.Label(root, text="", font=("Arial", 12))
        self.resultado_label.pack(pady=10)

    def atualizar_botao(self, button, state, bg_color, fg_color, active_bg_color):
        button.config(state=state, bg=bg_color, fg=fg_color, activebackground=active_bg_color)

    def exibir_mensagem(self, mensagem, tipo="info"):
        if tipo == "erro":
            self.resultado_label.config(fg="red")
        else:
            self.resultado_label.config(fg="green")
        self.resultado_label.config(text=mensagem)

    def atualizar_cat_status(self):
        """Atualiza a mensagem de estado da catraca."""
        if self.estado == Estado.E2 or self.estado == Estado.E6:
            self.cat_label.config(text="Catraca aberta - Você pode sair", fg="green")
        elif self.estado == Estado.E3:
            self.cat_label.config(text="Catraca aberta - Você pode entrar", fg="green")
        else:
            self.cat_label.config(text="Catraca fechada", fg="red") 

    def retira_comanda(self):
        if self.estado == Estado.E0:
            self.estado = Estado.E3
            self.label.config(text="Você retirou a comanda. A catraca está liberada para entrar.")
            self.exibir_mensagem("Comanda retirada! Agora entre no restaurante.", "info")
            self.atualizar_botao(self.retira_comanda_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.atualizar_botao(self.entrar_button, tk.NORMAL, cores["botao_on"], cores["text_on"], cores["active_bg"])
            self.atualizar_cat_status() 
        else:
            self.exibir_mensagem("Você já retirou a comanda ou ainda não entrou no restaurante.", "erro")

    def entrar(self):
        if self.estado == Estado.E3:
            self.estado = Estado.E6
            self.label.config(text="Você entrou no restaurante.")
            self.exibir_mensagem("")
            self.atualizar_botao(self.entrar_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.atualizar_botao(self.fazer_pedido_button, tk.NORMAL, cores["botao_on"], cores["text_on"], cores["active_bg"])
            self.sair_button.config(state=tk.NORMAL, bg=cores["botao_on"], fg=cores["text_on"], activebackground=cores["active_bg"])
            self.atualizar_cat_status()
        else:
            self.exibir_mensagem("Primeiro, retire a comanda para poder entrar.", "erro")

    def fazer_pedido(self):
        if self.estado in [Estado.E6, Estado.E1, Estado.E2]:
            self.estado = Estado.E4
            self.label.config(text="Pedido sendo preparado...")
            self.exibir_mensagem("Pedido sendo preparado!", "info")
            self.atualizar_botao(self.fazer_pedido_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.atualizar_botao(self.retira_pedido_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.atualizar_botao(self.pagar_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.atualizar_botao(self.sair_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.iniciar_timer_preparo()
            self.atualizar_cat_status() 
        else:
            self.exibir_mensagem("Você precisa entrar no restaurante antes de fazer o pedido.", "erro")

    def iniciar_timer_preparo(self):
        tempo_preparo = random.randint(3, 8)
        threading.Thread(target=self.timer_preparo, args=(tempo_preparo,)).start()

    def timer_preparo(self, tempo):
        time.sleep(tempo)
        self.estado = Estado.E5
        self.label.config(text="Pedido pronto para retirada!")
        self.exibir_mensagem(f"Pedido pronto após {tempo} segundos.", "info")
        self.atualizar_botao(self.retira_pedido_button, tk.NORMAL, cores["botao_on"], cores["text_on"], cores["active_bg"])

    def retira_pedido(self):
        if self.estado == Estado.E5:
            self.estado = Estado.E1
            self.label.config(text="Você retirou o pedido. Agora, pague para sair ou faça outro pedido.")
            self.exibir_mensagem("Pedido retirado!", "info")
            self.atualizar_botao(self.retira_pedido_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.atualizar_botao(self.fazer_pedido_button, tk.NORMAL, cores["botao_on"], cores["text_on"], cores["active_bg"])
            self.atualizar_botao(self.pagar_button, tk.NORMAL, cores["botao_on"], cores["text_on"], cores["active_bg"])
            self.atualizar_cat_status()
        else:
            self.exibir_mensagem("O pedido ainda não está pronto.", "erro")

    def pagar(self):
        if self.estado == Estado.E1:
            self.estado = Estado.E2
            self.label.config(text="Pagamento efetuado. Agora você pode sair.")
            self.exibir_mensagem("Pagamento realizado!", "info")
            self.atualizar_botao(self.pagar_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.atualizar_botao(self.sair_button, tk.NORMAL, cores["botao_on"], cores["text_on"], cores["active_bg"])
            self.atualizar_cat_status() 
        else:
            self.exibir_mensagem("Primeiro, faça o pedido.", "erro")

    def sair(self):
        if self.estado in [Estado.E2, Estado.E6]:
            self.estado = Estado.E0
            self.label.config(text="Você saiu do restaurante. Obrigado pela visita!")
            self.exibir_mensagem("Até a próxima!", "info")
            self.atualizar_botao(self.sair_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.atualizar_botao(self.entrar_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.atualizar_botao(self.retira_comanda_button, tk.NORMAL, cores["botao_on"], cores["text_on"], cores["active_bg"])
            self.atualizar_botao(self.fazer_pedido_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.atualizar_cat_status()
        else:
            self.exibir_mensagem("Você precisa pagar antes de sair.", "erro")

if __name__ == "__main__":
    root = tk.Tk()
    app = CatracaApp(root)
    root.mainloop()
