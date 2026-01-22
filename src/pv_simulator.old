import paho.mqtt.client as mqtt
import time
import json
import random
import os
import math
from datetime import datetime

# --- Konfiguracja ---
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "pv/anlage/data")
SIMULATION_INTERVAL = int(os.getenv("SIMULATION_INTERVAL", 5))

# Ścieżka do pliku, w którym zapiszemy stan licznika
STATE_FILE = "/app/data/simulation_state.json"

# Parametry instalacji
MAX_POWER_W = 3000.0
MPP_VOLTAGE_OPTIMAL = 450.0
MPP_VOLTAGE_MIN = 250.0
MPP_VOLTAGE_MAX = 550.0

# Parametry czasu
SUNRISE_HOUR = 6
SUNSET_HOUR = 20

# --- Zmienne stanu (domyślne) ---
tagesertrag_kwh = 0.0
last_reset_day = -1
current_mpp_voltage = MPP_VOLTAGE_OPTIMAL

def load_state():
    """Wczytuje stan symulacji z pliku JSON przy starcie."""
    global tagesertrag_kwh, last_reset_day
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                # Sprawdzamy, czy wczytany stan jest z dzisiaj
                saved_day = state.get('day', -1)
                current_day = datetime.now().day
                
                if saved_day == current_day:
                    tagesertrag_kwh = state.get('tagesertrag_kWh', 0.0)
                    last_reset_day = saved_day
                    print(f"--- PRZYWRÓCONO STAN: {tagesertrag_kwh} kWh ---")
                else:
                    print("--- NOWY DZIEŃ: Reset licznika ---")
                    tagesertrag_kwh = 0.0
                    last_reset_day = current_day
        except Exception as e:
            print(f"Błąd odczytu stanu: {e}")
    else:
        print("--- BRAK PLIKU STANU: Start od zera ---")

def save_state():
    """Zapisuje aktualny stan licznika do pliku."""
    try:
        # Upewnij się, że katalog istnieje
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        
        state = {
            'tagesertrag_kWh': tagesertrag_kwh,
            'day': datetime.now().day,
            'timestamp': int(time.time())
        }
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    except Exception as e:
        print(f"Błąd zapisu stanu: {e}")

def connect_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="pv_simulator_client")
    try:
        client.connect(MQTT_BROKER_HOST, 1883)
    except Exception as e:
        print(f"Błąd MQTT: {e}")
        return None
    return client

def get_seasonal_factor(now):
    day_of_year = now.timetuple().tm_yday
    return (math.cos(2 * math.pi * (day_of_year - 172) / 365) + 1) * 0.35 + 0.3

def get_daily_curve_factor(now):
    if not (SUNRISE_HOUR <= now.hour < SUNSET_HOUR):
        return 0.0
    day_progress = (now.hour + now.minute / 60 - SUNRISE_HOUR) / (SUNSET_HOUR - SUNRISE_HOUR)
    return pow(math.sin(day_progress * math.pi), 1.5)

def get_weather_factor():
    # Prosta symulacja chmur
    if random.random() < 0.05: return 0.4
    return random.uniform(0.95, 1.0)

def simulate_data(client):
    global tagesertrag_kwh, last_reset_day, current_mpp_voltage
    
    # 1. Wczytaj stan przy starcie
    load_state()
    
    client.loop_start()
    
    while True:
        try:
            now = datetime.now()

            # Reset o północy (jeśli skrypt działa ciągle)
            if now.day != last_reset_day:
                tagesertrag_kwh = 0.0
                last_reset_day = now.day
                save_state() # Zapisz reset

            # --- Fizyka (Uproszczona) ---
            seasonal = get_seasonal_factor(now)
            daily = get_daily_curve_factor(now)
            weather = get_weather_factor()
            
            # Symulacja MPPT
            current_mpp_voltage += random.uniform(-15.0, 15.0)
            current_mpp_voltage = max(MPP_VOLTAGE_MIN, min(current_mpp_voltage, MPP_VOLTAGE_MAX))
            voltage_efficiency = 1.0 - ((current_mpp_voltage - MPP_VOLTAGE_OPTIMAL) / (MPP_VOLTAGE_MAX - MPP_VOLTAGE_MIN))**2
            
            # Moc
            leistung_w = MAX_POWER_W * seasonal * daily * weather * voltage_efficiency
            leistung_w = max(0, leistung_w)

            # Prąd
            strom_a = leistung_w / current_mpp_voltage if current_mpp_voltage > 0 else 0

            # Uzysk (całkowanie)
            energie_intervall_wh = leistung_w * (SIMULATION_INTERVAL / 3600.0)
            tagesertrag_kwh += energie_intervall_wh / 1000.0

            # 2. Zapisz stan po każdej aktualizacji
            save_state()

            # Wysyłka
            data = {
                "spannung_V": round(current_mpp_voltage, 2),
                "strom_A": round(strom_a, 2),
                "leistung_W": round(leistung_w, 2),
                "tagesertrag_kWh": round(tagesertrag_kwh, 4),
                "timestamp": int(time.time())
            }

            client.publish(MQTT_TOPIC, json.dumps(data))
            print(f"[{now.strftime('%H:%M:%S')}] P: {int(leistung_w)}W | Total: {tagesertrag_kwh:.3f} kWh")

            time.sleep(SIMULATION_INTERVAL)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

    client.loop_stop()

if __name__ == "__main__":
    mqtt_client = connect_mqtt()
    if mqtt_client:
        simulate_data(mqtt_client)
