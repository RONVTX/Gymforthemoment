import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from typing import Any
from views.components import crear_boton_admin, crear_stat_card


def mostrar_dashboard_admin(app: Any):
    app.limpiar_ventana()
    app.configure(fg_color="#0a0e27")

    # Frame principal
    main_frame = ctk.CTkFrame(app, fg_color="#0a0e27")
    main_frame.pack(fill="both", expand=True)

    # Sidebar mejorado
    sidebar = ctk.CTkFrame(main_frame, width=280, fg_color="#1a1f3a", corner_radius=0)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Admin info mejorado
    user_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    user_frame.pack(pady=30, padx=20, fill="x")

    ctk.CTkLabel(
        user_frame,
        text="ADMINISTRADOR",
        font=ctk.CTkFont(size=11, weight="bold"),
        text_color="#ffd700"
    ).pack(anchor="w", pady=(0, 10))

    usuario = app.controller.usuario_actual
    ctk.CTkLabel(
        user_frame,
        text=f"{usuario['nombre']} {usuario['apellido']}",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#ffffff"
    ).pack(anchor="w")

    ctk.CTkLabel(
        user_frame,
        text=f"DNI: {usuario['dni']}",
        font=ctk.CTkFont(size=11),
        text_color="#7a8492"
    ).pack(anchor="w", pady=(5, 0))

    # Separador
    ctk.CTkFrame(sidebar, fg_color="#2a2f4a", height=1).pack(fill="x", padx=20, pady=20)

    # Menú admin
    menu_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    menu_frame.pack(fill="both", expand=True, padx=15, pady=0)

    crear_boton_admin(menu_frame, "Dashboard", lambda: mostrar_contenido_admin(app, "dashboard"), "📊")
    crear_boton_admin(menu_frame, "Clientes", lambda: mostrar_contenido_admin(app, "clientes"), "👥")
    crear_boton_admin(menu_frame, "Aparatos", lambda: mostrar_contenido_admin(app, "aparatos"), "🏋️")
    crear_boton_admin(menu_frame, "Reservas", lambda: mostrar_contenido_admin(app, "reservas"), "📅")
    crear_boton_admin(menu_frame, "Recibos", lambda: mostrar_contenido_admin(app, "recibos"), "📄")
    crear_boton_admin(menu_frame, "Morosos", lambda: mostrar_contenido_admin(app, "morosos"), "⚠️")
    crear_boton_admin(menu_frame, "Horarios", lambda: mostrar_contenido_admin(app, "horarios"), "🕐")

    # Botón cerrar sesión mejorado
    ctk.CTkButton(
        sidebar,
        text="🚪 Cerrar Sesión",
        command=app.cerrar_sesion,
        width=240,
        height=45,
        font=ctk.CTkFont(size=13, weight="bold"),
        fg_color="#c41e3a",
        hover_color="#a01830",
        corner_radius=10
    ).pack(side="bottom", pady=20, padx=15)

    # Contenido
    app.content_frame = ctk.CTkFrame(main_frame, fg_color="#0a0e27")
    app.content_frame.pack(side="right", fill="both", expand=True, padx=30, pady=30)

    mostrar_contenido_admin(app, "dashboard")


def mostrar_contenido_admin(app: Any, seccion: str):
    for widget in app.content_frame.winfo_children():
        widget.destroy()

    if seccion == "dashboard":
        contenido_dashboard_admin(app)
    elif seccion == "clientes":
        contenido_admin_clientes(app)
    elif seccion == "aparatos":
        contenido_admin_aparatos(app)
    elif seccion == "reservas":
        contenido_admin_reservas(app)
    elif seccion == "recibos":
        contenido_admin_recibos(app)
    elif seccion == "morosos":
        contenido_admin_morosos(app)
    elif seccion == "horarios":
        from .client import contenido_horarios
        contenido_horarios(app)


def contenido_dashboard_admin(app: Any):
    """Dashboard admin mejorado con estadísticas"""
    # Título
    titulo_frame = ctk.CTkFrame(app.content_frame, fg_color="transparent")
    titulo_frame.pack(fill="x", pady=(0, 30))

    ctk.CTkLabel(
        titulo_frame,
        text="📊 Panel de Control",
        font=ctk.CTkFont(size=32, weight="bold"),
        text_color="#00d4ff"
    ).pack(anchor="w")

    ctk.CTkLabel(
        titulo_frame,
        text="Resumen general del gimnasio",
        font=ctk.CTkFont(size=13),
        text_color="#7a8492"
    ).pack(anchor="w", pady=(5, 0))

    stats = app.controller.obtener_estadisticas_generales()

    # Grid de estadísticas
    stats_grid = ctk.CTkFrame(app.content_frame, fg_color="transparent")
    stats_grid.pack(fill="x", pady=(0, 30))

    # Fila 1
    row1 = ctk.CTkFrame(stats_grid, fg_color="transparent")
    row1.pack(fill="x", pady=(0, 15))

    crear_stat_card(row1, "👥", stats['total_clientes'], "Clientes", "#00d4ff").pack(side="left", fill="both", expand=True, padx=(0, 15))
    crear_stat_card(row1, "🏋️", stats['total_aparatos'], "Aparatos", "#00d4ff").pack(side="left", fill="both", expand=True, padx=(0, 15))
    crear_stat_card(row1, "📅", stats['total_reservas'], "Reservas", "#00d4ff").pack(side="left", fill="both", expand=True)

    # Fila 2
    row2 = ctk.CTkFrame(stats_grid, fg_color="transparent")
    row2.pack(fill="x", pady=(0, 15))

    crear_stat_card(row2, "📄", stats['total_recibos'], "Recibos Totales", "#ffd700").pack(side="left", fill="both", expand=True, padx=(0, 15))
    crear_stat_card(row2, "✅", stats['recibos_pagados'], "Pagados", "#2dbe60").pack(side="left", fill="both", expand=True, padx=(0, 15))
    crear_stat_card(row2, "⚠️", stats['total_morosos'], "Morosos", "#c41e3a").pack(side="left", fill="both", expand=True)

    # Fila 3 - Financiero
    row3 = ctk.CTkFrame(stats_grid, fg_color="transparent")
    row3.pack(fill="x")

    crear_stat_card(row3, "💰", f"€{stats['total_ingresos']:.2f}", "Ingresos", "#2dbe60").pack(side="left", fill="both", expand=True, padx=(0, 15))
    crear_stat_card(row3, "📉", f"€{stats['deuda_total']:.2f}", "Deuda Pendiente", "#c41e3a").pack(side="left", fill="both", expand=True)

    # Botones de acción rápida
    action_frame = ctk.CTkFrame(app.content_frame, fg_color="transparent")
    action_frame.pack(fill="x", pady=(30, 0))

    ctk.CTkButton(
        action_frame,
        text="📄 Generar Recibos",
        command=lambda: generar_recibos_dialog(app),
        width=220,
        height=50,
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color="#2dbe60",
        text_color="#ffffff",
        hover_color="#229d47",
        corner_radius=10
    ).pack(side="left", padx=(0, 15))

    ctk.CTkButton(
        action_frame,
        text="⚠️ Ver Morosos",
        command=lambda: mostrar_contenido_admin(app, "morosos"),
        width=220,
        height=50,
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color="#c41e3a",
        text_color="#ffffff",
        hover_color="#a01830",
        corner_radius=10
    ).pack(side="left")


