# 🚀 Quick Start - Sistema de Aprobación de Reservas

## Para Desarrolladores

### Métodos Rápidos

#### Cliente
```python
# Ver mis reservas con estados
reservas = controller.obtener_mis_reservas()
for r in reservas:
    print(f"{r['aparato']} - {r['dia']} {r['hora_inicio']}: {r['estado']}")
    # Salida: "Caminadora - Lunes 10:00: pendiente"

# Ver mis notificaciones
notificaciones = controller.obtener_mis_notificaciones()
for n in notificaciones:
    print(f"[{n['tipo'].upper()}] {n['mensaje']}")
    # Salida: "[ACEPTADA] Tu reserva para Caminadora...ha sido ACEPTADA ✅"

# Crear solicitud (no reserva)
exito, msg = controller.crear_reserva(
    id_aparato=1, 
    dia_semana='Lunes', 
    hora_inicio='10:00'
)
# Retorna: (True, "Solicitud de reserva enviada...")
```

#### Admin
```python
# Ver solicitudes pendientes
pendientes = controller.obtener_reservas_pendientes()
for p in pendientes:
    print(f"{p['cliente']} solicita {p['aparato']}")

# Aceptar una solicitud
exito, msg = controller.aceptar_reserva(id_reserva=5)
# Automáticamente:
# - Cambia estado a 'aceptada'
# - Crea notificación para cliente
# - Cliente es notificado

# Rechazar una solicitud
exito, msg = controller.rechazar_reserva(id_reserva=5)
# Automáticamente:
# - Cambia estado a 'rechazada'
# - Crea notificación para cliente
# - Cliente es notificado
```

---

## Puntos Clave

### 1. Estados son la clave
```python
estado = 'pendiente'    # Esperando aprobación
estado = 'aceptada'     # Aprobada y activa
estado = 'rechazada'    # Rechazada por admin
```

### 2. Disponibilidad solo cuenta aceptadas
```python
# Cuando cliente solicita, NO bloquea horario:
reserva = Reserva()
reserva.crear_reserva(...)  # estado='pendiente' → NO bloquea

# Solo cuando admin aprueba:
reserva.aceptar_reserva(...)  # estado='aceptada' → BLOQUEA
```

### 3. Notificaciones automáticas
```python
# NO necesita código especial en views
# Cuando admin hace clic en "Aceptar":
exito, msg = controller.aceptar_reserva(id_reserva)
# Internamente: crea notificación automáticamente

# Cliente ve en "Mis Notificaciones"
notificaciones = controller.obtener_mis_notificaciones()
```

---

## Base de Datos - Queries Útiles

```sql
-- Ver todas las solicitudes pendientes
SELECT * FROM reservas WHERE estado = 'pendiente';

-- Ver aparatos disponibles (sin reservas aceptadas)
SELECT DISTINCT a.* FROM aparatos a
WHERE a.id_aparato NOT IN (
    SELECT id_aparato FROM reservas 
    WHERE estado = 'aceptada'
    AND dia_semana = 'Lunes'
    AND hora_inicio = '10:00'
);

-- Ver notificaciones no leídas de un cliente
SELECT * FROM notificaciones 
WHERE id_cliente = 3 AND leida = 0;

-- Ver historial de decisiones del admin
SELECT r.*, n.tipo, n.mensaje 
FROM reservas r
LEFT JOIN notificaciones n ON r.id_reserva = n.id_reserva
ORDER BY r.fecha_reserva DESC;
```

---

## Testing

### Test Cliente
```python
# 1. Cliente crea solicitud
exito, msg = controller.crear_reserva(1, 'Lunes', '10:00')
assert exito == True
assert 'Solicitud' in msg

# 2. Ver en estado PENDIENTE
reservas = controller.obtener_mis_reservas()
assert reservas[0]['estado'] == 'pendiente'

# 3. Ver notificación después de aprobación
# (Hecho por admin en otro lado)
notificaciones = controller.obtener_mis_notificaciones()
assert len(notificaciones) > 0
assert 'ACEPTADA' in notificaciones[0]['mensaje']
```

### Test Admin
```python
# 1. Ver pendientes
pendientes = controller.obtener_reservas_pendientes()
assert len(pendientes) > 0

# 2. Aceptar
exito, msg = controller.aceptar_reserva(pendientes[0]['id'])
assert exito == True

# 3. Verificar cambio de estado
todas = controller.obtener_todas_reservas()
reserva_aprobada = [r for r in todas if r['id'] == pendientes[0]['id']][0]
assert reserva_aprobada['estado'] == 'aceptada'
```

---

## Troubleshooting

