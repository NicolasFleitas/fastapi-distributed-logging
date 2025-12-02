import requests
import random
import time
from datetime import datetime
from config import SERVICE_TOKENS, SERVICE_MESSAGES

# CONFIGURACIÓN
API_URL = "http://127.0.0.1:8000/logs"

def generate_log():
    """Crea un diccionario con datos aleatorios para el log."""
    # Elegir un servicio al azar
    service = random.choice(list(SERVICE_TOKENS.keys()))
    
    # Elegir un mensaje con su severidad apropiada
    severity, message = random.choice(SERVICE_MESSAGES[service])
    
    return {
        "service": service,
        "severity": severity,
        "message": message,
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
            print(f"[{data['severity']}] [{data['service'].upper()}]: {data['message'][:60]}...")
        else:
            print(f"[ERROR] Status {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"[SERVER_ERROR] El servidor no responde: {e}")

if __name__ == "__main__":
    print("--- Iniciando simulación de tráfico distribuido ---")
    print(f"Simulando {len(SERVICE_TOKENS)} servicios diferentes")
    print("=" * 80)
    
    # Bucle infinito para enviar logs
    # Ctrl+C para detenerlo
    try:
        while True:
            send_log()
            time.sleep(random.uniform(0.1, 0.5))
    except KeyboardInterrupt:
        print("\n\n--- Simulación detenida por el usuario ---")