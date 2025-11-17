import paho.mqtt.client as mqtt
import time
import json
import random
import os
import math
from datetime import datetime

# --- Konfiguracja Symulacji (rozbudowana) ---
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "pv/anlage/data")
SIMULATION_INTERVAL = int(os.getenv("SIMULATION_INTERVAL", 10))

# Parametry charakterystyczne dla stringu paneli PV
MAX_POWER_W = 3000.0          # Moc maksymalna instalacji w idealny letni dzień [W]
MPP_VOLTAGE_OPTIMAL = 450.0   # Optymalne napięcie pracy falownika [V]
MPP_VOLTAGE_MIN = 250.0       # Minimalne napięcie pracy
MPP_VOLTAGE_MAX = 550.0       # Maksymalne napięcie pracy

# *** NOWA SEKCJA: Parametry realistycznej symulacji ***
SUNRISE_HOUR = 6              # Uproszczona godzina wschodu słońca
SUNSET_HOUR = 20              # Uproszczona godzina zachodu słońca

# Parametry pogodowe
CLOUDINESS_LEVEL = 0.95       # Współczynnik "czystego nieba" (1.0 = idealnie, 0.7 = lekkie zamglenie)
CLOUD_CHANCE = 0.05           # Szansa (0 do 1) na pojawienie się dużej chmury w danym cyklu
CLOUD_IMPACT = 0.4            # Jak bardzo chmura redukuje moc (0.4 = redukcja o 60%)

# --- Zmienne stanu symulacji ---
tagesertrag_kwh = 0.0
current_mpp_voltage = MPP_VOLTAGE_OPTIMAL
last_reset_day = -1 # Zmienna do śledzenia dnia w celu resetowania uzysku

def connect_mqtt():
    """Nawiązuje połączenie z brokerem MQTT."""
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Pomyślnie połączono z brokerem MQTT")
        else:
            print(f"Nie udało się połączyć, kod błędu: {rc}")
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="pv_simulator_client")
    client.on_connect = on_connect
    try:
        client.connect(MQTT_BROKER_HOST, 1883)
    except Exception as e:
        print(f"Błąd podczas łączenia z MQTT: {e}")
        return None
    return client

# *** NOWA FUNKCJA: Współczynnik pory roku ***
def get_seasonal_factor(now):
    """Zwraca współczynnik pory roku (ok. 0.3 zimą, 1.0 latem)."""
    day_of_year = now.timetuple().tm_yday
    # Używamy funkcji cosinus, aby stworzyć roczną falę
    # Przesuwamy ją, aby szczyt był w lecie (ok. 172 dzień roku - okolice 21 czerwca)
    cos_arg = 2 * math.pi * (day_of_year - 172) / 365
    # Skalujemy wynik z zakresu [-1, 1] do [0.3, 1.0] (zima ma ~30% mocy lata)
    return (math.cos(cos_arg) + 1) * 0.35 + 0.3

# *** ZMODYFIKOWANA FUNKCJA: Krzywa dzienna oparta na realnym czasie ***
def get_daily_curve_factor(now):
    """Zwraca współczynnik pory dnia (0 w nocy, 1 w południe) na podstawie aktualnego czasu."""
    if not (SUNRISE_HOUR <= now.hour < SUNSET_HOUR):
        return 0.0 # Noc

    # Obliczamy postęp dnia jako wartość od 0 (wschód) do 1 (zachód)
    day_progress = (now.hour + now.minute / 60 - SUNRISE_HOUR) / (SUNSET_HOUR - SUNRISE_HOUR)
    
    # Używamy funkcji sinus do stworzenia krzywej dzwonowej
    sin_val = math.sin(day_progress * math.pi)
    
    # Podniesienie do potęgi > 1 sprawia, że krzywa jest bardziej "spiczasta" w południe
    return pow(sin_val, 1.5)

# *** NOWA FUNKCJA: Współczynnik pogody ***
def get_weather_factor():
    """Zwraca współczynnik pogody (losowe chmury)."""
    base_weather = random.uniform(CLOUDINESS_LEVEL, 1.0)
    
    if random.random() < CLOUD_CHANCE:
        print("-> Symulacja chmury!")
        return base_weather * CLOUD_IMPACT
    
    return base_weather

def simulate_data(client):
    """Główna pętla symulacji i publikacji danych."""
    global tagesertrag_kwh, current_mpp_voltage, last_reset_day
    
    client.loop_start()
    
    while True:
        try:
            now = datetime.now()

            # *** ZMIANA: Inteligentne zerowanie uzysku dziennego o północy ***
            if now.day != last_reset_day:
                print(f"Nowy dzień ({now.day}), zerowanie licznika uzysku dziennego.")
                tagesertrag_kwh = 0.0
                last_reset_day = now.day

            # === LOGIKA SYMULACJI ===
            # 1. Pobranie wszystkich współczynników środowiskowych
            seasonal_factor = get_seasonal_factor(now)
            daily_factor = get_daily_curve_factor(now)
            weather_factor = get_weather_factor()
            
            # 2. Symulacja pracy falownika MPPT (logika z Twojego kodu - bez zmian)
            voltage_change = random.uniform(-15.0, 15.0)
            current_mpp_voltage += voltage_change
            current_mpp_voltage = max(MPP_VOLTAGE_MIN, min(current_mpp_voltage, MPP_VOLTAGE_MAX))
            
            # 3. Obliczenie mocy z uwzględnieniem wszystkich czynników
            voltage_efficiency = 1.0 - ((current_mpp_voltage - MPP_VOLTAGE_OPTIMAL) / (MPP_VOLTAGE_MAX - MPP_VOLTAGE_MIN))**2
            
            # *** ZMIANA: Mnożymy wszystkie czynniki razem ***
            ideal_power = MAX_POWER_W * seasonal_factor * daily_factor * weather_factor
            aktuelle_leistung_w = ideal_power * voltage_efficiency
            aktuelle_leistung_w = max(0, aktuelle_leistung_w)

            # 4. Obliczenie PRĄDU (I = P / U) - bez zmian
            strom_a = aktuelle_leistung_w / current_mpp_voltage if current_mpp_voltage > 0 else 0

            # 5. Obliczenie DZIENNEGO UZYSKU - bez zmian
            energie_intervall_wh = aktuelle_leistung_w * (SIMULATION_INTERVAL / 3600.0)
            tagesertrag_kwh += energie_intervall_wh / 1000.0

            # === Przygotowanie danych do wysyłki (format JSON z Twojego kodu) ===
            data = {
                "spannung_V": round(current_mpp_voltage, 2),
                "strom_A": round(strom_a, 2),
                "leistung_W": round(aktuelle_leistung_w, 2),
                "tagesertrag_kWh": round(tagesertrag_kwh, 2),
                "timestamp": int(time.time())
            }

            payload = json.dumps(data)
            result = client.publish(MQTT_TOPIC, payload)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"[{now.strftime('%H:%M:%S')}] P: {data['leistung_W']} W, U: {data['spannung_V']} V, I: {data['strom_A']} A, Uzysk: {data['tagesertrag_kWh']} kWh")
            else:
                print(f"Fehler beim Senden, Code: {result.rc}")

            time.sleep(SIMULATION_INTERVAL)

        except KeyboardInterrupt:
            print("Symulacja zatrzymana.")
            break
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd w pętli: {e}")
            time.sleep(10)

    client.loop_stop()

if __name__ == "__main__":
    mqtt_client = connect_mqtt()
    if mqtt_client:
        simulate_data(mqtt_client)
    else:
        print("Nie można uruchomić symulacji - brak połączenia z MQTT.")
