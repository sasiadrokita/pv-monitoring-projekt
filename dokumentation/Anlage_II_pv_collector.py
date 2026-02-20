import os
import time
import json
import logging
from datetime import datetime
import paho.mqtt.client as mqtt
import minimalmodbus
import serial

# --- KONFIGURACJA ---
# MQTT
MQTT_BROKER = os.getenv("MQTT_BROKER_HOST", "mosquitto")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "pv/anlage/data")

# Modbus (Licznik SDM120)
MODBUS_PORT = os.getenv("MODBUS_PORT", "/dev/ttyUSB0")
MODBUS_BAUDRATE = int(os.getenv("MODBUS_BAUDRATE", 9600))
SLAVE_ID = 1

# Plik do zapisu stanu (żeby pamiętać stan licznika o północy)
STATE_FILE = "/app/data/meter_state.json"

# Konfiguracja logowania
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

# --- ZMIENNE STANU ---
midnight_counter_kwh = 0.0  # Stan licznika o północy
last_reset_day = -1

def load_state():
    """Wczytuje stan początkowy (stan licznika z początku dnia)."""
    global midnight_counter_kwh, last_reset_day
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                midnight_counter_kwh = state.get('midnight_kwh', 0.0)
                last_reset_day = state.get('day', -1)
                logging.info(f"Stan wczytany. Start dnia: {midnight_counter_kwh} kWh")
        except Exception as e:
            logging.error(f"Błąd odczytu stanu: {e}")

def save_state(current_total_kwh):
    """Zapisuje stan licznika (jako punkt odniesienia dla nowego dnia)."""
    global midnight_counter_kwh, last_reset_day
    now = datetime.now()
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        state = {
            'midnight_kwh': current_total_kwh,
            'day': now.day,
            'updated': str(now)
        }
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
        
        midnight_counter_kwh = current_total_kwh
        last_reset_day = now.day
        logging.info(f"ZAPISANO NOWY DZIEŃ. Start dnia ustawiony na: {current_total_kwh} kWh")
    except Exception as e:
        logging.error(f"Błąd zapisu stanu: {e}")

def get_modbus_data(instrument):
    """Odczytuje rejestry z Eastron SDM120 przy użyciu minimalmodbus."""
    data = {}
    try:
        # Rejestry Input (Func 04) dla SDM120
        # read_float(registeraddress, functioncode=3/4, number_of_registers=2)
        
        # 1. Napięcie (0x0000) -> 0
        data["spannung_V"] = round(instrument.read_float(0, functioncode=4, number_of_registers=2), 2)
        
        # 2. Prąd (0x0006) -> 6
        data["strom_A"] = abs(round(instrument.read_float(6, functioncode=4, number_of_registers=2), 2))

        # 3. Moc (0x000C) -> 12
        data["leistung_W"] = abs(round(instrument.read_float(12, functioncode=4, number_of_registers=2), 2))

        # 4. Energia Całkowita (0x0156) -> 342
        data["total_kwh"] = abs(round(instrument.read_float(342, functioncode=4, number_of_registers=2), 4))

        return data

    except Exception as e:
        logging.error(f"Błąd odczytu Modbus: {e}")
        return None

def main():
    global midnight_counter_kwh, last_reset_day
    
    # 1. Load State
    load_state()

    # 2. Setup MQTT
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    try:
        mqtt_client.connect(MQTT_BROKER, 1883, 60)
        mqtt_client.loop_start()
        logging.info(f"Połączono z MQTT: {MQTT_BROKER}")
    except Exception as e:
        logging.error(f"Błąd MQTT: {e}")
        return

    # 3. Setup Modbus (minimalmodbus)
    try:
        instrument = minimalmodbus.Instrument(MODBUS_PORT, SLAVE_ID)
        instrument.serial.baudrate = MODBUS_BAUDRATE
        instrument.serial.bytesize = 8
        instrument.serial.parity = serial.PARITY_NONE
        instrument.serial.stopbits = 1
        instrument.serial.timeout = 1
        logging.info(f"Skonfigurowano Modbus: {MODBUS_PORT} @ {MODBUS_BAUDRATE} baud")
    except Exception as e:
        logging.error(f"Błąd konfiguracji Modbus: {e}")
        return

    logging.info("Start pętli odczytu...")

    while True:
        try:
            # Read Data
            readings = get_modbus_data(instrument)
            
            if readings and "total_kwh" in readings:
                current_total = readings["total_kwh"]
                now = datetime.now()

                # Sprawdzenie zmiany dnia (Reset licznika dziennego)
                if last_reset_day != now.day:
                    logging.info("Wykryto zmianę dnia. Resetuję licznik dzienny.")
                    save_state(current_total)
                
                # Inicjalizacja przy pierwszym uruchomieniu
                if midnight_counter_kwh == 0.0 and current_total > 0:
                    save_state(current_total)

                # Obliczenie produkcji dziennej
                daily_yield = current_total - midnight_counter_kwh
                if daily_yield < 0: daily_yield = 0.0 

                # Przygotowanie JSON
                payload = {
                    "spannung_V": readings.get("spannung_V", 0.0),
                    "strom_A": readings.get("strom_A", 0.0),
                    "leistung_W": readings.get("leistung_W", 0.0),
                    "tagesertrag_kWh": round(daily_yield, 3),
                    "total_kWh": current_total,
                    "timestamp": int(time.time())
                }

                # Wysyłka MQTT
                mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
                logging.info(f"Wysłano: {payload['leistung_W']}W | Dziś: {payload['tagesertrag_kWh']}kWh | V: {payload['spannung_V']}V")
            
            else:
                logging.warning("Brak poprawnych danych z licznika.")

            time.sleep(5) 

        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error(f"Błąd w pętli głównej: {e}")
            time.sleep(10)

    mqtt_client.loop_stop()

if __name__ == "__main__":
    main()
