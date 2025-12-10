import customtkinter as ctk
from tkinter import messagebox
from typing import Any


def mostrar_dashboard_cliente(app: Any):
    """Muestra el dashboard del cliente"""
    print("[DEBUG] mostrar_dashboard_cliente() ejecutado")
    app.limpiar_ventana()

    # Frame principal
    main_frame = ctk.CTkFrame(app, fg_color="transparent")
    main_frame.pack(fill="both", expand=True)

    # Sidebar
    sidebar = ctk.CTkFrame(main_frame, width=250, corner_radius=0)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Usuario info
    usuario = app.controller.usuario_actual
    user_frame = ctk.CTkFrame(sidebar)
    user_frame.pack(pady=20, padx=20, fill="x")

    ctk.CTkLabel(
        user_frame,
        text=f"👤 {usuario['nombre']} {usuario['apellido']}",
        font=ctk.CTkFont(size=14, weight="bold")
    ).pack(pady=10)

    ctk.CTkLabel(
        user_frame,
        text=f"DNI: {usuario['dni']}",
        font=ctk.CTkFont(size=12),
        text_color="gray"
    ).pack()

    # Menú
    menu_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    menu_frame.pack(fill="both", expand=True, pady=20)

    from .components import crear_boton_menu

    # Botón destacado visible para Notificaciones (temporal)
    btn_notif_visible = ctk.CTkButton(
        sidebar,
        text="🔔 NOTIFICACIONES",
        command=lambda: mostrar_contenido_cliente(app, "notificaciones"),
        width=210,
        height=45,
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color="#2dbe60",
        hover_color="#28a754"
    )
    btn_notif_visible.pack(pady=(10, 6), padx=20)

    crear_boton_menu(menu_frame, "Hacer Reserva", lambda: mostrar_contenido_cliente(app, "reservar"), "📅")
    crear_boton_menu(menu_frame, "Mis Reservas", lambda: mostrar_contenido_cliente(app, "mis_reservas"), "📋")
    print("[DEBUG] Agregando boton: Notificaciones")
    crear_boton_menu(menu_frame, "Notificaciones", lambda: mostrar_contenido_cliente(app, "notificaciones"), "🔔")
    print("[DEBUG] Boton Notificaciones creado en el código")
    crear_boton_menu(menu_frame, "Mis Pagos", lambda: mostrar_contenido_cliente(app, "pagos"), "💳")
    crear_boton_menu(menu_frame, "Ver Horarios", lambda: mostrar_contenido_cliente(app, "horarios"), "🕐")

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

    # Mostrar inicio
    mostrar_contenido_cliente(app, "inicio")


def mostrar_contenido_cliente(app: Any, seccion: str):
    """Muestra el contenido según la sección seleccionada"""
    for widget in app.content_frame.winfo_children():
        widget.destroy()

    if seccion == "inicio":
        contenido_inicio_cliente(app)
    elif seccion == "reservar":
        contenido_reservar(app)
    elif seccion == "mis_reservas":
        contenido_mis_reservas(app)
    elif seccion == "notificaciones":
        contenido_notificaciones(app)
    elif seccion == "pagos":
        contenido_pagos(app)
    elif seccion == "horarios":
        contenido_horarios(app)


def contenido_inicio_cliente(app: Any):
    ctk.CTkLabel(
        app.content_frame,
        text="🏋️ Bienvenido a GymForTheMoment",
        font=ctk.CTkFont(size=32, weight="bold")
    ).pack(pady=(20, 10))

    ctk.CTkLabel(
        app.content_frame,
        text="Gimnasio 24/7 - Lunes a Viernes",
        font=ctk.CTkFont(size=18)
    ).pack(pady=(0, 40))

    # Tarjetas de información
    info_frame = ctk.CTkFrame(app.content_frame, fg_color="transparent")
    info_frame.pack(fill="both", expand=True, padx=20)

    # Obtener datos
    mis_reservas = app.controller.obtener_mis_reservas()
    mis_recibos = app.controller.obtener_mis_recibos_pendientes()

    # Tarjeta reservas
    card1 = ctk.CTkFrame(info_frame)
    card1.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(card1, text="📅", font=ctk.CTkFont(size=48)).pack(pady=(20, 10))
    ctk.CTkLabel(
        card1,
        text=f"{len(mis_reservas)}",
        font=ctk.CTkFont(size=42, weight="bold")
    ).pack()
    ctk.CTkLabel(
        card1,
        text="Reservas Activas",
        font=ctk.CTkFont(size=16)
    ).pack(pady=(0, 20))

    # Tarjeta pagos
    card2 = ctk.CTkFrame(info_frame)
    card2.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(card2, text="💳", font=ctk.CTkFont(size=48)).pack(pady=(20, 10))
    ctk.CTkLabel(
        card2,
        text=f"{len(mis_recibos)}",
        font=ctk.CTkFont(size=42, weight="bold"),
        text_color="orange" if len(mis_recibos) > 0 else "green"
    ).pack()
    ctk.CTkLabel(
        card2,
        text="Pagos Pendientes",
        font=ctk.CTkFont(size=16)
    ).pack(pady=(0, 20))

    # Botones de acción rápida
    action_frame = ctk.CTkFrame(app.content_frame)
    action_frame.pack(pady=30, padx=20)

    ctk.CTkButton(
        action_frame,
        text="📅 Nueva Reserva",
        command=lambda: mostrar_contenido_cliente(app, "reservar"),
        width=200,
        height=50,
        font=ctk.CTkFont(size=16, weight="bold")
    ).pack(side="left", padx=10)

    if len(mis_recibos) > 0:
        ctk.CTkButton(
            action_frame,
            text="💰 Pagar Ahora",
            command=lambda: mostrar_contenido_cliente(app, "pagos"),
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="orange",
            hover_color="darkorange"
        ).pack(side="left", padx=10)


