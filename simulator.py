import requests
import random
import time
from datetime import datetime

# CONFIGURACIÓN
API_URL = "http://127.0.0.1:8000/logs"

# Mapeo de servicios a sus tokens (debe coincidir con main.py)
SERVICE_TOKENS = {
    "pagos": "tok_pagos_prod_a1b2c3d4e5f6",
    "ventas": "tok_ventas_prod_g7h8i9j0k1l2",
    "auth": "tok_auth_prod_m3n4o5p6q7r8",
    "notificaciones": "tok_notif_prod_s9t0u1v2w3x4",
    "inventario": "tok_invent_prod_y5z6a7b8c9d0",
}

SEVERITIES = ["INFO", "WARNING", "ERROR", "CRITICAL", "DEBUG"]

# Mensajes específicos por servicio para mayor realismo
SERVICE_MESSAGES = {
    "pagos": [
        "Pago procesado exitosamente - Monto: $2500",
        "Error al procesar tarjeta de crédito - Fondos insuficientes",
        "Timeout con gateway de pago - Stripe",
        "Reembolso iniciado para pedido #12345",
        "Pago rechazado - Tarjeta vencida"
    ],
    "ventas": [
        "Nueva venta registrada - Producto: Laptop HP",
        "Descuento aplicado: Black Friday 20%",
        "Stock bajo detectado en producto ID 456",
        "Carrito abandonado después de 30 minutos",
        "Venta cancelada por el cliente"
    ],
    "auth": [
        "Usuario logueado exitosamente - ID: user_789",
        "Intento de login fallido - Contraseña incorrecta",
        "Token JWT renovado para sesión activa",
        "Logout realizado - Sesión cerrada",
        "Intento sospechoso de acceso bloqueado - IP: 192.168.1.100"
    ],
    "notificaciones": [
        "Email enviado correctamente - Confirmación de orden",
        "SMS fallido - Número inválido",
        "Push notification enviada - 1500 usuarios",
        "Email rebotado - Buzón lleno",
        "Webhook recibido de sistema externo"
    ],
    "inventario": [
        "Stock actualizado - Producto: Mouse Logitech (+50 unidades)",
        "Alerta: Stock crítico en producto ID 321",
        "Transferencia entre almacenes completada",
        "Producto marcado como discontinuado",
        "Orden de reabastecimiento creada"
    ]
}

def generate_log():
    """Crea un diccionario con datos aleatorios para el log."""
    # Elegir un servicio al azar
    service = random.choice(list(SERVICE_TOKENS.keys()))
    
    return {
        "service": service,
        "severity": random.choice(SEVERITIES),
        "message": random.choice(SERVICE_MESSAGES[service]),
        "timestamp": datetime.now().isoformat()
    }, service

def send_log():
    """Genera un log y lo envía al servidor."""
    data, service = generate_log()
    
    # Usar el token específico del servicio
    token = SERVICE_TOKENS[service]
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        
        if response.status_code == 201:
            emoji = "✅" if data['severity'] in ["INFO", "DEBUG"] else "⚠️" if data['severity'] == "WARNING" else "❌"
            print(f"{emoji} [{data['service'].upper()}] {data['severity']}: {data['message'][:60]}...")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"🔥 El servidor no responde: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando simulación de tráfico distribuido...")
    print(f"📡 Simulando {len(SERVICE_TOKENS)} servicios diferentes")
    print("=" * 80)
    
    # Bucle infinito para bombardear al servidor
    # Pulsa Ctrl+C para detenerlo
    try:
        while True:
            send_log()
            # Esperamos un poco entre logs para poder leer la consola (0.5 segundos)
            time.sleep(random.uniform(0.1, 0.5))
    except KeyboardInterrupt:
        print("\n\n👋 Simulación detenida por el usuario")