import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from typing import Optional

from core import Controlador as GymController

# Configuración de tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Import views separated
from .login import mostrar_login as mostrar_login_view, mostrar_registro as mostrar_registro_view
from .components import crear_boton_menu, crear_boton_admin, crear_stat_card
from . import admin as admin_module
# Importar la vista de notificaciones del cliente (reutilizar implementación)
from .client import contenido_notificaciones


class GymApp(ctk.CTk):
    """Aplicación principal del gimnasio"""

    def __init__(self):
        super().__init__()

        self.controller = GymController()
        self.current_frame: Optional[ctk.CTkFrame] = None

        # Configuración de la ventana
        self.title("GymForTheMoment - Sistema de Gestión")
        self.geometry("1200x700")
        self.resizable(True, True)

        # Centrar ventana
        self.center_window()

        # Mostrar pantalla de login (desde módulo separado)
        mostrar_login_view(self)

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def limpiar_ventana(self):
        """Limpia todos los widgets de la ventana"""
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        """Muestra la pantalla de inicio de sesión (usa la versión mejorada de login.py)"""
        mostrar_login_view(self)

    def mostrar_registro(self):
        """Muestra la pantalla de registro (usa la versión mejorada de login.py)"""
        mostrar_registro_view(self)

    def mostrar_dashboard_cliente(self):
        """Muestra el dashboard del cliente"""
        print("[DEBUG-GYMAPP] mostrar_dashboard_cliente() ejecutado")
        self.limpiar_ventana()

        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)

        # Sidebar
        sidebar = ctk.CTkFrame(main_frame, width=250, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Usuario info
        usuario = self.controller.usuario_actual
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

        # Botón destacado para Notificaciones (temporal, color llamativo para debug/visibilidad)
        btn_notif_visible = ctk.CTkButton(
            sidebar,
            text="🔔 NOTIFICACIONES",
            command=lambda: self.mostrar_contenido_cliente("notificaciones"),
            width=210,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2dbe60",
            hover_color="#28a754"
        )
        btn_notif_visible.pack(pady=(10, 6), padx=20)

        def crear_boton_menu(texto, comando, icono=""):
            btn = ctk.CTkButton(
                menu_frame,
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

        print('[DEBUG-GYMAPP] Agregando boton: Hacer Reserva')
        crear_boton_menu("Hacer Reserva", lambda: self.mostrar_contenido_cliente("reservar"), "📅")
        print('[DEBUG-GYMAPP] Agregando boton: Mis Reservas')
        crear_boton_menu("Mis Reservas", lambda: self.mostrar_contenido_cliente("mis_reservas"), "📋")
        print('[DEBUG-GYMAPP] Agregando boton: Notificaciones')
        crear_boton_menu("Notificaciones", lambda: self.mostrar_contenido_cliente("notificaciones"), "🔔")
        print('[DEBUG-GYMAPP] Agregando boton: Mis Pagos')
        crear_boton_menu("Mis Pagos", lambda: self.mostrar_contenido_cliente("pagos"), "💳")
        print('[DEBUG-GYMAPP] Agregando boton: Ver Horarios')
        crear_boton_menu("Ver Horarios", lambda: self.mostrar_contenido_cliente("horarios"), "🕐")

        # Botón cerrar sesión
        ctk.CTkButton(
            sidebar,
            text="🚪 Cerrar Sesión",
            command=self.cerrar_sesion,
            width=210,
            height=40,
            fg_color="red",
            hover_color="darkred"
        ).pack(side="bottom", pady=20, padx=20)

        # Contenido
        self.content_frame = ctk.CTkFrame(main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Mostrar inicio
        self.mostrar_contenido_cliente("inicio")

    def mostrar_contenido_cliente(self, seccion: str):
        """Muestra el contenido según la sección seleccionada"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if seccion == "inicio":
            self.contenido_inicio_cliente()
        elif seccion == "reservar":
            self.contenido_reservar()
        elif seccion == "mis_reservas":
            self.contenido_mis_reservas()
        elif seccion == "notificaciones":
            # Delegar a la implementación de notificaciones en views.client
            contenido_notificaciones(self)
        elif seccion == "pagos":
            self.contenido_pagos()
        elif seccion == "horarios":
            self.contenido_horarios()

    def contenido_inicio_cliente(self):
        """Contenido de inicio para cliente"""
        ctk.CTkLabel(
            self.content_frame,
            text="🏋️ Bienvenido a GymForTheMoment",
            font=ctk.CTkFont(size=32, weight="bold")
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            self.content_frame,
            text="Gimnasio 24/7 - Lunes a Viernes",
            font=ctk.CTkFont(size=18)
        ).pack(pady=(0, 40))

        # Tarjetas de información
        info_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=20)

        # Obtener datos
        mis_reservas = self.controller.obtener_mis_reservas()
        mis_recibos = self.controller.obtener_mis_recibos_pendientes()

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
        action_frame = ctk.CTkFrame(self.content_frame)
        action_frame.pack(pady=30, padx=20)

        ctk.CTkButton(
            action_frame,
            text="📅 Nueva Reserva",
            command=lambda: self.mostrar_contenido_cliente("reservar"),
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left", padx=10)

        if len(mis_recibos) > 0:
            ctk.CTkButton(
                action_frame,
                text="💰 Pagar Ahora",
                command=lambda: self.mostrar_contenido_cliente("pagos"),
                width=200,
                height=50,
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color="orange",
                hover_color="darkorange"
            ).pack(side="left", padx=10)

    def contenido_reservar(self):
        """Contenido para hacer reservas"""
        ctk.CTkLabel(
            self.content_frame,
            text="📅 Nueva Reserva",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=20)

        # Frame de formulario
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(pady=20, padx=100, fill="both", expand=True)

        # Aparato
        ctk.CTkLabel(form_frame, text="Seleccione el aparato:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
        aparatos = self.controller.obtener_aparatos()
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
        horarios = self.controller.generar_horarios_disponibles()
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

            exito, mensaje = self.controller.crear_reserva(
                id_aparato,
                dia_combo.get(),
                hora_combo.get()
            )

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.mostrar_contenido_cliente("mis_reservas")
            else:
                messagebox.showerror("Error", mensaje)

        ctk.CTkButton(
            form_frame,
            text="✅ Confirmar Reserva",
            command=hacer_reserva,
            width=400,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=30)

    def contenido_mis_reservas(self):
        """Contenido de mis reservas"""
        ctk.CTkLabel(
            self.content_frame,
            text="📋 Mis Reservas",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=20)

        reservas = self.controller.obtener_mis_reservas()

        if not reservas:
            ctk.CTkLabel(
                self.content_frame,
                text="No tienes reservas activas",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            ).pack(pady=40)
            return

        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        for reserva in reservas:
            card = ctk.CTkFrame(scroll_frame)
            card.pack(fill="x", pady=5, padx=10)

            info_text = f"🏋️ {reserva['aparato']} ({reserva['tipo']})\n" \
                       f"📅 {reserva['dia']} | ⏰ {reserva['hora_inicio']} - {reserva['hora_fin']}"

            ctk.CTkLabel(
                card,
                text=info_text,
                font=ctk.CTkFont(size=14),
                justify="left"
            ).pack(side="left", pady=15, padx=20)

            ctk.CTkButton(
                card,
                text="❌ Cancelar",
                command=lambda r=reserva: self.cancelar_reserva(r['id']),
                width=100,
                fg_color="red",
                hover_color="darkred"
            ).pack(side="right", pady=10, padx=20)

    def cancelar_reserva(self, id_reserva: int):
        """Cancela una reserva"""
        if messagebox.askyesno("Confirmar", "¿Desea cancelar esta reserva?"):
            exito, mensaje = self.controller.eliminar_reserva(id_reserva)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.mostrar_contenido_cliente("mis_reservas")
            else:
                messagebox.showerror("Error", mensaje)

    def contenido_pagos(self):
        """Contenido de pagos"""
        ctk.CTkLabel(
            self.content_frame,
            text="💳 Gestión de Pagos",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=20)

        recibos = self.controller.obtener_mis_recibos()

        if not recibos:
            ctk.CTkLabel(
                self.content_frame,
                text="No hay recibos disponibles",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            ).pack(pady=40)
            return

        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        for recibo in recibos:
            card = ctk.CTkFrame(scroll_frame)
            card.pack(fill="x", pady=5, padx=10)

            mes_nombre = self.controller.obtener_nombre_mes(recibo['mes'])
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
                    command=lambda r=recibo: self.pagar_recibo(r['id']),
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

    def pagar_recibo(self, id_recibo: int):
        """Procesa el pago de un recibo"""
        if messagebox.askyesno("Confirmar Pago", "¿Desea confirmar el pago de este recibo?"):
            exito, mensaje = self.controller.pagar_recibo(id_recibo)
            if exito:
                messagebox.showinfo("Éxito", "Pago procesado correctamente")
                self.mostrar_contenido_cliente("pagos")
            else:
                messagebox.showerror("Error", mensaje)

    def contenido_horarios(self):
        """Contenido de horarios disponibles"""
        ctk.CTkLabel(
            self.content_frame,
            text="🕐 Horarios Ocupados",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=20)

        # Selector de día
        dia_frame = ctk.CTkFrame(self.content_frame)
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
        ocupacion_frame = ctk.CTkScrollableFrame(self.content_frame)
        ocupacion_frame.pack(fill="both", expand=True, padx=20, pady=20)

        def mostrar_ocupacion():
            for widget in ocupacion_frame.winfo_children():
                widget.destroy()

            ocupacion = self.controller.obtener_ocupacion_dia(dia_var.get())

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

    def cerrar_sesion(self):
        """Cierra la sesión del usuario"""
        if messagebox.askyesno("Cerrar Sesión", "¿Desea cerrar sesión?"):
            self.controller.logout()
            self.mostrar_login()
    def mostrar_dashboard_admin(self):
        """Muestra el dashboard del administrador (delegado a views.admin)"""
        admin_module.mostrar_dashboard_admin(self)

    def mostrar_contenido_admin(self, seccion: str):
        """Muestra el contenido según la sección del admin (delegado a views.admin)"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        admin_module.mostrar_contenido_admin(self, seccion)


if __name__ == "__main__":
    app = GymApp()
    app.mainloop()
