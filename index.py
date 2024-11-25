import tkinter as tk
from tkinter import messagebox  

class Filho:
    def __init__(self, entrada, direcionamento):
        self.entrada = entrada
        self.direcionamento = direcionamento

class Pai:
    def __init__(self, simbolo, final=False, start=False):
        self.simbolo = simbolo
        self.filhos = []
        self.final = final
        self.start = start

    def adicionar_filho(self, filho):
        if isinstance(filho, Filho):
            self.filhos.append(filho)
        else:
            raise TypeError("O parâmetro deve ser uma instância da classe Filho")

    def buscar_filho(self, letra):
        for filho in self.filhos:
            if filho.entrada == letra:
                return filho
        return None
    
def inserir_simbolo(simbolo):
    campo_texto.insert(tk.INSERT, simbolo)

def verificar_string(pais, pais_dict, string):
    passos = []
    
    atual = next((pai for pai in pais if pai.start), None)
    if not atual:
        passos.append("Erro: Não há nó inicial definido.")
        return False, "\n".join(passos)
    
    for i, letra in enumerate(string):
        passos.append(f"Verificando letra '{letra}' no nó {atual.simbolo}")

        filho = atual.buscar_filho(letra)
        
        if not filho:
            passos.append(f"Não encontrou a letra '{letra}' no simbolo {atual.simbolo}. A string é inválida.")
            return False, "\n".join(passos)

        atual = pais_dict.get(filho.direcionamento)
        if not atual:
            passos.append(f"Erro: Não encontrou o nó de direcionamento '{filho.direcionamento}'")
            return False, "\n".join(passos)

        if i == len(string) - 1 and atual.final:
            passos.append(f"String válida. Chegou ao final no nó {atual.simbolo}.")
            return True, "\n".join(passos)
    
    passos.append(f"String inválida. O símbolo {atual.simbolo} não é final.")
    return False, "\n".join(passos)


def enviar_texto():
    tipo = tipo_linguagem.get()
    
    texto_entrada = campo_texto.get("1.0", tk.END).strip()
    string = campo_string.get().strip()
    
    linhas = texto_entrada.split("\n")
    erros = []
    pais = []
    linhaAtual = 1
    pais_dict = {}
    automato_finais = []
    
    for linha in linhas:
        if tipo == "Gramática Regular":
            if "->" in linha:
                simbolos = linha.split("->")
                if len(simbolos) != 2:
                    erros.append(f"linha {linhaAtual} - Formato inválido de seta '->'")
                    linhaAtual += 1
                    continue
                
                pai_simbolo = simbolos[0].strip()
                filhos_simbolos = simbolos[1].split("|")
                
                pai = Pai(pai_simbolo)
                if pai_simbolo == "S":
                    pai.start = True
                pais_dict[pai_simbolo] = pai
                
                for simbolo in filhos_simbolos:
                    simbolo = simbolo.strip()
                    if simbolo == "Σ":
                        pai.final = True
                    elif simbolo:
                        entrada = simbolo[0]
                        direcionamento = simbolo[1:]
                        filho = Filho(entrada, direcionamento)
                        pai.adicionar_filho(filho)
                
                pais.append(pai)
            else:
                erros.append(f"linha {linhaAtual} - Símbolo '->' não encontrado")
            linhaAtual += 1
        else:
            if "δ" in linha:
                simbolos = linha.split(":")
                if len(simbolos) != 2:
                    erros.append(f"linha {linhaAtual} - Formato inválido de ':'")
                    linhaAtual += 1
                    continue
                
                def remove_simbols(text):
                    return text.replace("δ", "").replace("(", "").replace(")", "").replace(":", "").replace(",", "").replace(" ", "")
                
                pai_simbolo = remove_simbols(simbolos[0].split(",")[0].strip())
                entrada = remove_simbols(simbolos[0].split(",")[1].strip())
                direcionamento = remove_simbols(simbolos[1].strip())
                
                pai = pais_dict.get(pai_simbolo)
                
                if not pai:
                    pai = Pai(pai_simbolo)
                    pais_dict[pai_simbolo] = pai
                    if pai_simbolo == "q0":
                        pai.start = True
                    filho = Filho(entrada, direcionamento)
                    pai.adicionar_filho(filho)
                    pais.append(pai)
                else:
                    filho = Filho(entrada, direcionamento)
                    pai.adicionar_filho(filho)
            elif "F{" in linha:
                simbolos = linha.replace("F{", "").replace("}", "").split(",")
                for simbolo in simbolos:
                    automato_finais.append(simbolo.strip())
            else:
                erros.append(f"linha {linhaAtual} - Símbolo 'δ' não encontrado")
            
            linhaAtual += 1
    
    if (tipo == "Autômato Finito"):
        if len(automato_finais) == 0:
            erros.append("Nenhum estado final encontrado")
            
        for simbolo in automato_finais:
            pai = pais_dict.get(simbolo)
            if pai:
                pai.final = True
            else:
                erros.append(f"Estado final '{simbolo}' não encontrado")
    
    for pai in pais:
        for filho in pai.filhos:
            paiEncontrado = pais_dict.get(filho.direcionamento)
            if not paiEncontrado and filho.direcionamento:
                erros.append(f"Derivada {filho.entrada} - Símbolo '{filho.direcionamento}' não encontrado")
        
    if not erros:
        is_aceita, mensagem = verificar_string(pais, pais_dict, string)
        label_resultado["text"] = "String aceita" if is_aceita else "String rejeitada"
        
        campo_passos.delete(1.0, tk.END) 
        campo_passos.insert(tk.END, mensagem)
    else:
        erros = list(set(erros))  
        label_resultado["text"] = "Erro na validação"
        campo_passos.delete(1.0, tk.END) 
        campo_passos.insert(tk.END, "\n".join(erros))
        
        