def contenido_reservar(app: Any):
    ctk.CTkLabel(
        app.content_frame,
        text="📅 Nueva Reserva",
        font=ctk.CTkFont(size=28, weight="bold")
    ).pack(pady=20)

    # Frame de formulario
    form_frame = ctk.CTkFrame(app.content_frame)
    form_frame.pack(pady=20, padx=100, fill="both", expand=True)

    # Aparato
    ctk.CTkLabel(form_frame, text="Seleccione el aparato:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
    aparatos = app.controller.obtener_aparatos()
    aparato_names = [f"{a['nombre']} - {a['tipo']}" for a in aparatos]
    aparato_combo = ctk.CTkComboBox(form_frame, values=aparato_names, width=400, height=40)
    aparato_combo.pack(pady=5)

    # Día
    ctk.CTkLabel(form_frame, text="Día de la semana:", font=ctk.CTkFont(size=14)).pack(pady=(15, 5))
    dia_combo = ctk.CTkComboBox(
        form_frame,
        values=['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'],
        width=400,
        height=40
    )
    dia_combo.pack(pady=5)

    # Hora
    ctk.CTkLabel(form_frame, text="Hora de inicio:", font=ctk.CTkFont(size=14)).pack(pady=(15, 5))
    horarios = app.controller.generar_horarios_disponibles()
    hora_combo = ctk.CTkComboBox(form_frame, values=horarios, width=400, height=40)
    hora_combo.pack(pady=5)

    # Botón reservar
    def hacer_reserva():
        if not aparato_combo.get() or not dia_combo.get() or not hora_combo.get():
            messagebox.showerror("Error", "Complete todos los campos")
            return

        # Validar que el aparato seleccionado existe en la lista
        if aparato_combo.get() not in aparato_names:
            messagebox.showerror("Error", "Seleccione un aparato válido")
            return

        idx = aparato_names.index(aparato_combo.get())
        id_aparato = aparatos[idx]['id']

        exito, mensaje = app.controller.crear_reserva(
            id_aparato,
            dia_combo.get(),
            hora_combo.get()
        )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            mostrar_contenido_cliente(app, "mis_reservas")
        else:
            messagebox.showerror("Error", mensaje)

    ctk.CTkButton(
        form_frame,
        text="✅ Solicitar Reserva",
        command=hacer_reserva,
        width=400,
        height=50,
        font=ctk.CTkFont(size=16, weight="bold")
    ).pack(pady=30)


def contenido_mis_reservas(app: Any):
    ctk.CTkLabel(
        app.content_frame,
        text="📋 Mis Reservas",
        font=ctk.CTkFont(size=28, weight="bold")
    ).pack(pady=20)

    reservas = app.controller.obtener_mis_reservas()

    if not reservas:
        ctk.CTkLabel(
            app.content_frame,
            text="No tienes reservas activas",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        ).pack(pady=40)
        return

    # Scrollable frame
    scroll_frame = ctk.CTkScrollableFrame(app.content_frame)
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

    for reserva in reservas:
        card = ctk.CTkFrame(scroll_frame)
        card.pack(fill="x", pady=5, padx=10)

        # Determinar color del estado
        estado = reserva.get('estado', 'pendiente')
        if estado == 'pendiente':
            estado_color = "orange"
            estado_icon = "⏳"
            estado_texto = "PENDIENTE"
        elif estado == 'aceptada':
            estado_color = "green"
            estado_icon = "✅"
            estado_texto = "ACEPTADA"
        else:  # rechazada
            estado_color = "red"
            estado_icon = "❌"
            estado_texto = "RECHAZADA"

        info_text = f"🏋️ {reserva['aparato']} ({reserva['tipo']})\n" \
                   f"📅 {reserva['dia']} | ⏰ {reserva['hora_inicio']} - {reserva['hora_fin']}"

        ctk.CTkLabel(
            card,
            text=info_text,
            font=ctk.CTkFont(size=14),
            justify="left"
        ).pack(side="left", pady=15, padx=20)

        # Estado
        ctk.CTkLabel(
            card,
            text=f"{estado_icon} {estado_texto}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=estado_color
        ).pack(side="right", pady=15, padx=20)

        # Botón cancelar solo si está pendiente
        if estado == 'pendiente':
            ctk.CTkButton(
                card,
                text="❌ Cancelar",
                command=lambda r=reserva: cancelar_reserva(app, r['id']),
                width=100,
                fg_color="red",
                hover_color="darkred"
            ).pack(side="right", pady=10, padx=5)


def contenido_notificaciones(app: Any):
    ctk.CTkLabel(
        app.content_frame,
        text="🔔 Notificaciones",
        font=ctk.CTkFont(size=28, weight="bold")
    ).pack(pady=20)

    notificaciones = app.controller.obtener_mis_notificaciones()

    if not notificaciones:
        ctk.CTkLabel(
            app.content_frame,
            text="No tienes notificaciones",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        ).pack(pady=40)
        return

    # Scrollable frame
    scroll_frame = ctk.CTkScrollableFrame(app.content_frame)
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

    for notif in notificaciones:
        card = ctk.CTkFrame(scroll_frame)
        card.pack(fill="x", pady=5, padx=10)

        # Determinar color según tipo
        if notif['tipo'] == 'aceptada':
            tipo_icon = "✅"
            tipo_color = "green"
            tipo_texto = "ACEPTADA"
        else:  # rechazada
            tipo_icon = "❌"
            tipo_color = "red"
            tipo_texto = "RECHAZADA"

        # Mensaje
        ctk.CTkLabel(
            card,
            text=f"{tipo_icon} {notif['mensaje']}",
            font=ctk.CTkFont(size=13),
            text_color=tipo_color,
            justify="left"
        ).pack(side="left", pady=15, padx=20, fill="both", expand=True)

        # Botón aceptar solo si está sin leer
        if not notif.get('leida', False):
            ctk.CTkButton(
                card,
                text="✓ Aceptar",
                command=lambda n=notif: aceptar_notificacion(app, n['id']),
                width=100,
                fg_color="green",
                hover_color="darkgreen"
            ).pack(side="right", pady=10, padx=20)

        # Si la notificación es de tipo 'rechazada', permitir retirar la reserva directamente
        if notif.get('tipo') == 'rechazada' and notif.get('id_reserva'):
            ctk.CTkButton(
                card,
                text="🗑️ Retirar Reserva",
                command=lambda n=notif: retirar_reserva_desde_notificacion(app, n.get('id_reserva'), n.get('id')),
                width=140,
                fg_color="red",
                hover_color="darkred"
            ).pack(side="right", pady=10, padx=5)

        # Botón para eliminar la notificación permanentemente
        ctk.CTkButton(
            card,
            text="Eliminar",
            command=lambda n=notif: eliminar_notificacion_ui(app, n.get('id')),
            width=100,
            fg_color="#b22222",
            hover_color="#a11a1a"
        ).pack(side="right", pady=10, padx=5)


def aceptar_notificacion(app: Any, id_notificacion: int):
    exito, mensaje = app.controller.marcar_notificacion_leida(id_notificacion)
    if exito:
        messagebox.showinfo("Éxito", "Notificación marcada como leída")
        mostrar_contenido_cliente(app, "notificaciones")
    else:
        messagebox.showerror("Error", mensaje)


def cancelar_reserva(app: Any, id_reserva: int):
    if messagebox.askyesno("Confirmar", "¿Desea cancelar esta reserva?"):
        exito, mensaje = app.controller.eliminar_reserva(id_reserva)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            mostrar_contenido_cliente(app, "mis_reservas")
        else:
            messagebox.showerror("Error", mensaje)


def eliminar_notificacion_ui(app: Any, id_notificacion: int):
    """Eliminar notificación desde la vista del cliente"""
    if not id_notificacion:
        messagebox.showerror("Error", "ID de notificación inválido")
        return

    if messagebox.askyesno("Confirmar", "¿Desea eliminar esta notificación?"):
        exito, mensaje = app.controller.eliminar_notificacion(id_notificacion)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            mostrar_contenido_cliente(app, "notificaciones")
        else:
            messagebox.showerror("Error", mensaje)


def retirar_reserva_desde_notificacion(app: Any, id_reserva: int, id_notificacion: int):
    """El cliente retira su reserva desde la notificación (usado cuando fue rechazada)."""
    if not id_reserva:
        messagebox.showerror("Error", "ID de reserva inválido")
        return

    if messagebox.askyesno("Confirmar", "¿Desea retirar (eliminar) esta reserva?"):
        exito, mensaje = app.controller.eliminar_reserva(id_reserva)
        if exito:
            # Marcar notificación como leída si existe
            if id_notificacion:
                app.controller.marcar_notificacion_leida(id_notificacion)
            messagebox.showinfo("Éxito", "Reserva retirada")
            mostrar_contenido_cliente(app, "notificaciones")
        else:
            messagebox.showerror("Error", mensaje)


def contenido_pagos(app: Any):
    ctk.CTkLabel(
        app.content_frame,
        text="💳 Gestión de Pagos",
        font=ctk.CTkFont(size=28, weight="bold")
    ).pack(pady=20)

    recibos = app.controller.obtener_mis_recibos()

    if not recibos:
        ctk.CTkLabel(
            app.content_frame,
            text="No hay recibos disponibles",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        ).pack(pady=40)
        return

    # Scrollable frame
    scroll_frame = ctk.CTkScrollableFrame(app.content_frame)
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

    for recibo in recibos:
        card = ctk.CTkFrame(scroll_frame)
        card.pack(fill="x", pady=5, padx=10)

        mes_nombre = app.controller.obtener_nombre_mes(recibo['mes'])
        info_text = f"📄 Recibo {mes_nombre} {recibo['anio']}\n" \
                   f"💰 Monto: €{recibo['monto']:.2f} | Estado: {recibo['estado'].upper()}"

        ctk.CTkLabel(
            card,
            text=info_text,
            font=ctk.CTkFont(size=14),
            justify="left"
        ).pack(side="left", pady=15, padx=20)

        if recibo['estado'] == 'pendiente':
            ctk.CTkButton(
                card,
                text="💰 Pagar",
                command=lambda r=recibo: pagar_recibo(app, r['id']),
                width=100,
                fg_color="green",
                hover_color="darkgreen"
            ).pack(side="right", pady=10, padx=20)
        else:
            ctk.CTkLabel(
                card,
                text="✅ PAGADO",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="green"
            ).pack(side="right", pady=15, padx=20)


def pagar_recibo(app: Any, id_recibo: int):
    if messagebox.askyesno("Confirmar Pago", "¿Desea confirmar el pago de este recibo?"):
        exito, mensaje = app.controller.pagar_recibo(id_recibo)
        if exito:
            messagebox.showinfo("Éxito", "Pago procesado correctamente")
            mostrar_contenido_cliente(app, "pagos")
        else:
            messagebox.showerror("Error", mensaje)


def contenido_horarios(app: Any):
    ctk.CTkLabel(
        app.content_frame,
        text="🕐 Horarios Ocupados",
        font=ctk.CTkFont(size=28, weight="bold")
    ).pack(pady=20)

    # Selector de día
    dia_frame = ctk.CTkFrame(app.content_frame)
    dia_frame.pack(pady=10)

    ctk.CTkLabel(dia_frame, text="Seleccione el día:", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)

    dia_var = ctk.StringVar(value="Lunes")
    dia_combo = ctk.CTkComboBox(
        dia_frame,
        values=['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'],
        variable=dia_var,
        width=200
    )
    dia_combo.pack(side="left", padx=10)

    # Frame para mostrar ocupación
    ocupacion_frame = ctk.CTkScrollableFrame(app.content_frame)
    ocupacion_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def mostrar_ocupacion():
        for widget in ocupacion_frame.winfo_children():
            widget.destroy()

        ocupacion = app.controller.obtener_ocupacion_dia(dia_var.get())

        if not ocupacion:
            ctk.CTkLabel(
                ocupacion_frame,
                text="No hay reservas para este día",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            ).pack(pady=40)
            return

        for ocu in ocupacion:
            card = ctk.CTkFrame(ocupacion_frame)
            card.pack(fill="x", pady=5, padx=10)

            info_text = f"🏋️ {ocu['aparato']} ({ocu['tipo']})\n" \
                       f"⏰ {ocu['hora_inicio']} - {ocu['hora_fin']} | 👤 {ocu['cliente']}"

            ctk.CTkLabel(
                card,
                text=info_text,
                font=ctk.CTkFont(size=14),
                justify="left"
            ).pack(pady=15, padx=20)

    ctk.CTkButton(
        dia_frame,
        text="🔍 Ver Ocupación",
        command=mostrar_ocupacion,
        width=150
    ).pack(side="left", padx=10)

    mostrar_ocupacion()
