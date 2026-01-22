import os
import time
import json
import logging
from datetime import datetime
import paho.mqtt.client as mqtt
from pymodbus.client import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

# --- KONFIGURACJA ---
# MQTT
MQTT_BROKER = os.getenv("MQTT_BROKER_HOST", "mosquitto")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "pv/anlage/data")
# Modbus (Licznik SDM120)
MODBUS_PORT = os.getenv("MODBUS_PORT", "/dev/ttyUSB0")
MODBUS_BAUDRATE = int(os.getenv("MODBUS_BAUDRATE", 2400))
SLAVE_ID = 1

# Plik do zapisu stanu (żeby pamiętać stan licznika o północy)
# Ścieżka /app/data musi być zmapowana w docker-compose volumes
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

def get_modbus_data(client):
    """Odczytuje rejestry z Eastron SDM120."""
    data = {}
    try:
        # Rejestry Input (Func 04) dla SDM120
        # 0x0000: Voltage (V)
        # 0x0006: Current (A)
        # 0x000C: Active Power (W)
        # 0x0156: Total Active Energy (kWh)
        
        # Czytamy parametry elektryczne
        # 1. Napięcie (0x0000)
        rr = client.read_input_registers(address=0x0000, count=2, slave=SLAVE_ID)
        if not rr.isError():
            data["spannung_V"] = round(BinaryPayloadDecoder.fromRegisters(rr.registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_32bit_float(), 2)
        
        # 2. Prąd (0x0006)
        rr = client.read_input_registers(address=0x0006, count=2, slave=SLAVE_ID)
        if not rr.isError():
            data["strom_A"] = round(BinaryPayloadDecoder.fromRegisters(rr.registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_32bit_float(), 2)

        # 3. Moc (0x000C)
        rr = client.read_input_registers(address=0x000C, count=2, slave=SLAVE_ID)
        if not rr.isError():
            data["leistung_W"] = round(BinaryPayloadDecoder.fromRegisters(rr.registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_32bit_float(), 2)

        # 4. Energia Całkowita (0x0156)
        rr = client.read_input_registers(address=0x0156, count=2, slave=SLAVE_ID)
        if not rr.isError():
            data["total_kwh"] = round(BinaryPayloadDecoder.fromRegisters(rr.registers, byteorder=Endian.Big, wordorder=Endian.Big).decode_32bit_float(), 4)

        return data

    except Exception as e:
        logging.error(f"Modbus Exception: {e}")
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

    # 3. Setup Modbus
    modbus_client = ModbusSerialClient(
        port=MODBUS_PORT,
        baudrate=MODBUS_BAUDRATE,
        parity='N',
        stopbits=1,
        bytesize=8,
        timeout=1
    )

    logging.info("Start pętli odczytu...")

    while True:
        try:
            # Connect Modbus
            if not modbus_client.connect():
                logging.warning("Brak połączenia z Modbus (USB). Ponawiam za 5s...")
                time.sleep(5)
                continue

            # Read Data
            readings = get_modbus_data(modbus_client)
            
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
                logging.info(f"Wysłano: {payload['leistung_W']}W | Dziś: {payload['tagesertrag_kWh']}kWh")
            
            else:
                logging.warning("Błąd odczytu danych z licznika.")

            modbus_client.close()
            time.sleep(5) 

        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error(f"Błąd w pętli głównej: {e}")
            time.sleep(10)

    mqtt_client.loop_stop()

if __name__ == "__main__":
    main()
