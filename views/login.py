import customtkinter as ctk
from tkinter import messagebox
from typing import Any


def mostrar_login(app: Any):
    """Muestra la pantalla de inicio de sesión mejorada visualmente"""
    app.limpiar_ventana()
    app.configure(fg_color="#0a0e27")  # Fondo oscuro azulado

    # Frame principal con contenido centrado
    main_frame = ctk.CTkFrame(app, fg_color="#0a0e27")
    main_frame.pack(expand=True, fill="both")

    # Frame para el contenido (centrado)
    content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    content_frame.pack(expand=True, fill="both", padx=40, pady=40)

    # Encabezado con logo
    header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    header_frame.pack(pady=(0, 30))

    titulo = ctk.CTkLabel(
        header_frame,
        text="💪 GymForTheMoment",
        font=ctk.CTkFont(size=48, weight="bold"),
        text_color="#00d4ff"
    )
    titulo.pack()

    subtitulo = ctk.CTkLabel(
        header_frame,
        text="Tu Gimnasio, Tu Espacio, Tu Horario",
        font=ctk.CTkFont(size=15),
        text_color="#b0b8c1"
    )
    subtitulo.pack(pady=(8, 0))

    # Frame del formulario con fondo más claro y bordes redondeados
    login_frame = ctk.CTkFrame(
        content_frame,
        fg_color="#1a1f3a",
        corner_radius=20,
        border_width=2,
        border_color="#00d4ff"
    )
    login_frame.pack(pady=(30, 20), padx=20)

    # Encabezado del formulario
    form_header = ctk.CTkFrame(login_frame, fg_color="transparent")
    form_header.pack(pady=(30, 20), padx=40, fill="x")

    form_title = ctk.CTkLabel(
        form_header,
        text="🔐 Iniciar Sesión",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color="#ffffff"
    )
    form_title.pack(anchor="w")

    form_subtitle = ctk.CTkLabel(
        form_header,
        text="Accede a tu cuenta para comenzar",
        font=ctk.CTkFont(size=12),
        text_color="#7a8492"
    )
    form_subtitle.pack(anchor="w", pady=(5, 0))

    # Campos de entrada con estilo mejorado
    campos_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
    campos_frame.pack(pady=20, padx=40, fill="x")

    # Campo DNI con ícono
    dni_label = ctk.CTkLabel(
        campos_frame,
        text="👤 DNI",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color="#b0b8c1"
    )
    dni_label.pack(anchor="w", pady=(0, 5))

    dni_entry = ctk.CTkEntry(
        campos_frame,
        placeholder_text="Ingresa tu DNI",
        width=350,
        height=45,
        font=ctk.CTkFont(size=14),
        fg_color="#0f1428",
        border_color="#00d4ff",
        border_width=2,
        text_color="#ffffff",
        placeholder_text_color="#5a6270"
    )
    dni_entry.pack(pady=(0, 20), fill="x")

    # Campo Contraseña con ícono
    password_label = ctk.CTkLabel(
        campos_frame,
        text="🔑 Contraseña",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color="#b0b8c1"
    )
    password_label.pack(anchor="w", pady=(0, 5))

    password_entry = ctk.CTkEntry(
        campos_frame,
        placeholder_text="Ingresa tu contraseña",
        show="*",
        width=350,
        height=45,
        font=ctk.CTkFont(size=14),
        fg_color="#0f1428",
        border_color="#00d4ff",
        border_width=2,
        text_color="#ffffff",
        placeholder_text_color="#5a6270"
    )
    password_entry.pack(fill="x")

    # Botones
    botones_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
    botones_frame.pack(pady=30, padx=40, fill="x")

    def login_action():
        dni = dni_entry.get().strip()
        password = password_entry.get().strip()

        if not dni or not password:
            messagebox.showerror("Error", "Por favor completa todos los campos")
            return

        exito, mensaje, usuario = app.controller.login(dni, password)

        if exito:
            if app.controller.es_admin():
                app.mostrar_dashboard_admin()
            else:
                app.mostrar_dashboard_cliente()
        else:
            messagebox.showerror("Error de Autenticación", mensaje)

    btn_login = ctk.CTkButton(
        botones_frame,
        text="Ingresar Ahora",
        command=login_action,
        width=350,
        height=50,
        font=ctk.CTkFont(size=15, weight="bold"),
        fg_color="#00d4ff",
        text_color="#0a0e27",
        hover_color="#00b8d4",
        corner_radius=10
    )
    btn_login.pack(pady=(0, 15), fill="x")

    # Botón de registro con estilo secundario
    btn_registro = ctk.CTkButton(
        botones_frame,
        text="Crear Cuenta Nueva",
        command=lambda: mostrar_registro(app),
        width=350,
        height=45,
        font=ctk.CTkFont(size=14),
        fg_color="transparent",
        border_width=2,
        border_color="#00d4ff",
        text_color="#00d4ff",
        hover_color="#1a1f3a",
        corner_radius=10
    )
    btn_registro.pack(fill="x")

   

    # Vinculación de teclas
    password_entry.bind("<Return>", lambda e: login_action())
    dni_entry.bind("<Return>", lambda e: login_action())


