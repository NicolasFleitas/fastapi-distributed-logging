"""
Configuración compartida de la aplicación de logging.
Contiene los tokens de autenticación y mensajes de prueba para simuladores.
"""

# ==================== AUTENTICACIÓN ====================
# Tokens de servicios - Usados tanto en producción (main.py) como en test (simulators)
# En un sistema real, estos deberían estar en variables de entorno o un gestor de secretos
SERVICE_TOKENS = {
    "pagos": "tok_pagos_prod_a1b2c3d4e5f6",
    "ventas": "tok_ventas_prod_g7h8i9j0k1l2",
    "auth": "tok_auth_prod_m3n4o5p6q7r8",
    "notificaciones": "tok_notif_prod_s9t0u1v2w3x4",
    "inventario": "tok_invent_prod_y5z6a7b8c9d0",
}

# ==================== DATOS DE PRUEBA ====================
# Mensajes específicos por servicio con sus severidades apropiadas
# Cada mensaje es una tupla de (severity, message)
# Solo se usa en los simuladores para generar logs de prueba realistas
SERVICE_MESSAGES = {
    "pagos": [
        ("INFO", "Pago procesado exitosamente - Monto: $2500"),
        ("INFO", "Pago aprobado - Transacción completada"),
        ("ERROR", "Error al procesar tarjeta de crédito - Fondos insuficientes"),
        ("ERROR", "Pago rechazado - Tarjeta vencida"),
        ("WARNING", "Timeout con gateway de pago - Stripe"),
        ("INFO", "Reembolso iniciado para pedido #12345"),
        ("CRITICAL", "Sistema de pagos fuera de línea"),
        ("DEBUG", "Validando datos de tarjeta"),
    ],
    "ventas": [
        ("INFO", "Nueva venta registrada - Producto: Laptop HP"),
        ("INFO", "Descuento aplicado: Black Friday 20%"),
        ("INFO", "Venta completada exitosamente"),
        ("WARNING", "Stock bajo detectado en producto ID 456"),
        ("WARNING", "Carrito abandonado después de 30 minutos"),
        ("ERROR", "Venta cancelada por el cliente"),
        ("DEBUG", "Calculando totales de venta"),
        ("CRITICAL", "Error en sistema de inventario - ventas bloqueadas"),
    ],
    "auth": [
        ("INFO", "Usuario logueado exitosamente - ID: user_789"),
        ("INFO", "Logout realizado - Sesión cerrada"),
        ("INFO", "Token JWT renovado para sesión activa"),
        ("WARNING", "Intento de login fallido - Contraseña incorrecta"),
        ("WARNING", "Sesión expirada - Re-autenticación requerida"),
        ("ERROR", "Cuenta bloqueada después de múltiples intentos fallidos"),
        ("CRITICAL", "Intento sospechoso de acceso bloqueado - IP: 192.168.1.100"),
        ("DEBUG", "Validando credenciales de usuario"),
    ],
    "notificaciones": [
        ("INFO", "Email enviado correctamente - Confirmación de orden"),
        ("INFO", "Push notification enviada - 1500 usuarios"),
        ("INFO", "Webhook recibido de sistema externo"),
        ("WARNING", "Email rebotado - Buzón lleno"),
        ("ERROR", "SMS fallido - Número inválido"),
        ("ERROR", "Fallo en servidor SMTP - reintentar envío"),
        ("CRITICAL", "Servicio de notificaciones no disponible"),
        ("DEBUG", "Preparando mensaje para envío"),
    ],
    "inventario": [
        ("INFO", "Stock actualizado - Producto: Mouse Logitech (+50 unidades)"),
        ("INFO", "Transferencia entre almacenes completada"),
        ("INFO", "Orden de reabastecimiento creada"),
        ("WARNING", "Alerta: Stock crítico en producto ID 321"),
        ("WARNING", "Producto marcado como discontinuado"),
        ("ERROR", "Error al sincronizar inventario con almacén central"),
        ("CRITICAL", "Discrepancia detectada en conteo de inventario"),
        ("DEBUG", "Verificando disponibilidad de producto"),
    ]
}