def trocar_tipo():
    tipo = tipo_linguagem.get()
    if tipo == "Gramática Regular":
        campo_texto.delete("1.0", tk.END)
        campo_texto.insert(tk.END, """S->aA|bB|Σ\nA->aA|bB\nB->bB|Σ\n""")
    else:
        campo_texto.delete("1.0", tk.END)
        campo_texto.insert(tk.END, """δ(q0,0):q0\nδ(q0,1):q1\nδ(q1,0):q2\nδ(q1,1):q1\nδ(q2,0):q0\nδ(q2,1):q1\nF{q2}\n""")         
    set_botoes()  


def ocultar_botoes():
    for widget in frame_teclado.winfo_children():
        widget.destroy()
        

def set_botoes():
    ocultar_botoes()
    if (tipo_linguagem.get() == "Autômato Finito"):
        botao_delta = tk.Button(frame_teclado, text="Delta", command=lambda: inserir_simbolo("δ"))
        botao_delta.grid(row=0, column=0, padx=5, pady=5)
        
        botao_elemento = tk.Button(frame_teclado, text="δ(q0, 0): q0", command=lambda: inserir_simbolo("δ(q0,0):q0"))
        botao_elemento.grid(row=0, column=1, padx=5, pady=5)

        botao_quebra_linha = tk.Button(frame_teclado, text="Quebra de Linha", command=lambda: inserir_simbolo("\n"))
        botao_quebra_linha.grid(row=0, column=4, padx=5, pady=5)
        
        botao_finais = tk.Button(frame_teclado, text="Finais", command=lambda: inserir_simbolo("F{q2}"))
        botao_finais.grid(row=0, column=2, padx=5, pady=5)
    else:
        botao_s = tk.Button(frame_teclado, text="Início", command=lambda: inserir_simbolo("S->"))
        botao_s.grid(row=0, column=0, padx=5, pady=5)

        botao_tra = tk.Button(frame_teclado, text="->", command=lambda: inserir_simbolo("->"))
        botao_tra.grid(row=0, column=1, padx=5, pady=5)

        botao_epsilon = tk.Button(frame_teclado, text="Σ", command=lambda: inserir_simbolo("Σ"))
        botao_epsilon.grid(row=0, column=2, padx=5, pady=5)

        botao_pipe = tk.Button(frame_teclado, text="|", command=lambda: inserir_simbolo("|"))
        botao_pipe.grid(row=0, column=3, padx=5, pady=5)

        botao_quebra_linha = tk.Button(frame_teclado, text="Quebra de Linha", command=lambda: inserir_simbolo("\n"))
        botao_quebra_linha.grid(row=0, column=4, padx=5, pady=5)