def generar_recibos_dialog(app: Any):
    dialog = ctk.CTkToplevel(app)
    dialog.title("Generar Recibos")
    dialog.geometry("450x350")
    dialog.configure(fg_color="#0a0e27")
    dialog.transient(app)
    dialog.grab_set()

    ctk.CTkLabel(
        dialog,
        text="📄 Generar Recibos Mensuales",
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color="#00d4ff"
    ).pack(pady=20)

    # Mes
    ctk.CTkLabel(
        dialog,
        text="📅 Mes:",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color="#b0b8c1"
    ).pack(pady=(10, 5))
    
    mes_combo = ctk.CTkComboBox(
        dialog,
        values=[str(i) for i in range(1, 13)],
        width=300,
        height=40,
        font=ctk.CTkFont(size=12),
        fg_color="#1a1f3a",
        border_color="#00d4ff",
        border_width=1.5
    )
    mes_combo.set(str(datetime.now().month))
    mes_combo.pack()

    # Año
    ctk.CTkLabel(
        dialog,
        text="📆 Año:",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color="#b0b8c1"
    ).pack(pady=(15, 5))
    
    anio_combo = ctk.CTkComboBox(
        dialog,
        values=[str(i) for i in range(2024, 2027)],
        width=300,
        height=40,
        font=ctk.CTkFont(size=12),
        fg_color="#1a1f3a",
        border_color="#00d4ff",
        border_width=1.5
    )
    anio_combo.set(str(datetime.now().year))
    anio_combo.pack()

    def generar():
        mes = int(mes_combo.get())
        anio = int(anio_combo.get())

        exito, mensaje = app.controller.generar_recibos_mes(mes, anio)

        if exito:
            messagebox.showinfo("¡Éxito!", mensaje)
            dialog.destroy()
            mostrar_contenido_admin(app, "dashboard")
        else:
            messagebox.showerror("Error", mensaje)

    ctk.CTkButton(
        dialog,
        text="✅ Generar Recibos",
        command=generar,
        width=300,
        height=45,
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color="#00d4ff",
        text_color="#0a0e27",
        hover_color="#00b8d4",
        corner_radius=10
    ).pack(pady=30)


def contenido_admin_clientes(app: Any):
    """Gestión de clientes"""
    header = ctk.CTkFrame(app.content_frame, fg_color="transparent")
    header.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(
        header,
        text="👥 Gestión de Clientes",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color="#00d4ff"
    ).pack(side="left")

    ctk.CTkButton(
        header,
        text="➕ Nuevo Cliente",
        command=lambda: nuevo_cliente_dialog(app),
        width=180,
        height=45,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color="#00d4ff",
        text_color="#0a0e27",
        hover_color="#00b8d4",
        corner_radius=10
    ).pack(side="right")

    scroll_frame = ctk.CTkScrollableFrame(app.content_frame, fg_color="transparent")
    scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

    clientes = app.controller.obtener_clientes()

    if not clientes:
        ctk.CTkLabel(
            scroll_frame,
            text="No hay clientes en el sistema",
            font=ctk.CTkFont(size=16),
            text_color="#7a8492"
        ).pack(pady=40)
        return

    for cliente in clientes:
        tipo_emoji = "👑" if cliente['tipo'] == 'admin' else "👤"
        
        card = ctk.CTkFrame(
            scroll_frame,
            fg_color="#1a1f3a",
            corner_radius=12,
            border_width=2,
            border_color="#00d4ff"
        )
        card.pack(fill="x", pady=10, padx=0)

        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)

        titulo = f"{tipo_emoji} {cliente['nombre']} {cliente['apellido']}"
        ctk.CTkLabel(
            content_frame,
            text=titulo,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w")

        detalles = f"🆔 DNI: {cliente['dni']} | 📱 {cliente['telefono']} | 📧 {cliente['email']}"
        ctk.CTkLabel(
            content_frame,
            text=detalles,
            font=ctk.CTkFont(size=11),
            text_color="#7a8492"
        ).pack(anchor="w", pady=(5, 0))

        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(10, 0))

        if cliente['tipo'] != 'admin':
            ctk.CTkButton(
                button_frame,
                text="❌ Eliminar",
                command=lambda c=cliente: eliminar_cliente(app, c['id']),
                width=100,
                height=35,
                font=ctk.CTkFont(size=11),
                fg_color="#c41e3a",
                hover_color="#a01830",
                corner_radius=8
            ).pack(side="left")


def nuevo_cliente_dialog(app: Any):
    dialog = ctk.CTkToplevel(app)
    dialog.title("Nuevo Cliente")
    dialog.geometry("500x650")
    dialog.configure(fg_color="#0a0e27")
    dialog.transient(app)
    dialog.grab_set()

    ctk.CTkLabel(
        dialog,
        text="👤 Crear Nuevo Cliente",
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color="#00d4ff"
    ).pack(pady=20)

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
            font=ctk.CTkFont(size=12),
            fg_color="#1a1f3a",
            border_color="#00d4ff",
            border_width=1.5,
            text_color="#ffffff",
            placeholder_text_color="#5a6270"
        )
        entry.pack(pady=(0, 15), fill="x")
        return entry

    frame = ctk.CTkFrame(dialog, fg_color="transparent")
    frame.pack(pady=20, padx=30, fill="both", expand=True)

    nombre = create_labeled_entry(frame, "Nombre *", "Ej: Juan")
    apellido = create_labeled_entry(frame, "Apellido *", "Ej: García")
    dni = create_labeled_entry(frame, "DNI *", "Ej: 12345678A")
    telefono = create_labeled_entry(frame, "Teléfono", "Ej: +34 600000000")
    email = create_labeled_entry(frame, "Email", "Ej: juan@example.com")
    password = create_labeled_entry(frame, "Contraseña *", "Mínimo 6 caracteres", show_char="*")

    ctk.CTkLabel(
        frame,
        text="Tipo de Usuario:",
        font=ctk.CTkFont(size=11, weight="bold"),
        text_color="#b0b8c1"
    ).pack(anchor="w", pady=(0, 4))
    
    tipo = ctk.CTkComboBox(
        frame,
        values=['cliente', 'admin'],
        width=400,
        height=40,
        font=ctk.CTkFont(size=12),
        fg_color="#1a1f3a",
        border_color="#00d4ff",
        border_width=1.5
    )
    tipo.set('cliente')
    tipo.pack(pady=(0, 20), fill="x")

    def crear():
        if not all([nombre.get(), apellido.get(), dni.get(), password.get()]):
            messagebox.showerror("Error", "Complete todos los campos marcados con *")
            return

        exito, mensaje = app.controller.crear_cliente_admin(
            nombre.get(), apellido.get(), dni.get(),
            telefono.get(), email.get(), password.get(), tipo.get()
        )

        if exito:
            messagebox.showinfo("¡Éxito!", "Cliente creado correctamente")
            dialog.destroy()
            mostrar_contenido_admin(app, "clientes")
        else:
            messagebox.showerror("Error", mensaje)

    ctk.CTkButton(
        frame,
        text="✅ Crear Cliente",
        command=crear,
        width=400,
        height=45,
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color="#00d4ff",
        text_color="#0a0e27",
        hover_color="#00b8d4",
        corner_radius=10
    ).pack()


