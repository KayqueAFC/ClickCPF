import os
import re
import sys
import tkinter as tk
from tkinter import ttk


# Aparência da janela
FONT = ("Segoe UI", 10, "bold")
FONTBOX = ("Segoe UI", 10)

BTN_BG = "#1E90FF"
BTN_FG = "#ffffff"
BTN_HOVER = "#1C86EE"

BORDER_COLOR = "#FFD700"
BORDER_PAD = 2
STATUS_BG = "#f1f5f9"

PLACEHOLDER = "Pesquisar..."


# Arquivo de vendedores
def caminho_vendedores():
    # Quando compilado, o TXT fica na mesma pasta do executável.
    if getattr(sys, "frozen", False):
        pasta = os.path.dirname(sys.executable)
    else:
        pasta = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(pasta, "vendedores.txt")


def carregar_vendedores():
    caminho = caminho_vendedores()
    vendedores = []

    if not os.path.exists(caminho):
        return vendedores

    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(",")

            if len(partes) == 2:
                nome, cpf = partes
                vendedores.append((nome.strip(), cpf.strip()))

    return vendedores


def salvar_vendedores():
    # Regrava a lista para manter o arquivo atualizado após as alterações.
    with open(caminho_vendedores(), "w", encoding="utf-8") as arquivo:
        for nome, cpf in VENDEDORES:
            arquivo.write(f"{nome},{cpf}\n")


VENDEDORES = carregar_vendedores()


# Janela principal
root = tk.Tk()
root.title("ClickCpf - Desenvolvido por Kayque A.")
root.geometry("380x460")
root.resizable(False, False)
root.configure(bg="white")

style = ttk.Style(root)
style.configure("TEntry", padding=6, font=FONTBOX)
style.configure("TLabel", font=FONT)
style.configure("Status.TLabel", background=STATUS_BG, font=("Segoe UI", 9))


# Cabeçalho e pesquisa
header = tk.Label(
    root,
    text="Clique no vendedor para copiar o CPF",
    font=("Segoe UI", 11, "bold"),
    bg="white"
)
header.pack(padx=12, pady=(12, 6))

search_var = tk.StringVar()
search_entry = ttk.Entry(root, textvariable=search_var)
search_entry.pack(fill="x", padx=12, pady=(0, 8))
search_entry.insert(0, PLACEHOLDER)


def on_search_focus_in(event):
    if search_entry.get() == PLACEHOLDER:
        search_entry.delete(0, "end")


def on_search_focus_out(event):
    if not search_entry.get().strip():
        search_entry.insert(0, PLACEHOLDER)


search_entry.bind("<FocusIn>", on_search_focus_in)
search_entry.bind("<FocusOut>", on_search_focus_out)


# Lista de vendedores com rolagem
container = ttk.Frame(root)
container.pack(fill="both", expand=True, padx=12, pady=(0, 8))

canvas = tk.Canvas(
    container,
    borderwidth=0,
    highlightthickness=0,
    bg="white"
)

scrollbar = ttk.Scrollbar(
    container,
    orient="vertical",
    command=canvas.yview
)

scrollable_frame = ttk.Frame(canvas)
window_id = canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw"
)

canvas.configure(yscrollcommand=scrollbar.set)


def on_frame_configure(event):
    # Ajusta a área de rolagem conforme a quantidade de vendedores.
    canvas.configure(scrollregion=canvas.bbox("all"))


def on_canvas_configure(event):
    # Mantém os botões ocupando toda a largura disponível.
    canvas.itemconfig(window_id, width=event.width)


scrollable_frame.bind("<Configure>", on_frame_configure)
canvas.bind("<Configure>", on_canvas_configure)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# A rolagem pelo mouse só fica ativa enquanto o cursor está sobre a lista.
def on_mousewheel_windows(event):
    canvas.yview_scroll(int(-event.delta / 120), "units")


def on_mousewheel_linux(event):
    if event.num == 4:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        canvas.yview_scroll(1, "units")


def bind_mousewheel(event):
    root.bind_all("<MouseWheel>", on_mousewheel_windows)
    root.bind_all("<Button-4>", on_mousewheel_linux)
    root.bind_all("<Button-5>", on_mousewheel_linux)


def unbind_mousewheel(event):
    root.unbind_all("<MouseWheel>")
    root.unbind_all("<Button-4>")
    root.unbind_all("<Button-5>")


canvas.bind("<Enter>", bind_mousewheel)
canvas.bind("<Leave>", unbind_mousewheel)


# Barra de status
status_var = tk.StringVar(value="Pronto")

status = ttk.Label(
    root,
    textvariable=status_var,
    style="Status.TLabel",
    anchor="w"
)
status.pack(fill="x", padx=12, pady=(0, 12))


# Cópia do CPF e mensagens de status
def copiar_para_area_transferencia(texto):
    root.clipboard_clear()
    root.clipboard_append(texto)
    root.update()


def atualizar_status(texto, tempo_ms=2000):
    status_var.set(texto)
    root.after(tempo_ms, lambda: status_var.set("Pronto"))


# Criação e atualização dos botões
button_widgets = []


