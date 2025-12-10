import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from typing import Any
from views.components import crear_boton_admin, crear_stat_card


def mostrar_dashboard_admin(app: Any):
    app.limpiar_ventana()

    # Frame principal
    main_frame = ctk.CTkFrame(app, fg_color="transparent")
    main_frame.pack(fill="both", expand=True)

    # Sidebar
    sidebar = ctk.CTkFrame(main_frame, width=250, corner_radius=0, fg_color="#1a1a1a")
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Admin info
    user_frame = ctk.CTkFrame(sidebar, fg_color="#2b2b2b")
    user_frame.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(
        user_frame,
        text="👑 ADMINISTRADOR",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color="gold"
    ).pack(pady=10)

    usuario = app.controller.usuario_actual
    ctk.CTkLabel(
        user_frame,
        text=f"{usuario['nombre']} {usuario['apellido']}",
        font=ctk.CTkFont(size=12)
    ).pack(pady=(0, 10))

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


def contenido_admin_recibos(app: Any):
    ctk.CTkLabel(
        app.content_frame,
        text="📄 Todos los Recibos",
        font=ctk.CTkFont(size=28, weight="bold")
    ).pack(pady=20)

    scroll_frame = ctk.CTkScrollableFrame(app.content_frame)
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

    recibos = app.controller.obtener_todos_recibos()

    if not recibos:
        ctk.CTkLabel(
            scroll_frame,
            text="No hay recibos en el sistema",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        ).pack(pady=40)
        return

    for recibo in recibos:
        card = ctk.CTkFrame(scroll_frame)
        card.pack(fill="x", pady=5, padx=10)

        mes_nombre = app.controller.obtener_nombre_mes(recibo['mes'])
        estado_color = "green" if recibo['estado'] == 'pagado' else "orange"

        info_text = f"👤 {recibo['cliente']} | 📄 {mes_nombre} {recibo['anio']}\n" \
                    f"💰 €{recibo['monto']:.2f} | Estado: {recibo['estado'].upper()}"

        ctk.CTkLabel(
            card,
            text=info_text,
            font=ctk.CTkFont(size=13),
            justify="left"
        ).pack(side="left", pady=15, padx=20)

        # Botón para pagar si está pendiente
        if recibo['estado'] == 'pendiente':
            ctk.CTkButton(
                card,
                text="✅ Pagar",
                command=lambda r=recibo: pagar_recibo_admin(app, r['id']),
                width=80,
                fg_color="green",
                hover_color="darkgreen"
            ).pack(side="right", pady=10, padx=10)
        else:
            ctk.CTkLabel(
                card,
                text="●",
                font=ctk.CTkFont(size=30),
                text_color=estado_color
            ).pack(side="right", padx=20)


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