def contenido_admin_aparatos(app: Any):
    """Gestión de aparatos"""
    header = ctk.CTkFrame(app.content_frame, fg_color="transparent")
    header.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(
        header,
        text="🏋️ Gestión de Aparatos",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color="#00d4ff"
    ).pack(side="left")

    ctk.CTkButton(
        header,
        text="➕ Nuevo Aparato",
        command=lambda: nuevo_aparato_dialog(app),
        width=180,
        height=45,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color="#00d4ff",
        text_color="#0a0e27",
        hover_color="#00b8d4",
        corner_radius=10
    ).pack(side="right")

    scroll_frame = ctk.CTkScrollableFrame(app.content_frame, fg_color="transparent")
    scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

    aparatos = app.controller.obtener_aparatos()

    if not aparatos:
        ctk.CTkLabel(
            scroll_frame,
            text="No hay aparatos en el sistema",
            font=ctk.CTkFont(size=16),
            text_color="#7a8492"
        ).pack(pady=40)
        return

    for aparato in aparatos:
        card = ctk.CTkFrame(
            scroll_frame,
            fg_color="#1a1f3a",
            corner_radius=12,
            border_width=2,
            border_color="#00d4ff"
        )
        card.pack(fill="x", pady=10, padx=0)

        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)

        titulo = f"🏋️ {aparato['nombre']}"
        ctk.CTkLabel(
            content_frame,
            text=titulo,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w")

        detalles = f"Tipo: {aparato['tipo']} | {aparato['descripcion']}"
        ctk.CTkLabel(
            content_frame,
            text=detalles,
            font=ctk.CTkFont(size=11),
            text_color="#7a8492"
        ).pack(anchor="w", pady=(5, 0))

        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(10, 0))

        ctk.CTkButton(
            button_frame,
            text="❌ Eliminar",
            command=lambda a=aparato: eliminar_aparato(app, a['id']),
            width=100,
            height=35,
            font=ctk.CTkFont(size=11),
            fg_color="#c41e3a",
            hover_color="#a01830",
            corner_radius=8
        ).pack(side="left")


def nuevo_aparato_dialog(app: Any):
    dialog = ctk.CTkToplevel(app)
    dialog.title("Nuevo Aparato")
    dialog.geometry("500x450")
    dialog.configure(fg_color="#0a0e27")
    dialog.transient(app)
    dialog.grab_set()

    ctk.CTkLabel(
        dialog,
        text="🏋️ Crear Nuevo Aparato",
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color="#00d4ff"
    ).pack(pady=20)

    def create_labeled_entry(parent, label, placeholder):
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
            width=350,
            height=40,
            font=ctk.CTkFont(size=12),
            fg_color="#1a1f3a",
            border_color="#00d4ff",
            border_width=1.5,
            text_color="#ffffff",
            placeholder_text_color="#5a6270"
        )
        entry.pack(pady=(0, 15), fill="x")
        return entry

    frame = ctk.CTkFrame(dialog, fg_color="transparent")
    frame.pack(pady=20, padx=30, fill="both", expand=True)

    nombre = create_labeled_entry(frame, "Nombre *", "Ej: Banca de Pesas")
    tipo = create_labeled_entry(frame, "Tipo *", "Ej: Pesas, Cardio, etc")
    descripcion = create_labeled_entry(frame, "Descripción", "Descripción del aparato")

    def crear():
        if not nombre.get() or not tipo.get():
            messagebox.showerror("Error", "Nombre y Tipo son obligatorios")
            return

        exito, mensaje = app.controller.crear_aparato(
            nombre.get(), tipo.get(), descripcion.get()
        )

        if exito:
            messagebox.showinfo("¡Éxito!", "Aparato creado correctamente")
            dialog.destroy()
            mostrar_contenido_admin(app, "aparatos")
        else:
            messagebox.showerror("Error", mensaje)

    ctk.CTkButton(
        frame,
        text="✅ Crear Aparato",
        command=crear,
        width=350,
        height=45,
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color="#00d4ff",
        text_color="#0a0e27",
        hover_color="#00b8d4",
        corner_radius=10
    ).pack()


def eliminar_aparato(app: Any, id_aparato: int):
    if messagebox.askyesno("Confirmar", "¿Desea eliminar este aparato?"):
        exito, mensaje = app.controller.eliminar_aparato(id_aparato)
        if exito:
            messagebox.showinfo("Éxito", "Aparato eliminado")
            mostrar_contenido_admin(app, "aparatos")
        else:
            messagebox.showerror("Error", mensaje)


def contenido_admin_reservas(app: Any):
    """Gestión de reservas con aprobación"""
    header = ctk.CTkFrame(app.content_frame, fg_color="transparent")
    header.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(
        header,
        text="📅 Gestión de Reservas",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color="#00d4ff"
    ).pack(side="left")

    ctk.CTkButton(
        header,
        text="➕ Nueva Reserva",
        command=lambda: nueva_reserva_admin_dialog(app),
        width=180,
        height=45,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color="#00d4ff",
        text_color="#0a0e27",
        hover_color="#00b8d4",
        corner_radius=10
    ).pack(side="right")

    scroll_frame = ctk.CTkScrollableFrame(app.content_frame, fg_color="transparent")
    scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

    # Reservas Pendientes
    ctk.CTkLabel(
        scroll_frame,
        text="⏳ PENDIENTES DE APROBACIÓN",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#ff9800"
    ).pack(anchor="w", pady=(20, 10), padx=0)

    reservas_pendientes = app.controller.obtener_reservas_pendientes()
    
    if reservas_pendientes:
        for reserva in reservas_pendientes:
            card = ctk.CTkFrame(
                scroll_frame,
                fg_color="#1a1f3a",
                corner_radius=12,
                border_width=2,
                border_color="#ff9800"
            )
            card.pack(fill="x", pady=10, padx=0)

            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="both", expand=True, padx=20, pady=15)

            titulo = f"👤 {reserva['cliente']} | 🏋️ {reservato['aparato']}"
            ctk.CTkLabel(
                content,
                text=titulo,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#ffffff"
            ).pack(anchor="w")

            detalles = f"📅 {reserva['dia']} | ⏰ {reserva['hora_inicio']} - {reserva['hora_fin']}"
            ctk.CTkLabel(
                content,
                text=detalles,
                font=ctk.CTkFont(size=11),
                text_color="#7a8492"
            ).pack(anchor="w", pady=(5, 0))

            buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
            buttons_frame.pack(fill="x", padx=20, pady=(10, 0))

            ctk.CTkButton(
                buttons_frame,
                text="✅ Aceptar",
                command=lambda r=reserva: admin_aceptar_reserva(app, r['id']),
                width=90,
                height=35,
                font=ctk.CTkFont(size=11),
                fg_color="#2dbe60",
                hover_color="#229d47",
                corner_radius=8
            ).pack(side="left", padx=(0, 10))

            ctk.CTkButton(
                buttons_frame,
                text="❌ Rechazar",
                command=lambda r=reserva: admin_rechazar_reserva(app, r['id']),
                width=90,
                height=35,
                font=ctk.CTkFont(size=11),
                fg_color="#c41e3a",
                hover_color="#a01830",
                corner_radius=8
            ).pack(side="left")
    else:
        ctk.CTkLabel(
            scroll_frame,
            text="No hay reservas pendientes",
            font=ctk.CTkFont(size=12),
            text_color="#7a8492"
        ).pack(pady=20, padx=10)

    # Reservas Aceptadas
    ctk.CTkLabel(
        scroll_frame,
        text="✅ RESERVAS ACEPTADAS",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#2dbe60"
    ).pack(anchor="w", pady=(30, 10), padx=0)

    reservas = app.controller.obtener_todas_reservas()
    reservas_aceptadas = [r for r in reservas if r.get('estado') == 'aceptada']

    if reservas_aceptadas:
        for reserva in reservas_aceptadas:
            card = ctk.CTkFrame(
                scroll_frame,
                fg_color="#1a1f3a",
                corner_radius=12,
                border_width=1,
                border_color="#2dbe60"
            )
            card.pack(fill="x", pady=10, padx=0)

            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="both", expand=True, padx=20, pady=15)

            titulo = f"👤 {reserva['cliente']} | 🏋️ {reserva['aparato']}"
            ctk.CTkLabel(
                content,
                text=titulo,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#ffffff"
            ).pack(anchor="w")

            detalles = f"📅 {reserva['dia']} | ⏰ {reserva['hora_inicio']} - {reserva['hora_fin']}"
            ctk.CTkLabel(
                content,
                text=detalles,
                font=ctk.CTkFont(size=11),
                text_color="#7a8492"
            ).pack(anchor="w", pady=(5, 0))

            button_frame = ctk.CTkFrame(card, fg_color="transparent")
            button_frame.pack(fill="x", padx=20, pady=(10, 0))

            ctk.CTkButton(
                button_frame,
                text="🗑️ Eliminar",
                command=lambda r=reserva: admin_eliminar_reserva(app, r['id']),
                width=100,
                height=35,
                font=ctk.CTkFont(size=11),
                fg_color="#c41e3a",
                hover_color="#a01830",
                corner_radius=8
            ).pack(side="left")
    else:
        ctk.CTkLabel(
            scroll_frame,
            text="No hay reservas aceptadas",
            font=ctk.CTkFont(size=12),
            text_color="#7a8492"
        ).pack(pady=20, padx=10)