def criar_botao(nome, cpf):
    # A borda amarela fica separada do botão para facilitar a personalização.
    border = tk.Frame(
        scrollable_frame,
        bg=BORDER_COLOR,
        padx=BORDER_PAD,
        pady=BORDER_PAD
    )
    border.pack(pady=6, padx=0, anchor="n", fill="x")

    btn = tk.Button(
        border,
        text=nome,
        anchor="center",
        bg=BTN_BG,
        fg=BTN_FG,
        relief="flat",
        font=FONT,
        activebackground=BTN_HOVER,
        bd=0
    )
    btn.pack(fill="x", expand=True)

    # Guarda o nome e o CPF para usar os dados do vendedor clicado.
    btn.configure(
        command=lambda n=nome, c=cpf: (
            copiar_para_area_transferencia(c),
            atualizar_status(f"CPF de {n} copiado")
        )
    )

    def on_enter(event):
        btn.configure(bg=BTN_HOVER)

    def on_leave(event):
        btn.configure(bg=BTN_BG)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    button_widgets.append((border, nome, cpf))


def popular_lista(filtro=""):
    # Remove os botões antigos antes de montar a lista filtrada.
    for widget, *_ in button_widgets:
        widget.destroy()

    button_widgets.clear()
    filtro = filtro.strip().lower()

    for nome, cpf in VENDEDORES:
        if not filtro or filtro in nome.lower():
            criar_botao(nome, cpf)


def on_search_change(*args):
    texto = search_var.get()

    if texto == PLACEHOLDER:
        texto = ""

    popular_lista(texto)


search_var.trace_add("write", on_search_change)


# Cadastro de vendedores
def adicionar_vendedor():
    popup = tk.Toplevel(root)
    popup.title("Adicionar Vendedor")
    popup.geometry("300x220")
    popup.configure(bg="white")

    tk.Label(
        popup,
        text="Nome:",
        font=FONT,
        bg="white"
    ).pack(pady=5)

    nome_var = tk.StringVar()
    tk.Entry(
        popup,
        textvariable=nome_var,
        font=FONTBOX
    ).pack(pady=5)

    tk.Label(
        popup,
        text="CPF (XXX.XXX.XXX-XX):",
        font=FONT,
        bg="white"
    ).pack(pady=5)

    cpf_var = tk.StringVar()
    tk.Entry(
        popup,
        textvariable=cpf_var,
        font=FONTBOX
    ).pack(pady=5)

    def confirmar():
        nome = nome_var.get().strip()
        cpf = cpf_var.get().strip()

        # Por enquanto, validamos o formato digitado do CPF.
        if not re.match(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", cpf):
            tk.Label(
                popup,
                text="Formato inválido!",
                fg="red",
                bg="white",
                font=("Segoe UI", 9, "bold")
            ).pack()
            return

        if nome and cpf:
            VENDEDORES.append((nome, cpf))
            salvar_vendedores()
            popular_lista()
            popup.destroy()

    tk.Button(
        popup,
        text="Confirmar",
        command=confirmar,
        bg=BTN_BG,
        fg=BTN_FG,
        font=FONT,
        activebackground=BTN_HOVER
    ).pack(pady=10)


# Exclusão de vendedores
def excluir_vendedor():
    popup = tk.Toplevel(root)
    popup.title("Excluir Vendedor")
    popup.geometry("300x250")
    popup.configure(bg="white")

    lista = tk.Listbox(popup, font=FONTBOX)
    lista.pack(fill="both", expand=True, padx=10, pady=10)

    for nome, cpf in VENDEDORES:
        lista.insert("end", f"{nome} - {cpf}")

    def confirmar():
        selecao = lista.curselection()

        if selecao:
            indice = selecao[0]
            VENDEDORES.pop(indice)
            salvar_vendedores()
            popular_lista()
            popup.destroy()

    tk.Button(
        popup,
        text="Excluir Selecionado",
        command=confirmar,
        bg="#b91c1c",
        fg="white",
        font=FONT,
        activebackground="#a11a1a"
    ).pack(pady=10)


# Botões de ação
frame_actions = tk.Frame(root, bg="white")
frame_actions.pack(pady=6)

tk.Button(
    frame_actions,
    text="Adicionar Vendedor",
    command=adicionar_vendedor,
    bg=BTN_BG,
    fg=BTN_FG,
    font=FONT,
    activebackground=BTN_HOVER
).pack(side="left", padx=10)

tk.Button(
    frame_actions,
    text="Excluir Vendedor",
    command=excluir_vendedor,
    bg="#b91c1c",
    fg="white",
    font=FONT,
    activebackground="#a11a1a"
).pack(side="left", padx=10)


# Atalhos do teclado
root.bind("<Escape>", lambda event: root.destroy())
root.bind("<Control-f>", lambda event: search_entry.focus_set())


# Centraliza a janela na tela
root.update_idletasks()

largura = root.winfo_width()
altura = root.winfo_height()

largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()

x = (largura_tela - largura) // 2
y = (altura_tela - altura) // 2

root.geometry(f"{largura}x{altura}+{x}+{y}")


# Carrega a lista inicial e inicia a interface.
popular_lista()
root.mainloop()