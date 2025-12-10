import customtkinter as ctk
from tkinter import messagebox
from typing import Any


def mostrar_login(app: Any):
    """Muestra la pantalla de inicio de sesión (módulo separado)"""
    app.limpiar_ventana()

    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(expand=True, fill="both", padx=40, pady=40)

    titulo = ctk.CTkLabel(
        frame,
        text="🏋️ GymForTheMoment",
        font=ctk.CTkFont(size=40, weight="bold")
    )
    titulo.pack(pady=(0, 10))

    subtitulo = ctk.CTkLabel(
        frame,
        text="Sistema de Gestión de Gimnasio 24/7",
        font=ctk.CTkFont(size=16)
    )
    subtitulo.pack(pady=(0, 40))

    login_frame = ctk.CTkFrame(frame, width=400)
    login_frame.pack(pady=20)

    ctk.CTkLabel(
        login_frame,
        text="Iniciar Sesión",
        font=ctk.CTkFont(size=24, weight="bold")
    ).pack(pady=(30, 20))

    dni_entry = ctk.CTkEntry(
        login_frame,
        placeholder_text="DNI",
        width=300,
        height=40,
        font=ctk.CTkFont(size=14)
    )
    dni_entry.pack(pady=10, padx=40)

    password_entry = ctk.CTkEntry(
        login_frame,
        placeholder_text="Contraseña",
        show="*",
        width=300,
        height=40,
        font=ctk.CTkFont(size=14)
    )
    password_entry.pack(pady=10, padx=40)

    # Botón de login
    def login_action():
        dni = dni_entry.get()
        password = password_entry.get()

        exito, mensaje, usuario = app.controller.login(dni, password)

        if exito:
            if app.controller.es_admin():
                app.mostrar_dashboard_admin()
            else:
                app.mostrar_dashboard_cliente()
        else:
            messagebox.showerror("Error", mensaje)

    btn_login = ctk.CTkButton(
        login_frame,
        text="Ingresar",
        command=login_action,
        width=300,
        height=40,
        font=ctk.CTkFont(size=14, weight="bold")
    )
    btn_login.pack(pady=20, padx=40)

    # Botón de registro (usa la función del mismo módulo)
    btn_registro = ctk.CTkButton(
        login_frame,
        text="Crear Cuenta Nueva",
        command=lambda: mostrar_registro(app),
        width=300,
        height=40,
        font=ctk.CTkFont(size=14),
        fg_color="transparent",
        border_width=2
    )
    btn_registro.pack(pady=(0, 30), padx=40)

    info = ctk.CTkLabel(
        frame,
        text="👤 Admin: DNI: admin123 | Contraseña: admin123",
        font=ctk.CTkFont(size=12),
        text_color="gray"
    )
    info.pack(pady=20)

    password_entry.bind("<Return>", lambda e: login_action())


def mostrar_registro(app: Any):
    """Muestra la pantalla de registro (módulo separado)"""
    app.limpiar_ventana()

    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(expand=True, fill="both", padx=40, pady=40)

    ctk.CTkLabel(
        frame,
        text="Crear Cuenta Nueva",
        font=ctk.CTkFont(size=32, weight="bold")
    ).pack(pady=(0, 30))

    reg_frame = ctk.CTkFrame(frame, width=500)
    reg_frame.pack(pady=20)

    nombre_entry = ctk.CTkEntry(reg_frame, placeholder_text="Nombre *", width=400, height=40)
    nombre_entry.pack(pady=10, padx=40)

    apellido_entry = ctk.CTkEntry(reg_frame, placeholder_text="Apellido *", width=400, height=40)
    apellido_entry.pack(pady=10, padx=40)

    dni_entry = ctk.CTkEntry(reg_frame, placeholder_text="DNI *", width=400, height=40)
    dni_entry.pack(pady=10, padx=40)

    telefono_entry = ctk.CTkEntry(reg_frame, placeholder_text="Teléfono", width=400, height=40)
    telefono_entry.pack(pady=10, padx=40)

    email_entry = ctk.CTkEntry(reg_frame, placeholder_text="Email", width=400, height=40)
    email_entry.pack(pady=10, padx=40)

    password_entry = ctk.CTkEntry(reg_frame, placeholder_text="Contraseña *", show="*", width=400, height=40)
    password_entry.pack(pady=10, padx=40)

    def registrar_action():
        exito, mensaje = app.controller.registrar_usuario(
            nombre_entry.get(),
            apellido_entry.get(),
            dni_entry.get(),
            telefono_entry.get(),
            email_entry.get(),
            password_entry.get()
        )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            mostrar_login(app)
        else:
            messagebox.showerror("Error", mensaje)

    btn_frame = ctk.CTkFrame(reg_frame, fg_color="transparent")
    btn_frame.pack(pady=30, padx=40)

    ctk.CTkButton(
        btn_frame,
        text="Registrarse",
        command=registrar_action,
        width=190,
        height=40,
        font=ctk.CTkFont(size=14, weight="bold")
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        btn_frame,
        text="Volver",
        command=lambda: mostrar_login(app),
        width=190,
        height=40,
        font=ctk.CTkFont(size=14),
        fg_color="gray",
        hover_color="darkgray"
    ).pack(side="left", padx=5)