def admin_aceptar_reserva(app: Any, id_reserva: int):
    exito, mensaje = app.controller.aceptar_reserva(id_reserva)
    if exito:
        messagebox.showinfo("Éxito", "Reserva aceptada")
        mostrar_contenido_admin(app, "reservas")
    else:
        messagebox.showerror("Error", mensaje)


def admin_rechazar_reserva(app: Any, id_reserva: int):
    if messagebox.askyesno("Confirmar", "¿Rechazar esta reserva?"):
        exito, mensaje = app.controller.rechazar_reserva(id_reserva)
        if exito:
            messagebox.showinfo("Éxito", "Reserva rechazada")
            mostrar_contenido_admin(app, "reservas")
        else:
            messagebox.showerror("Error", mensaje)


def admin_eliminar_reserva(app: Any, id_reserva: int):
    if messagebox.askyesno("Confirmar", "¿Eliminar esta reserva?"):
        exito, mensaje = app.controller.eliminar_reserva(id_reserva)
        if exito:
            messagebox.showinfo("Éxito", "Reserva eliminada")
            mostrar_contenido_admin(app, "reservas")
        else:
            messagebox.showerror("Error", mensaje)


def contenido_admin_recibos(app: Any):
    """Gestión de recibos con opción de crear facturas"""
    header = ctk.CTkFrame(app.content_frame, fg_color="transparent")
    header.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(
        header,
        text="📄 Todos los Recibos",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color="#00d4ff"
    ).pack(side="left")

    ctk.CTkButton(
        header,
        text="➕ Crear Factura",
        command=lambda: crear_factura_dialog(app),
        width=180,
        height=45,
        font=ctk.CTkFont(size=12, weight="bold"),
        fg_color="#00d4ff",
        text_color="#0a0e27",
        hover_color="#00b8d4",
        corner_radius=10
    ).pack(side="right")

    scroll_frame = ctk.CTkScrollableFrame(app.content_frame, fg_color="transparent")
    scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

    recibos = app.controller.obtener_todos_recibos()

    if not recibos:
        ctk.CTkLabel(
            scroll_frame,
            text="No hay recibos en el sistema",
            font=ctk.CTkFont(size=16),
            text_color="#7a8492"
        ).pack(pady=40)
        return

    for recibo in recibos:
        mes_nombre = app.controller.obtener_nombre_mes(recibo['mes'])
        
        border_color = "#c41e3a" if recibo['estado'] == 'pendiente' else "#2dbe60"

        card = ctk.CTkFrame(
            scroll_frame,
            fg_color="#1a1f3a",
            corner_radius=12,
            border_width=2,
            border_color=border_color
        )
        card.pack(fill="x", pady=10, padx=0)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=15)

        titulo = f"📄 {recibo['cliente']} - {mes_nombre} {recibo['anio']}"
        ctk.CTkLabel(
            content,
            text=titulo,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w")

        detalles = f"💰 €{recibo['monto']:.2f}"
        ctk.CTkLabel(
            content,
            text=detalles,
            font=ctk.CTkFont(size=11),
            text_color="#7a8492"
        ).pack(anchor="w", pady=(5, 0))

        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(10, 0))

        if recibo['estado'] == 'pendiente':
            ctk.CTkButton(
                button_frame,
                text="✅ Pagar",
                command=lambda r=recibo: pagar_recibo_admin(app, r['id']),
                width=80,
                height=35,
                font=ctk.CTkFont(size=11),
                fg_color="#2dbe60",
                hover_color="#229d47",
                corner_radius=8
            ).pack(side="left", padx=(0, 10))
        else:
            ctk.CTkLabel(
                button_frame,
                text="✅ PAGADO",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#2dbe60"
            ).pack(side="left")

        # Botón para descargar/ver factura
        ctk.CTkButton(
            button_frame,
            text="📥 Descargar",
            command=lambda r=recibo: descargar_factura(app, r['id']),
            width=100,
            height=35,
            font=ctk.CTkFont(size=11),
            fg_color="#ffd700",
            text_color="#0a0e27",
            hover_color="#ffed4e",
            corner_radius=8
        ).pack(side="right")


def crear_factura_dialog(app: Any):
    """Diálogo para crear una nueva factura manual para un cliente"""
    dialog = ctk.CTkToplevel(app)
    dialog.title("Crear Factura")
    dialog.geometry("550x750")
    dialog.configure(fg_color="#0a0e27")
    dialog.transient(app)
    dialog.grab_set()

    ctk.CTkLabel(
        dialog,
        text="📄 Crear Nueva Factura",
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color="#00d4ff"
    ).pack(pady=20)

    scroll_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
    scroll_frame.pack(fill="both", expand=True, padx=30, pady=0)

    def create_labeled_entry(parent, label, placeholder, is_number=False):
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
            width=400,
            height=40,
            font=ctk.CTkFont(size=12),
            fg_color="#1a1f3a",
            border_color="#00d4ff",
            border_width=1.5,
            text_color="#ffffff",
            placeholder_text_color="#5a6270"
        )
        entry.pack(pady=(0, 15), fill="x")
        return entry

    def create_labeled_combo(parent, label, values):
        label_widget = ctk.CTkLabel(
            parent,
            text=label,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#b0b8c1"
        )
        label_widget.pack(anchor="w", pady=(0, 4))

        combo = ctk.CTkComboBox(
            parent,
            values=values,
            width=400,
            height=40,
            font=ctk.CTkFont(size=12),
            fg_color="#1a1f3a",
            border_color="#00d4ff",
            border_width=1.5,
            text_color="#ffffff"
        )
        combo.pack(pady=(0, 15), fill="x")
        return combo

    # Cliente
    clientes = app.controller.obtener_clientes()
    cliente_options = [f"{c['nombre']} {c['apellido']} (DNI: {c['dni']})" for c in clientes]
    cliente_combo = create_labeled_combo(scroll_frame, "👤 Cliente *", cliente_options)

    # Concepto
    concepto = create_labeled_entry(scroll_frame, "📋 Concepto de la Factura *", "Ej: Cuota Mensual Gimnasio")

    # Monto
    monto = create_labeled_entry(scroll_frame, "💰 Monto (€) *", "Ej: 50.00")

    # Mes
    mes_combo = create_labeled_combo(
        scroll_frame,
        "📅 Mes *",
        [str(i) for i in range(1, 13)]
    )
    mes_combo.set(str(datetime.now().month))

    # Año
    anio_combo = create_labeled_combo(
        scroll_frame,
        "📆 Año *",
        [str(i) for i in range(2024, 2027)]
    )
    anio_combo.set(str(datetime.now().year))

    # Descripción
    desc_label = ctk.CTkLabel(
        scroll_frame,
        text="📝 Descripción (Opcional)",
        font=ctk.CTkFont(size=11, weight="bold"),
        text_color="#b0b8c1"
    )
    desc_label.pack(anchor="w", pady=(0, 4))

    descripcion = ctk.CTkTextbox(
        scroll_frame,
        width=400,
        height=100,
        font=ctk.CTkFont(size=11),
        fg_color="#1a1f3a",
        border_color="#00d4ff",
        border_width=1.5,
        text_color="#ffffff"
    )
    descripcion.pack(pady=(0, 20), fill="both")

    # Frame para botones
    button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
    button_frame.pack(pady=20, padx=30, fill="x")

    def crear():
        if not cliente_combo.get() or not concepto.get() or not monto.get():
            messagebox.showerror("Error", "Complete los campos requeridos (*)")
            return

        try:
            # Validar que el monto sea un número válido
            monto_float = float(monto.get())
            if monto_float <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a 0")
                return

            # Extraer índice del cliente
            cliente_idx = cliente_options.index(cliente_combo.get())
            id_cliente = clientes[cliente_idx]['id']

            # Crear recibo
            mes = int(mes_combo.get())
            anio = int(anio_combo.get())
            desc = descripcion.get("1.0", "end").strip()

            exito, mensaje = app.controller.crear_recibo_manual(
                id_cliente=id_cliente,
                concepto=concepto.get(),
                monto=monto_float,
                mes=mes,
                anio=anio,
                descripcion=desc
            )

            if exito:
                messagebox.showinfo("¡Éxito!", "Factura creada correctamente")
                dialog.destroy()
                mostrar_contenido_admin(app, "recibos")
            else:
                messagebox.showerror("Error", mensaje)

        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear factura: {str(e)}")

    ctk.CTkButton(
        button_frame,
        text="✅ Crear Factura",
        command=crear,
        width=200,
        height=45,
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color="#00d4ff",
        text_color="#0a0e27",
        hover_color="#00b8d4",
        corner_radius=10
    ).pack(side="left", padx=(0, 10))

    ctk.CTkButton(
        button_frame,
        text="❌ Cancelar",
        command=dialog.destroy,
        width=150,
        height=45,
        font=ctk.CTkFont(size=14),
        fg_color="#555555",
        hover_color="#444444",
        corner_radius=10
    ).pack(side="left")


