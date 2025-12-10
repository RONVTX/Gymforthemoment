# 📅 Sistema de Aprobación de Reservas

## Descripción General

Se ha implementado un nuevo flujo de reservas donde los clientes **solicitan** reservas y el administrador **aprueba o rechaza** estas solicitudes, notificando automáticamente al cliente sobre la decisión.

## 🔄 Flujo de Funcionamiento

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO DE RESERVAS                         │
└─────────────────────────────────────────────────────────────┘

1. CLIENTE SOLICITA RESERVA
   ├─ Cliente entra a "Hacer Reserva"
   ├─ Selecciona: Aparato, Día, Hora
   ├─ Hace clic en "Solicitar Reserva"
   └─ Reserva se crea con estado: PENDIENTE ⏳

2. ADMIN REVISA SOLICITUDES
   ├─ Admin entra a "Reservas"
   ├─ Ve sección "RESERVAS PENDIENTES"
   ├─ Puede ver: Cliente, Aparato, Día, Hora
   └─ Opciones: ✅ Aceptar | ❌ Rechazar

3. ADMIN ACEPTA/RECHAZA
   ├─ Si ACEPTA:
   │  ├─ Reserva cambia a estado: ACEPTADA ✅
   │  ├─ Se crea NOTIFICACIÓN para el cliente
   │  └─ Cliente recibe confirmación
   │
   └─ Si RECHAZA:
      ├─ Reserva cambia a estado: RECHAZADA ❌
      ├─ Se crea NOTIFICACIÓN para el cliente
      └─ Cliente recibe aviso de rechazo

4. CLIENTE VE ESTADO
   ├─ Cliente entra a "Mis Reservas"
   ├─ Ve todas sus reservas con estado:
   │  ├─ 🟠 PENDIENTE - Esperando aprobación
   │  ├─ 🟢 ACEPTADA - Reserva confirmada
   │  └─ 🔴 RECHAZADA - Reserva no autorizada
   └─ Solo puede cancelar reservas PENDIENTES
```

## 📊 Estados de Reservas

| Estado | Color | Descripción | Acciones |
|--------|-------|-------------|----------|
| **pendiente** | 🟠 Naranja | Esperando revisión del admin | Cancelar |
| **aceptada** | 🟢 Verde | Aprobada y confirmada | Ninguna |
| **rechazada** | 🔴 Rojo | No aprobada | Ninguna |

## 💾 Cambios en Base de Datos

### Nueva Columna en `reservas`
```sql
ALTER TABLE reservas ADD COLUMN estado TEXT DEFAULT 'pendiente'
  CHECK (estado IN ('pendiente', 'aceptada', 'rechazada'));
```

### Nueva Tabla `notificaciones`
```sql
CREATE TABLE notificaciones (
    id_notificacion INTEGER PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    id_reserva INTEGER,
    tipo TEXT NOT NULL CHECK (tipo IN ('aceptada', 'rechazada')),
    mensaje TEXT NOT NULL,
    leida BOOLEAN DEFAULT 0,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY(id_reserva) REFERENCES reservas(id_reserva)
);
```

## 🛠️ Componentes Implementados

### Modelos (`core/models/`)

#### Clase `Reserva` - Nuevos métodos:
- `aceptar_reserva(id_reserva)` - Cambia estado a 'aceptada'
- `rechazar_reserva(id_reserva)` - Cambia estado a 'rechazada'
- `obtener_reservas_pendientes()` - Retorna reservas sin aprobar
- `obtener_id_cliente_por_reserva(id_reserva)` - Obtiene dueño de reserva

#### Nueva Clase `Notificacion`:
- `crear_notificacion()` - Crea notificación de aceptación/rechazo
- `obtener_por_cliente()` - Obtiene notificaciones de un cliente
- `marcar_como_leida()` - Marca notificación como leída
- `contar_no_leidas()` - Cuenta notificaciones pendientes

### Servicios (`core/services/`)

#### Actualización `ReservationService`:
- `aceptar_reserva()` - Acepta reserva y crea notificación
- `rechazar_reserva()` - Rechaza reserva y crea notificación
- `obtener_reservas_pendientes()` - Obtiene pendientes

#### Nuevo `NotificationService`:
- `crear_notificacion_reserva()` - Crea notificaciones automáticas
- `obtener_notificaciones_cliente()` - Obtiene notificaciones
- `marcar_como_leida()` - Marca como leída
- `obtener_notificaciones_no_leidas()` - Cuenta no leídas

### Controlador (`core/controller/gym_controller.py`)

Nuevos métodos disponibles:
```python
# Aprobación de reservas
obtener_reservas_pendientes()
aceptar_reserva(id_reserva)
rechazar_reserva(id_reserva)