### Error: "no such column: estado"
**Solución**: La BD antigua necesita migración
```python
# Se ejecuta automáticamente al iniciar la aplicación
# Si no funciona, eliminar gimnasio.db y reiniciar
```

### Error: "no such table: notificaciones"
**Solución**: La tabla se crea automáticamente
```python
# Se ejecuta en _execute_migrations()
# Reiniciar la aplicación
```

### Cliente no ve notificación
**Solución**: Verificar que la reserva fue aceptada
```python
# 1. Admin debe haber hecho clic en "Aceptar"
# 2. Esto cambia estado a 'aceptada' Y crea notificación
# 3. Cliente puede ver en "Mis Notificaciones"
```

### Dos clientes pueden solicitar el mismo horario
**Esto es CORRECTO** - El sistema permite múltiples solicitudes:
```
Juan solicita Lunes 10:00   → pendiente (NO bloquea)
María solicita Lunes 10:00  → pendiente (NO bloquea)
Admin aprueba Juan          → Juan = aceptada (BLOQUEA)
Admin intenta aprobar María → ERROR (ya está ocupado)
```

---

## Checklist de Desarrollo

- [ ] Base de datos con tabla `reservas.estado`
- [ ] Base de datos con tabla `notificaciones`
- [ ] Clase `Notificacion` en models.py
- [ ] Métodos en `Reserva`: aceptar, rechazar, pendientes
- [ ] Métodos en `ReservationService`: aceptar, rechazar
- [ ] Métodos en `GymController`: aceptar, rechazar, pendientes
- [ ] UI Cliente: Mostrar estado en "Mis Reservas"
- [ ] UI Admin: Sección "Pendientes" con Aceptar/Rechazar
- [ ] Migración automática en `_execute_migrations()`
- [ ] Tests unitarios (opcional pero recomendado)

---

## Archivos Importantes

```
core/
├── core/models/                 ← Clase Reserva + Notificacion
├── core/controller/gym_controller.py  ← Métodos públicos
└── services/
    ├── reservation_service.py   ← Aceptar/Rechazar
    └── notification_service.py  ← NEW: Notificaciones

views/
├── client.py                    ← Muestra estado
└── admin.py                     ← Panel de aprobación

docs/
├── SISTEMA_APROBACION_RESERVAS.md           ← Documentación completa
├── DIAGRAMA_FLUJO_RESERVAS.md               ← Diagramas visuales
└── IMPLEMENTACION_APROBACION_RESERVAS.md    ← Este archivo
```

---

## Referencias Rápidas

| Necesidad | Método | Retorno |
|-----------|--------|---------|
| Ver reservas con estado | `obtener_mis_reservas()` | `[{...,'estado':'pendiente'}]` |
| Ver solicitudes sin aprobar | `obtener_reservas_pendientes()` | `[{...}]` |
| Aprobar solicitud | `aceptar_reserva(id)` | `(bool, str)` |
| Rechazar solicitud | `rechazar_reserva(id)` | `(bool, str)` |
| Ver notificaciones | `obtener_mis_notificaciones()` | `[{...,'tipo':'aceptada'}]` |
| Marcar notificación leída | `marcar_notificacion_leida(id)` | `(bool, str)` |
| Contar no leídas | `obtener_notificaciones_no_leidas()` | `int` |

---

## Tips de Implementación

✅ **DO:**
- Llamar `aceptar_reserva()` cuando admin hace clic en "Aceptar"
- Llamar `rechazar_reserva()` cuando admin hace clic en "Rechazar"
- Mostrar estado con colores en "Mis Reservas"
- Notificar automáticamente (ya está hecho en el servicio)

❌ **DON'T:**
- No crear directamente en tabla notificaciones
- No cambiar estado manualmente (usar métodos)
- No bloquear horarios con estado 'pendiente'
- No mostrar botón "Cancelar" en reservas aceptadas/rechazadas

---

## Performance

- Queries optimizadas con `CHECK (estado IN (...))`
- Índice implícito en foreign keys
- Las notificaciones se guardan una sola vez
- No hay loops innecesarios

**Nota**: Si hay +1000 reservas/día, considerar agregar índice:
```sql
CREATE INDEX idx_reservas_estado ON reservas(estado);
CREATE INDEX idx_notificaciones_cliente ON notificaciones(id_cliente);
```

---

## Para Preguntas

Consultar:
1. `docs/SISTEMA_APROBACION_RESERVAS.md` - Documentación técnica
2. `docs/DIAGRAMA_FLUJO_RESERVAS.md` - Diagramas visuales
3. Docstrings en el código (Python)
4. Este archivo (Quick Start)