def descargar_factura(app: Any, id_recibo: int):
    """Descarga o abre la factura en PDF"""
    try:
        exito, ruta = app.controller.generar_pdf_factura(id_recibo)
        if exito:
            messagebox.showinfo("Éxito", f"Factura generada: {ruta}")
        else:
            messagebox.showwarning("Advertencia", "No se pudo generar la factura PDF")
    except Exception as e:
        messagebox.showerror("Error", f"Error al descargar factura: {str(e)}")



def contenido_admin_morosos(app: Any):
    """Muestra clientes morosos"""
    ctk.CTkLabel(
        app.content_frame,
        text="⚠️ Clientes Morosos",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color="#c41e3a"
    ).pack(pady=(0, 20))

    scroll_frame = ctk.CTkScrollableFrame(app.content_frame, fg_color="transparent")
    scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

    morosos = app.controller.obtener_morosos()

    if not morosos:
        ctk.CTkLabel(
            scroll_frame,
            text="✅ No hay clientes morosos",
            font=ctk.CTkFont(size=18),
            text_color="#2dbe60"
        ).pack(pady=40)
        return

    for moroso in morosos:
        card = ctk.CTkFrame(
            scroll_frame,
            fg_color="#1a1f3a",
            corner_radius=12,
            border_width=2,
            border_color="#c41e3a"
        )
        card.pack(fill="x", pady=10, padx=0)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=15)

        titulo = f"⚠️ {moroso['nombre']} {moroso['apellido']}"
        ctk.CTkLabel(
            content,
            text=titulo,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w")

        detalles = f"🆔 DNI: {moroso['dni']} | 📱 {moroso['telefono']}"
        ctk.CTkLabel(
            content,
            text=detalles,
            font=ctk.CTkFont(size=11),
            text_color="#7a8492"
        ).pack(anchor="w", pady=(3, 3))

        deuda = f"📋 {moroso['recibos_pendientes']} recibos pendientes | 💰 Deuda: €{moroso['deuda_total']:.2f}"
        ctk.CTkLabel(
            content,
            text=deuda,
            font=ctk.CTkFont(size=11),
            text_color="#c41e3a"
        ).pack(anchor="w", pady=(3, 0))


def eliminar_cliente(app: Any, id_cliente: int):
    if messagebox.askyesno("Confirmar", "¿Eliminar este cliente y sus datos?"):
        exito, mensaje = app.controller.eliminar_cliente_admin(id_cliente)
        if exito:
            messagebox.showinfo("Éxito", "Cliente eliminado")
            mostrar_contenido_admin(app, "clientes")
        else:
            messagebox.showerror("Error", mensaje)


def pagar_recibo_admin(app: Any, id_recibo: int):
    if messagebox.askyesno("Confirmar", "¿Marcar como pagado?"):
        exito, mensaje = app.controller.pagar_recibo_admin(id_recibo)
        if exito:
            messagebox.showinfo("Éxito", "Pago registrado")
            mostrar_contenido_admin(app, "recibos")
        else:
            messagebox.showerror("Error", mensaje)


def nueva_reserva_admin_dialog(app: Any):
    dialog = ctk.CTkToplevel(app)
    dialog.title("Nueva Reserva")
    dialog.geometry("500x650")
    dialog.configure(fg_color="#0a0e27")
    dialog.transient(app)
    dialog.grab_set()

    ctk.CTkLabel(
        dialog,
        text="📅 Crear Nueva Reserva",
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color="#00d4ff"
    ).pack(pady=20)

    def create_labeled_combo(parent, label, values):
        label_widget = ctk.CTkLabel(
            parent,
            text=label,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#b0b8c1"
        )
        label_widget.pack(anchor="w", pady=(0, 4))

        combo = ctk.CTkComboBox(
            parent,
            values=values,
            width=400,
            height=40,
            font=ctk.CTkFont(size=12),
            fg_color="#1a1f3a",
            border_color="#00d4ff",
            border_width=1.5,
            text_color="#ffffff"
        )
        combo.pack(pady=(0, 15), fill="x")
        return combo

    frame = ctk.CTkFrame(dialog, fg_color="transparent")
    frame.pack(pady=20, padx=30, fill="both", expand=True)

    clientes = app.controller.obtener_clientes()
    cliente_options = [f"{c['nombre']} {c['apellido']} (DNI: {c['dni']})" for c in clientes]
    cliente_combo = create_labeled_combo(frame, "👤 Cliente *", cliente_options)

    aparatos = app.controller.obtener_aparatos()
    aparato_options = [f"{a['nombre']} ({a['tipo']})" for a in aparatos]
    aparato_combo = create_labeled_combo(frame, "🏋️ Aparato *", aparato_options)

    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    dia_combo = create_labeled_combo(frame, "📅 Día *", dias)

    horas = app.controller.generar_horarios_disponibles()
    hora_combo = create_labeled_combo(frame, "⏰ Hora *", horas)

    def crear():
        if not all([cliente_combo.get(), aparato_combo.get(), dia_combo.get(), hora_combo.get()]):
            messagebox.showerror("Error", "Complete todos los campos")
            return

        try:
            cliente_idx = cliente_options.index(cliente_combo.get())
            id_cliente = clientes[cliente_idx]['id']

            aparato_idx = aparato_options.index(aparato_combo.get())
            id_aparato = aparatos[aparato_idx]['id']

            exito, mensaje = app.controller.crear_reserva_admin(
                id_cliente, id_aparato, dia_combo.get(), hora_combo.get()
            )

            if exito:
                messagebox.showinfo("¡Éxito!", "Reserva creada")
                dialog.destroy()
                mostrar_contenido_admin(app, "reservas")
            else:
                messagebox.showerror("Error", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear reserva: {str(e)}")

    ctk.CTkButton(
        frame,
        text="✅ Crear Reserva",
        command=crear,
        width=400,
        height=45,
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color="#00d4ff",
        text_color="#0a0e27",
        hover_color="#00b8d4",
        corner_radius=10
    ).pack()


    # Menú admin
    menu_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    menu_frame.pack(fill="both", expand=True, pady=20)

    crear_boton_admin(menu_frame, "Dashboard", lambda: mostrar_contenido_admin(app, "dashboard"), "📊")
    crear_boton_admin(menu_frame, "Clientes", lambda: mostrar_contenido_admin(app, "clientes"), "👥")
    crear_boton_admin(menu_frame, "Aparatos", lambda: mostrar_contenido_admin(app, "aparatos"), "🏋️")
    crear_boton_admin(menu_frame, "Reservas", lambda: mostrar_contenido_admin(app, "reservas"), "📅")
    crear_boton_admin(menu_frame, "Recibos", lambda: mostrar_contenido_admin(app, "recibos"), "📄")
    crear_boton_admin(menu_frame, "Morosos", lambda: mostrar_contenido_admin(app, "morosos"), "⚠️")
    crear_boton_admin(menu_frame, "Horarios", lambda: mostrar_contenido_admin(app, "horarios"), "🕐")

    # Botón cerrar sesión
    ctk.CTkButton(
        sidebar,
        text="🚪 Cerrar Sesión",
        command=app.cerrar_sesion,
        width=210,
        height=40,
        fg_color="red",
        hover_color="darkred"
    ).pack(side="bottom", pady=20, padx=20)

    # Contenido
    app.content_frame = ctk.CTkFrame(main_frame)
    app.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    mostrar_contenido_admin(app, "dashboard")


def mostrar_contenido_admin(app: Any, seccion: str):
    for widget in app.content_frame.winfo_children():
        widget.destroy()

    if seccion == "dashboard":
        contenido_dashboard_admin(app)
    elif seccion == "clientes":
        contenido_admin_clientes(app)
    elif seccion == "aparatos":
        contenido_admin_aparatos(app)
    elif seccion == "reservas":
        contenido_admin_reservas(app)
    elif seccion == "recibos":
        contenido_admin_recibos(app)
    elif seccion == "morosos":
        contenido_admin_morosos(app)
    elif seccion == "horarios":
        # reuse client horarios
        from .client import contenido_horarios
        contenido_horarios(app)


def contenido_dashboard_admin(app: Any):
    ctk.CTkLabel(
        app.content_frame,
        text="📊 Panel de Control",
        font=ctk.CTkFont(size=32, weight="bold")
    ).pack(pady=20)

    stats = app.controller.obtener_estadisticas_generales()

    # Grid de estadísticas
    stats_grid = ctk.CTkFrame(app.content_frame, fg_color="transparent")
    stats_grid.pack(fill="both", expand=True, padx=20, pady=20)

    # Fila 1
    row1 = ctk.CTkFrame(stats_grid, fg_color="transparent")
    row1.pack(fill="x", pady=10)

    crear_stat_card(row1, "👥", stats['total_clientes'], "Clientes").pack(side="left", fill="both", expand=True, padx=5)
    crear_stat_card(row1, "🏋️", stats['total_aparatos'], "Aparatos").pack(side="left", fill="both", expand=True, padx=5)
    crear_stat_card(row1, "📅", stats['total_reservas'], "Reservas").pack(side="left", fill="both", expand=True, padx=5)

    # Fila 2
    row2 = ctk.CTkFrame(stats_grid, fg_color="transparent")
    row2.pack(fill="x", pady=10)

    crear_stat_card(row2, "📄", stats['total_recibos'], "Recibos Totales").pack(side="left", fill="both", expand=True, padx=5)
    crear_stat_card(row2, "✅", stats['recibos_pagados'], "Recibos Pagados", "green").pack(side="left", fill="both", expand=True, padx=5)
    crear_stat_card(row2, "⚠️", stats['total_morosos'], "Clientes Morosos", "orange").pack(side="left", fill="both", expand=True, padx=5)

    # Fila 3 - Financiero
    row3 = ctk.CTkFrame(stats_grid, fg_color="transparent")
    row3.pack(fill="x", pady=10)

    crear_stat_card(row3, "💰", f"€{stats['total_ingresos']:.2f}", "Ingresos Totales", "green").pack(side="left", fill="both", expand=True, padx=5)
    crear_stat_card(row3, "📉", f"€{stats['deuda_total']:.2f}", "Deuda Pendiente", "red").pack(side="left", fill="both", expand=True, padx=5)

    # Botones de acción rápida
    action_frame = ctk.CTkFrame(app.content_frame)
    action_frame.pack(pady=30)

    ctk.CTkButton(
        action_frame,
        text="📄 Generar Recibos del Mes",
        command=lambda: generar_recibos_dialog(app),
        width=250,
        height=50,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color="green",
        hover_color="darkgreen"
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        action_frame,
        text="⚠️ Ver Clientes Morosos",
        command=lambda: mostrar_contenido_admin(app, "morosos"),
        width=250,
        height=50,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color="orange",
        hover_color="darkorange"
    ).pack(side="left", padx=10)


def generar_recibos_dialog(app: Any):
    dialog = ctk.CTkToplevel(app)
    dialog.title("Generar Recibos")
    dialog.geometry("400x300")
    dialog.transient(app)
    dialog.grab_set()

    ctk.CTkLabel(
        dialog,
        text="Generar Recibos Mensuales",
        font=ctk.CTkFont(size=20, weight="bold")
    ).pack(pady=20)

    # Mes
    ctk.CTkLabel(dialog, text="Mes:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
    mes_combo = ctk.CTkComboBox(
        dialog,
        values=[str(i) for i in range(1, 13)],
        width=200
    )
    mes_combo.set(str(datetime.now().month))
    mes_combo.pack()

    # Año
    ctk.CTkLabel(dialog, text="Año:", font=ctk.CTkFont(size=14)).pack(pady=(15, 5))
    anio_combo = ctk.CTkComboBox(
        dialog,
        values=[str(i) for i in range(2024, 2027)],
        width=200
    )
    anio_combo.set(str(datetime.now().year))
    anio_combo.pack()

    # Botón generar
    def generar():
        mes = int(mes_combo.get())
        anio = int(anio_combo.get())

        exito, mensaje = app.controller.generar_recibos_mes(mes, anio)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            dialog.destroy()
            mostrar_contenido_admin(app, "dashboard")
        else:
            messagebox.showerror("Error", mensaje)

    ctk.CTkButton(
        dialog,
        text="✅ Generar Recibos",
        command=generar,
        width=200,
        height=40,
        font=ctk.CTkFont(size=14, weight="bold")
    ).pack(pady=30)


def contenido_admin_clientes(app: Any):
    header = ctk.CTkFrame(app.content_frame, fg_color="transparent")
    header.pack(fill="x", pady=20, padx=20)

    ctk.CTkLabel(
        header,
        text="👥 Gestión de Clientes",
        font=ctk.CTkFont(size=28, weight="bold")
    ).pack(side="left")

    ctk.CTkButton(
        header,
        text="➕ Nuevo Cliente",
        command=lambda: nuevo_cliente_dialog(app),
        width=150,
        height=40
    ).pack(side="right")

    # Lista de clientes
    scroll_frame = ctk.CTkScrollableFrame(app.content_frame)
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

    clientes = app.controller.obtener_clientes()

    if not clientes:
        ctk.CTkLabel(
            scroll_frame,
            text="No hay clientes en el sistema",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        ).pack(pady=40)
        return

    for cliente in clientes:
        card = ctk.CTkFrame(scroll_frame)
        card.pack(fill="x", pady=5, padx=10)

        tipo_emoji = "👑" if cliente['tipo'] == 'admin' else "👤"
        info_text = f"{tipo_emoji} {cliente['nombre']} {cliente['apellido']}\n" \
                    f"DNI: {cliente['dni']} | Tel: {cliente['telefono']} | Email: {cliente['email']}"

        ctk.CTkLabel(
            card,
            text=info_text,
            font=ctk.CTkFont(size=13),
            justify="left"
        ).pack(side="left", pady=15, padx=20)

        # No permitir eliminar a usuarios admin (seguridad)
        if cliente['tipo'] != 'admin':
            ctk.CTkButton(
                card,
                text="❌",
                command=lambda c=cliente: eliminar_cliente(app, c['id']),
                width=60,
                fg_color="red",
                hover_color="darkred"
            ).pack(side="right", pady=10, padx=10)


def nuevo_cliente_dialog(app: Any):
    dialog = ctk.CTkToplevel(app)
    dialog.title("Nuevo Cliente")
    dialog.geometry("500x600")
    dialog.transient(app)
    dialog.grab_set()

    ctk.CTkLabel(
        dialog,
        text="Crear Nuevo Cliente",
        font=ctk.CTkFont(size=24, weight="bold")
    ).pack(pady=20)

    # Campos
    nombre = ctk.CTkEntry(dialog, placeholder_text="Nombre *", width=400, height=40)
    nombre.pack(pady=5)

    apellido = ctk.CTkEntry(dialog, placeholder_text="Apellido *", width=400, height=40)
    apellido.pack(pady=5)

    dni = ctk.CTkEntry(dialog, placeholder_text="DNI *", width=400, height=40)
    dni.pack(pady=5)

    telefono = ctk.CTkEntry(dialog, placeholder_text="Teléfono", width=400, height=40)
    telefono.pack(pady=5)

    email = ctk.CTkEntry(dialog, placeholder_text="Email", width=400, height=40)
    email.pack(pady=5)

    password = ctk.CTkEntry(dialog, placeholder_text="Contraseña *", show="*", width=400, height=40)
    password.pack(pady=5)

    tipo = ctk.CTkComboBox(dialog, values=['cliente', 'admin'], width=400, height=40)
    tipo.set('cliente')
    tipo.pack(pady=5)

    def crear():
        exito, mensaje = app.controller.crear_cliente_admin(
            nombre.get(), apellido.get(), dni.get(),
            telefono.get(), email.get(), password.get(), tipo.get()
        )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            dialog.destroy()
            mostrar_contenido_admin(app, "clientes")
        else:
            messagebox.showerror("Error", mensaje)

    ctk.CTkButton(
        dialog,
        text="✅ Crear Cliente",
        command=crear,
        width=400,
        height=45,
        font=ctk.CTkFont(size=14, weight="bold")
    ).pack(pady=20)


def contenido_admin_aparatos(app: Any):
    header = ctk.CTkFrame(app.content_frame, fg_color="transparent")
    header.pack(fill="x", pady=20, padx=20)

    ctk.CTkLabel(
        header,
        text="🏋️ Gestión de Aparatos",
        font=ctk.CTkFont(size=28, weight="bold")
    ).pack(side="left")

    ctk.CTkButton(
        header,
        text="➕ Nuevo Aparato",
        command=lambda: nuevo_aparato_dialog(app),
        width=150,
        height=40
    ).pack(side="right")

    # Lista de aparatos
    scroll_frame = ctk.CTkScrollableFrame(app.content_frame)
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

    aparatos = app.controller.obtener_aparatos()

    for aparato in aparatos:
        card = ctk.CTkFrame(scroll_frame)
        card.pack(fill="x", pady=5, padx=10)

        info_text = f"🏋️ {aparato['nombre']}\n" \
                    f"Tipo: {aparato['tipo']} | {aparato['descripcion']}"

        ctk.CTkLabel(
            card,
            text=info_text,
            font=ctk.CTkFont(size=13),
            justify="left"
        ).pack(side="left", pady=15, padx=20)

        ctk.CTkButton(
            card,
            text="❌",
            command=lambda a=aparato: eliminar_aparato(app, a['id']),
            width=60,
            fg_color="red",
            hover_color="darkred"
        ).pack(side="right", pady=10, padx=10)


def nuevo_aparato_dialog(app: Any):
    dialog = ctk.CTkToplevel(app)
    dialog.title("Nuevo Aparato")
    dialog.geometry("450x400")
    dialog.transient(app)
    dialog.grab_set()

    ctk.CTkLabel(
        dialog,
        text="Crear Nuevo Aparato",
        font=ctk.CTkFont(size=24, weight="bold")
    ).pack(pady=20)

    nombre = ctk.CTkEntry(dialog, placeholder_text="Nombre del aparato *", width=350, height=40)
    nombre.pack(pady=10)

    tipo = ctk.CTkEntry(dialog, placeholder_text="Tipo (ej: Cardio, Pesas) *", width=350, height=40)
    tipo.pack(pady=10)

    descripcion = ctk.CTkEntry(dialog, placeholder_text="Descripción", width=350, height=40)
    descripcion.pack(pady=10)

    def crear():
        exito, mensaje = app.controller.crear_aparato(
            nombre.get(), tipo.get(), descripcion.get()
        )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            dialog.destroy()
            mostrar_contenido_admin(app, "aparatos")
        else:
            messagebox.showerror("Error", mensaje)

    ctk.CTkButton(
        dialog,
        text="✅ Crear Aparato",
        command=crear,
        width=350,
        height=45,
        font=ctk.CTkFont(size=14, weight="bold")
    ).pack(pady=20)


def eliminar_aparato(app: Any, id_aparato: int):
    if messagebox.askyesno("Confirmar", "¿Desea eliminar este aparato?"):
        exito, mensaje = app.controller.eliminar_aparato(id_aparato)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            mostrar_contenido_admin(app, "aparatos")
        else:
            messagebox.showerror("Error", mensaje)


def contenido_admin_reservas(app: Any):
    header = ctk.CTkFrame(app.content_frame, fg_color="transparent")
    header.pack(fill="x", pady=20, padx=20)

    ctk.CTkLabel(
        header,
        text="📅 Gestión de Reservas",
        font=ctk.CTkFont(size=28, weight="bold")
    ).pack(side="left")

    ctk.CTkButton(
        header,
        text="➕ Nueva Reserva",
        command=lambda: nueva_reserva_admin_dialog(app),
        width=150,
        height=40
    ).pack(side="right")

    scroll_frame = ctk.CTkScrollableFrame(app.content_frame)
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Sección de Reservas Pendientes
    ctk.CTkLabel(
        scroll_frame,
        text="⏳ RESERVAS PENDIENTES DE APROBACIÓN",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color="orange"
    ).pack(pady=(20, 10), padx=10)

    reservas_pendientes = app.controller.obtener_reservas_pendientes()
    
    if reservas_pendientes:
        for reserva in reservas_pendientes:
            card = ctk.CTkFrame(scroll_frame, fg_color="#3a3a3a")
            card.pack(fill="x", pady=5, padx=10)

            info_text = f"👤 {reserva['cliente']} | 🏋️ {reserva['aparato']}\n" \
                        f"📅 {reserva['dia']} | ⏰ {reserva['hora_inicio']} - {reserva['hora_fin']}"

            ctk.CTkLabel(
                card,
                text=info_text,
                font=ctk.CTkFont(size=13),
                justify="left"
            ).pack(side="left", pady=15, padx=20)

            # Botones de aceptar y rechazar
            buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
            buttons_frame.pack(side="right", pady=10, padx=10)

            ctk.CTkButton(
                buttons_frame,
                text="✅ Aceptar",
                command=lambda r=reserva: admin_aceptar_reserva(app, r['id']),
                width=90,
                fg_color="green",
                hover_color="darkgreen"
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                buttons_frame,
                text="❌ Rechazar",
                command=lambda r=reserva: admin_rechazar_reserva(app, r['id']),
                width=90,
                fg_color="red",
                hover_color="darkred"
            ).pack(side="left", padx=5)
    else:
        ctk.CTkLabel(
            scroll_frame,
            text="No hay reservas pendientes",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=20, padx=10)

    # Sección de Reservas Aceptadas
    ctk.CTkLabel(
        scroll_frame,
        text="✅ RESERVAS ACEPTADAS",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color="green"
    ).pack(pady=(30, 10), padx=10)

    reservas = app.controller.obtener_todas_reservas()
    reservas_aceptadas = [r for r in reservas if r.get('estado') == 'aceptada']

    if reservas_aceptadas:
        for reserva in reservas_aceptadas:
            card = ctk.CTkFrame(scroll_frame)
            card.pack(fill="x", pady=5, padx=10)

            info_text = f"👤 {reserva['cliente']} | 🏋️ {reserva['aparato']}\n" \
                        f"📅 {reserva['dia']} | ⏰ {reserva['hora_inicio']} - {reserva['hora_fin']}"

            ctk.CTkLabel(
                card,
                text=info_text,
                font=ctk.CTkFont(size=13),
                justify="left"
            ).pack(side="left", pady=15, padx=20)

            ctk.CTkButton(
                card,
                text="🗑️ Eliminar",
                command=lambda r=reserva: admin_eliminar_reserva(app, r['id']),
                width=100,
                fg_color="red",
                hover_color="darkred"
            ).pack(side="right", pady=10, padx=10)
    else:
        ctk.CTkLabel(
            scroll_frame,
            text="No hay reservas aceptadas",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=20, padx=10)


def admin_aceptar_reserva(app: Any, id_reserva: int):
    exito, mensaje = app.controller.aceptar_reserva(id_reserva)
    if exito:
        messagebox.showinfo("Éxito", "Reserva aceptada. El cliente será notificado.")
        mostrar_contenido_admin(app, "reservas")
    else:
        messagebox.showerror("Error", mensaje)


def admin_rechazar_reserva(app: Any, id_reserva: int):
    if messagebox.askyesno("Confirmar", "¿Desea rechazar esta reserva?"):
        exito, mensaje = app.controller.rechazar_reserva(id_reserva)
        if exito:
            messagebox.showinfo("Éxito", "Reserva rechazada. El cliente será notificado.")
            mostrar_contenido_admin(app, "reservas")
        else:
            messagebox.showerror("Error", mensaje)


def admin_eliminar_reserva(app: Any, id_reserva: int):
    if messagebox.askyesno("Confirmar", "¿Desea eliminar esta reserva?"):
        exito, mensaje = app.controller.eliminar_reserva(id_reserva)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            mostrar_contenido_admin(app, "reservas")
        else:
            messagebox.showerror("Error", mensaje)


def contenido_admin_morosos(app: Any):
    ctk.CTkLabel(
        app.content_frame,
        text="⚠️ Clientes Morosos",
        font=ctk.CTkFont(size=28, weight="bold")
    ).pack(pady=20)

    scroll_frame = ctk.CTkScrollableFrame(app.content_frame)
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

    morosos = app.controller.obtener_morosos()

    if not morosos:
        ctk.CTkLabel(
            scroll_frame,
            text="✅ No hay clientes morosos",
            font=ctk.CTkFont(size=18),
            text_color="green"
        ).pack(pady=40)
        return

    for moroso in morosos:
        card = ctk.CTkFrame(scroll_frame, border_width=2, border_color="orange")
        card.pack(fill="x", pady=5, padx=10)

        info_text = f"⚠️ {moroso['nombre']} {moroso['apellido']}\n" \
                    f"DNI: {moroso['dni']} | Tel: {moroso['telefono']}\n" \
                    f"Recibos pendientes: {moroso['recibos_pendientes']} | Deuda: €{moroso['deuda_total']:.2f}"

        ctk.CTkLabel(
            card,
            text=info_text,
            font=ctk.CTkFont(size=13),
            justify="left"
        ).pack(pady=15, padx=20)


def eliminar_cliente(app: Any, id_cliente: int):
    """Elimina un cliente del sistema."""
    if messagebox.askyesno("Confirmar", "¿Desea eliminar este cliente y todas sus reservas/recibos?"):
        exito, mensaje = app.controller.eliminar_cliente_admin(id_cliente)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            mostrar_contenido_admin(app, "clientes")
        else:
            messagebox.showerror("Error", mensaje)


def pagar_recibo_admin(app: Any, id_recibo: int):
    """Admin marca un recibo como pagado."""
    if messagebox.askyesno("Confirmar", "¿Marcar este recibo como pagado?"):
        exito, mensaje = app.controller.pagar_recibo_admin(id_recibo)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            mostrar_contenido_admin(app, "recibos")
        else:
            messagebox.showerror("Error", mensaje)


def nueva_reserva_admin_dialog(app: Any):
    """Diálogo para crear una reserva para un cliente."""
    dialog = ctk.CTkToplevel(app)
    dialog.title("Nueva Reserva")
    dialog.geometry("500x600")
    dialog.transient(app)
    dialog.grab_set()

    ctk.CTkLabel(
        dialog,
        text="Crear Nueva Reserva",
        font=ctk.CTkFont(size=24, weight="bold")
    ).pack(pady=20)

    # Cliente
    ctk.CTkLabel(dialog, text="Cliente *", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
    clientes = app.controller.obtener_clientes()
    cliente_options = [f"{c['nombre']} {c['apellido']} (DNI: {c['dni']})" for c in clientes]
    cliente_combo = ctk.CTkComboBox(dialog, values=cliente_options, width=400, height=40)
    cliente_combo.pack(pady=5)

    # Aparato
    ctk.CTkLabel(dialog, text="Aparato *", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
    aparatos = app.controller.obtener_aparatos()
    aparato_options = [f"{a['nombre']} ({a['tipo']})" for a in aparatos]
    aparato_combo = ctk.CTkComboBox(dialog, values=aparato_options, width=400, height=40)
    aparato_combo.pack(pady=5)

    # Día
    ctk.CTkLabel(dialog, text="Día de la Semana *", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    dia_combo = ctk.CTkComboBox(dialog, values=dias, width=400, height=40)
    dia_combo.pack(pady=5)

    # Hora
    ctk.CTkLabel(dialog, text="Hora de Inicio *", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
    horas = app.controller.generar_horarios_disponibles()
    hora_combo = ctk.CTkComboBox(dialog, values=horas, width=400, height=40)
    hora_combo.pack(pady=5)

    def crear():
        if not cliente_combo.get() or not aparato_combo.get() or not dia_combo.get() or not hora_combo.get():
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            # Extraer índice de cliente
            cliente_idx = cliente_options.index(cliente_combo.get())
            id_cliente = clientes[cliente_idx]['id']

            # Extraer índice de aparato
            aparato_idx = aparato_options.index(aparato_combo.get())
            id_aparato = aparatos[aparato_idx]['id']

            exito, mensaje = app.controller.crear_reserva_admin(
                id_cliente, id_aparato, dia_combo.get(), hora_combo.get()
            )

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                dialog.destroy()
                mostrar_contenido_admin(app, "reservas")
            else:
                messagebox.showerror("Error", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear reserva: {str(e)}")

    ctk.CTkButton(
        dialog,
        text="✅ Crear Reserva",
        command=crear,
        width=400,
        height=45,
        font=ctk.CTkFont(size=14, weight="bold")
    ).pack(pady=20)