def mostrar_registro(app: Any):
    """Muestra la pantalla de registro mejorada visualmente"""
    app.limpiar_ventana()
    app.configure(fg_color="#0a0e27")

    main_frame = ctk.CTkFrame(app, fg_color="#0a0e27")
    main_frame.pack(expand=True, fill="both")

    # Frame principal con scroll
    scroll_frame = ctk.CTkScrollableFrame(
        main_frame,
        fg_color="#0a0e27",
        label_text="",
        label_font=ctk.CTkFont(size=0)
    )
    scroll_frame.pack(expand=True, fill="both", padx=40, pady=40)

    # Encabezado
    titulo = ctk.CTkLabel(
        scroll_frame,
        text="✨ Crear Cuenta Nueva",
        font=ctk.CTkFont(size=44, weight="bold"),
        text_color="#00d4ff"
    )
    titulo.pack(pady=(0, 10))

    subtitulo = ctk.CTkLabel(
        scroll_frame,
        text="Únete a nuestra comunidad de fitness",
        font=ctk.CTkFont(size=13),
        text_color="#b0b8c1"
    )
    subtitulo.pack(pady=(0, 30))

    # Frame del formulario
    reg_frame = ctk.CTkFrame(
        scroll_frame,
        fg_color="#1a1f3a",
        corner_radius=20,
        border_width=2,
        border_color="#00d4ff"
    )
    reg_frame.pack(pady=20, padx=0, fill="x")

    # Contenedor de campos
    campos_frame = ctk.CTkFrame(reg_frame, fg_color="transparent")
    campos_frame.pack(pady=30, padx=40, fill="x")

    # Helper para crear campos etiquetados
    def create_labeled_entry(parent, label, placeholder, show_char=None):
        label_widget = ctk.CTkLabel(
            parent,
            text=label,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#b0b8c1"
        )
        label_widget.pack(anchor="w", pady=(0, 4))

        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            show=show_char,
            width=400,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="#0f1428",
            border_color="#00d4ff",
            border_width=1.5,
            text_color="#ffffff",
            placeholder_text_color="#5a6270"
        )
        entry.pack(pady=(0, 15), fill="x")
        return entry

    nombre_entry = create_labeled_entry(campos_frame, "👤 Nombre Completo *", "Ej: Juan")
    apellido_entry = create_labeled_entry(campos_frame, "👥 Apellido *", "Ej: García")
    dni_entry = create_labeled_entry(campos_frame, "🆔 DNI *", "Ej: 12345678")
    telefono_entry = create_labeled_entry(campos_frame, "📱 Teléfono", "Ej: +34 600000000")
    email_entry = create_labeled_entry(campos_frame, "📧 Email", "Ej: juan@example.com")
    password_entry = create_labeled_entry(campos_frame, "🔐 Contraseña *", "Mínimo 6 caracteres", show_char="*")

    # Botones
    botones_frame = ctk.CTkFrame(reg_frame, fg_color="transparent")
    botones_frame.pack(padx=40, pady=(0, 20), fill="x")

    def registrar_action():
        nombre = nombre_entry.get().strip()
        apellido = apellido_entry.get().strip()
        dni = dni_entry.get().strip()
        telefono = telefono_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not all([nombre, apellido, dni, password]):
            messagebox.showerror("Error", "Por favor completa los campos marcados con *")
            return

        exito, mensaje = app.controller.registrar_usuario(
            nombre, apellido, dni, telefono, email, password
        )

        if exito:
            messagebox.showinfo("¡Éxito!", "Cuenta creada correctamente. Ahora inicia sesión.")
            mostrar_login(app)
        else:
            messagebox.showerror("Error en Registro", mensaje)

    ctk.CTkButton(
        botones_frame,
        text="Crear Cuenta",
        command=registrar_action,
        width=190,
        height=45,
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color="#00d4ff",
        text_color="#0a0e27",
        hover_color="#00b8d4",
        corner_radius=10
    ).pack(side="left", padx=5, fill="x", expand=True)

    ctk.CTkButton(
        botones_frame,
        text="Volver al Login",
        command=lambda: mostrar_login(app),
        width=190,
        height=45,
        font=ctk.CTkFont(size=14),
        fg_color="transparent",
        border_width=2,
        border_color="#00d4ff",
        text_color="#00d4ff",
        hover_color="#1a1f3a",
        corner_radius=10
    ).pack(side="left", padx=5, fill="x", expand=True)

    # Notas de validación
    notes_frame = ctk.CTkFrame(reg_frame, fg_color="#0f1428", corner_radius=10)
    notes_frame.pack(padx=40, pady=(0, 0), fill="x")

    notes_title = ctk.CTkLabel(
        notes_frame,
        text="ℹ️ Requerimientos",
        font=ctk.CTkFont(size=10, weight="bold"),
        text_color="#00d4ff"
    )
    notes_title.pack(pady=(12, 6), anchor="w", padx=12)

    notes_text = ctk.CTkLabel(
        notes_frame,
        text="• Nombre, Apellido, DNI y Contraseña son requeridos\n• El DNI debe ser único en el sistema\n• La contraseña debe tener al menos 6 caracteres",
        font=ctk.CTkFont(size=9),
        text_color="#7a8492",
        justify="left"
    )
    notes_text.pack(pady=(0, 12), anchor="w", padx=12)

