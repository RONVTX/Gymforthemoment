import customtkinter as ctk


def crear_boton_menu(parent, texto, comando, icono=""):
    btn = ctk.CTkButton(
        parent,
        text=f"{icono} {texto}",
        command=comando,
        width=210,
        height=45,
        font=ctk.CTkFont(size=14),
        anchor="w",
        fg_color="transparent",
        hover_color=("#3b8ed0", "#1f6aa5")
    )
    btn.pack(pady=5, padx=20)
    return btn


def crear_boton_admin(parent, texto, comando, icono=""):
    btn = ctk.CTkButton(
        parent,
        text=f"{icono} {texto}",
        command=comando,
        width=210,
        height=45,
        font=ctk.CTkFont(size=13),
        anchor="w",
        fg_color="transparent",
        hover_color=("#3b8ed0", "#1f6aa5")
    )
    btn.pack(pady=5, padx=20)
    return btn


def crear_stat_card(parent, icono, valor, texto, color="blue"):
    card = ctk.CTkFrame(parent)

    ctk.CTkLabel(card, text=icono, font=ctk.CTkFont(size=40)).pack(pady=(15, 5))

    ctk.CTkLabel(
        card,
        text=str(valor),
        font=ctk.CTkFont(size=36, weight="bold"),
        text_color=color
    ).pack()

    ctk.CTkLabel(
        card,
        text=texto,
        font=ctk.CTkFont(size=14)
    ).pack(pady=(0, 15))

    return card