# Gestión de notificaciones
obtener_mis_notificaciones()
obtener_notificaciones_no_leidas()
marcar_notificacion_leida(id_notificacion)
```

### Vistas (`views/`)

#### Cliente (`views/client.py`)
- **"Hacer Reserva"**: Botón cambiado de "Confirmar" a "Solicitar"
- **"Mis Reservas"**: Ahora muestra estado con colores y emojis
  - Reservas PENDIENTES: Mostrar botón cancelar
  - Reservas ACEPTADAS: Sin botones de acción
  - Reservas RECHAZADAS: Solo visualización

#### Admin (`views/admin.py`)
- Nueva sección: **"RESERVAS PENDIENTES"** (⏳)
  - Muestra cliente, aparato, día, hora
  - Botones: ✅ Aceptar | ❌ Rechazar
  - Botones con colores verde y rojo
  
- Nueva sección: **"RESERVAS ACEPTADAS"** (✅)
  - Reservas confirmadas para referencia
  - Botón: 🗑️ Eliminar (si es necesario)

## 🔍 Lógica de Disponibilidad

**Punto importante**: La disponibilidad de aparatos ahora solo cuenta **reservas aceptadas**:

```python
# En Reserva.verificar_disponibilidad():
SELECT COUNT(*)
FROM reservas
WHERE id_aparato = ?
  AND dia_semana = ?
  AND hora_inicio = ?
  AND estado = 'aceptada'  # ← Solo cuenta aceptadas
```

Esto significa:
- ✅ Múltiples clientes pueden solicitar el mismo horario
- ✅ El admin decide cuál solicitud se aprueba
- ✅ Solo las aprobadas bloquean el horario

## 📝 Ejemplos de Uso

### Cliente solicita reserva:
```python
# Cliente hace clic en "Solicitar Reserva"
exito, mensaje = controller.crear_reserva(
    id_aparato=5,
    dia_semana='Lunes',
    hora_inicio='10:00'
)
# Resultado: Reserva creada con estado='pendiente'
# Mensaje: "Solicitud de reserva enviada. El administrador la revisará"
```

### Admin aprueba reserva:
```python
# Admin hace clic en botón "Aceptar"
exito, mensaje = controller.aceptar_reserva(id_reserva=42)
# Resultado:
# - Reserva estado cambia a 'aceptada'
# - Se crea notificación para el cliente
# - Cliente es notificado automáticamente
```

### Cliente ve notificación:
```python
# Cliente abre la aplicación
notificaciones = controller.obtener_mis_notificaciones()
# Retorna:
# [{
#   'id': 1,
#   'tipo': 'aceptada',
#   'mensaje': 'Tu reserva para Caminadora el Lunes a las 10:00 ha sido ACEPTADA ✅',
#   'leida': False,
#   'fecha': '2025-12-10 14:30:00'
# }]
```

## 🚀 Cambios Técnicos

### Migración Automática
- El sistema detecta bases de datos existentes
- Agrega automáticamente la columna `estado` si falta
- Crea la tabla `notificaciones` si no existe
- Todo sin perder datos

### Cambios en Métodos Existentes

```python
# Antes:
reserva_service.crear_reserva()  # Creaba directamente confirmada

# Ahora:
reservation_service.crear_reserva()  # Crea con estado 'pendiente'
```

## ✅ Pruebas Recomendadas

1. **Crear solicitud de reserva** como cliente
   - Verificar que aparece con estado PENDIENTE
   - Verificar que no bloquea el horario

2. **Aceptar reserva** como admin
   - Verificar que estado cambia a ACEPTADA
   - Verificar que ahora bloquea el horario

3. **Rechazar reserva** como admin
   - Verificar que estado cambia a RECHAZADA
   - Verificar que permite otros solicitudes

4. **Ver notificaciones** como cliente
   - Aceptación: "Tu reserva...ha sido ACEPTADA ✅"
   - Rechazo: "Tu reserva...ha sido RECHAZADA ❌"

## 📋 Resumen de Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `core/models.py` | Nuevos métodos Reserva, Nueva clase Notificacion, Migración automática |
| `core/services/reservation_service.py` | Métodos aceptar/rechazar, Integración notificaciones |
| `core/services/notification_service.py` | ✨ Nuevo archivo |
| `core/controller.py` | Nuevos métodos públicos para notificaciones |
| `views/client.py` | Muestra estado en "Mis Reservas" |
| `views/admin.py` | Nueva UI con secciones pendientes/aceptadas |

## 🎯 Beneficios

✅ **Para Clientes:**
- Claridad sobre estado de solicitudes
- Notificación automática de aprobación/rechazo
- No pueden afectar horarios sin aprobación

✅ **Para Admin:**
- Control completo sobre qué reservas se aprueban
- Vista clara de solicitudes pendientes
- Puede rechazar sin afectar otras solicitudes

✅ **Para el Sistema:**
- Mayor control de recursos
- Prevención de overbooking
- Mejor gestión de disponibilidad
- Auditoría mediante notificaciones
