import tkinter as tk
from tkinter import messagebox
from enum import Enum

cores = {
    "botao_off": "#d3d3d3",
    "botao_on": "#4CAF50",
    "text_on": "white",
    "text_off": "black",
    "active_bg": "#45a049",
    "inactive_bg": "#a9a9a9"
}

class Estado(Enum):
    E0 = "E0" 
    E1 = "E1" 
    E2 = "E2" 

class CatracaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Catraca do Restaurante")
        self.root.geometry("500x400")
        
        self.estado = Estado.E0
        
        self.label = tk.Label(root, text="Bem-vindo ao Restaurante", font=("Arial", 16))
        self.label.pack(pady=20)

        self.cat_label = tk.Label(root, text="Catraca fechada", font=("Arial", 12), fg="red")
        self.cat_label.pack(pady=5) 

        self.instrucoes_label = tk.Label(root, text="Escolha uma opção:", font=("Arial", 12))
        self.instrucoes_label.pack(pady=10)

        self.entrar_button = tk.Button(root, text="Entrar no Restaurante", command=self.entrar, font=("Arial", 14),
                                       bg=cores["botao_on"], fg=cores["text_on"], activebackground=cores["inactive_bg"])
        self.entrar_button.pack(pady=5)

        self.fazer_pedido_button = tk.Button(root, text="Fazer Pedido", command=self.fazer_pedido, font=("Arial", 14),
                                             state=tk.DISABLED, bg=cores["botao_off"], fg=cores["text_off"], activebackground=cores["inactive_bg"])
        self.fazer_pedido_button.pack(pady=5)

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
        if self.estado == Estado.E2:
            self.cat_label.config(text="Catraca aberta", fg="green") 
        else:
            self.cat_label.config(text="Catraca fechada", fg="red") 

    def entrar(self):
        self.estado = Estado.E0
        self.label.config(text="Você entrou no restaurante")
        self.exibir_mensagem("")
        self.atualizar_botao(self.entrar_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
        self.atualizar_botao(self.fazer_pedido_button, tk.NORMAL, cores["botao_on"], cores["text_on"], cores["active_bg"])
        self.atualizar_botao(self.sair_button, tk.NORMAL, cores["botao_on"], cores["text_on"], cores["active_bg"])
        self.atualizar_cat_status() 

    def fazer_pedido(self):
        if self.estado == Estado.E0:
            self.estado = Estado.E1
            self.label.config(text="Você fez o pedido. Agora, pague para sair.")
            self.exibir_mensagem("Pedido realizado!", "info")
            self.atualizar_botao(self.fazer_pedido_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.atualizar_botao(self.pagar_button, tk.NORMAL, cores["botao_on"], cores["text_on"], cores["active_bg"])
            self.atualizar_botao(self.sair_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.atualizar_cat_status() 
        else:
            self.exibir_mensagem("Primeiro, entre no restaurante.", "erro")

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
        if self.estado in [Estado.E2, Estado.E0]:
            self.estado = Estado.E0
            self.label.config(text="Você saiu do restaurante. Obrigado pela visita!")
            self.exibir_mensagem("Até a próxima!", "info")
            self.atualizar_botao(self.sair_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.atualizar_botao(self.entrar_button, tk.NORMAL, cores["botao_on"], cores["text_on"], cores["active_bg"])
            self.atualizar_botao(self.fazer_pedido_button, tk.DISABLED, cores["botao_off"], cores["text_off"], cores["inactive_bg"])
            self.atualizar_cat_status() 
        elif self.estado == Estado.E1:
            self.exibir_mensagem("Você precisa pagar antes de sair.", "erro")
        else:
            self.exibir_mensagem("Você ainda não fez o pedido.", "erro")

if __name__ == "__main__":
    root = tk.Tk()
    app = CatracaApp(root)
    root.mainloop()