def mostrar_informacoes():
    tipo = tipo_linguagem.get()
    message = ""
    if (tipo == "Gramática Regular"):
        message = "Para iniciar a gramática regular, insira o símbolo inicial 'S' seguido de '->'.\n"
        message += "Em seguida, insira os símbolos que podem ser derivados de 'S' separados por '|'.\n"
        message += "Para indicar o fim da derivação, insira o símbolo 'Σ'."
    else:
        message = "Neste simulador, o início será sempre com o estado 'q0'.\n"
        message += "Para iniciar o autômato finito, insira o símbolo de transição 'δ'.\n"
        message += "Em seguida, insira o estado de origem, o símbolo de entrada e o estado de destino separados por ':'\n"
        message += "Para quebra de linha, insira '\\n'."        
    messagebox.showinfo("Informações - " + tipo, message)

janela = tk.Tk()
janela.title("Simulador de Linguagem Regular")

frame = tk.Frame(janela, padx=20, pady=20)
frame.pack(padx=10, pady=10)

tipo_linguagem = tk.StringVar()
tipo_linguagem.set("Gramática Regular") 

frame_selecao = tk.Frame(frame)
frame_selecao.pack(padx=5, pady=5, fill="x")

radio_gramatica = tk.Radiobutton(frame_selecao, text="Gramática Regular", variable=tipo_linguagem, value="Gramática Regular", command=trocar_tipo)
radio_gramatica.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

radio_automato = tk.Radiobutton(frame_selecao, text="Autômato Finito", variable=tipo_linguagem, value="Autômato Finito", command=trocar_tipo)
radio_automato.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

frame_selecao.grid_columnconfigure(0, weight=1)
frame_selecao.grid_columnconfigure(1, weight=1)

frame_teclado = tk.Frame(frame)
frame_teclado.pack(padx=5, pady=10)

label_texto = tk.Label(frame, text="Digite um texto:")
label_texto.pack(padx=5, pady=5)

botao_info = tk.Button(frame, text="Informações", command=mostrar_informacoes)
botao_info.pack(padx=5, pady=5)

campo_texto = tk.Text(frame, height=10, width=40)
campo_texto.pack(padx=5, pady=5)

trocar_tipo()

label_string = tk.Label(frame, text="Digite uma string:")
label_string.pack(padx=5, pady=5)

campo_string = tk.Entry(frame, width=40)
campo_string.pack(padx=5, pady=5)

botao_enviar = tk.Button(frame, text="Enviar", command=enviar_texto)
botao_enviar.pack(padx=5, pady=10)

label_resultado = tk.Label(frame, text="")
label_resultado.pack(padx=5, pady=5)

label_passos = tk.Label(frame, text="Passos realizados:")
label_passos.pack(padx=5, pady=5)

frame_scroll = tk.Frame(frame)
frame_scroll.pack(padx=5, pady=5)

campo_passos = tk.Text(frame_scroll, height=10, width=60)
campo_passos.pack(side=tk.LEFT, padx=5, pady=5)

scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=campo_passos.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

campo_passos.config(yscrollcommand=scrollbar.set)

janela.mainloop()
