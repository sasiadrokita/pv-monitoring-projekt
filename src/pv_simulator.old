import time
import json
import random
import paho.mqtt.client as mqtt
import os

# --- MQTT Konfiguration ---
# Die Konfiguration wird aus Umgebungsvariablen gelesen, um Flexibilität zu gewährleisten.
# Standardwerte werden verwendet, falls die Variablen nicht gesetzt sind.
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "mosquitto")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "pv/anlage/data")
SIMULATION_INTERVAL = int(os.getenv("SIMULATION_INTERVAL", 5)) # Intervall in Sekunden

def generate_pv_data():
    """
    Generiert simulierte Leistungsdaten einer PV-Anlage.
    Die Leistung wird anhand einer einfachen Sinus-ähnlichen Kurve modelliert, 
    um den Tagesverlauf der Sonne nachzubilden.
    """
    current_hour = time.localtime().tm_hour
    
    # Die Anlage produziert nur während der Tageslichtstunden (z.B. zwischen 6 und 20 Uhr)
    if 6 <= current_hour < 20:
        # Berechnung einer Basisleistung, die zur Mittagszeit am höchsten ist
        # Die Formel simuliert eine Parabel, die um 13:00 Uhr ihr Maximum erreicht
        hours_from_peak = abs(13 - current_hour)
        # Maximalleistung von 3000 W wird angenommen
        base_power = 3000 * (1 - (hours_from_peak / 7)**2) 
        
        # Hinzufügen einer zufälligen Schwankung (z.B. durch Wolken)
        power = base_power + random.uniform(-100, 100)
        power = max(0, power) # Leistung kann nicht negativ sein
    else:
        # Nachts wird keine Energie produziert
        power = 0.0

    # Andere Werte werden basierend auf der Leistung berechnet
    voltage = 230.0 + random.uniform(-5, 5) if power > 0 else 0.0
    current = power / voltage if voltage > 0 else 0.0
    
    # Der Tagesertrag wird hier nur simpel simuliert. In einem echten System würde dieser Wert akkumuliert.
    daily_yield = round((time.time() / 10000) % 100, 2)

    # Erstellen des Daten-Dictionarys
    data = {
        "spannung_V": round(voltage, 2),
        "strom_A": round(current, 2),
        "leistung_W": round(power, 2),
        "tagesertrag_kWh": daily_yield,
        "timestamp": int(time.time()) # UNIX-Timestamp
    }
    return data

def on_connect(client, userdata, flags, rc):
    """Callback, der beim Verbindungsaufbau mit dem MQTT-Broker aufgerufen wird."""
    if rc == 0:
        print("Erfolgreich mit dem MQTT-Broker verbunden.")
    else:
        print(f"Verbindung fehlgeschlagen, Rückgabecode: {rc}")

def main():
    """Hauptfunktion des Simulators."""
    client = mqtt.Client(client_id="pv_simulator_client")
    client.on_connect = on_connect

    print("Versuche, eine Verbindung zum MQTT-Broker herzustellen...")
    
    # Die Verbindung wird in einer Schleife versucht, um robust gegenüber Startverzögerungen des Brokers zu sein
    while True:
        try:
            client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
            break # Schleife verlassen bei erfolgreicher Verbindung
        except ConnectionRefusedError:
            print("Verbindung verweigert. Broker ist möglicherweise noch nicht bereit. Nächster Versuch in 5 Sekunden...")
            time.sleep(5)
        except OSError:
            print(f"Broker unter {MQTT_BROKER_HOST} nicht erreichbar. Nächster Versuch in 5 Sekunden...")
            time.sleep(5)

    client.loop_start() # Startet den Netzwerk-Thread für die MQTT-Kommunikation

    try:
        while True:
            # Daten generieren und als JSON-String aufbereiten
            pv_data = generate_pv_data()
            payload = json.dumps(pv_data)
            
            # Nachricht an das definierte Topic senden
            result = client.publish(MQTT_TOPIC, payload)
            
            # Überprüfen, ob die Nachricht erfolgreich gesendet wurde
            status = result[0]
            if status == 0:
                print(f"Nachricht an Topic '{MQTT_TOPIC}' gesendet: {payload}")
            else:
                print(f"Fehler beim Senden der Nachricht an Topic '{MQTT_TOPIC}'")
            
            # Warten für das definierte Intervall
            time.sleep(SIMULATION_INTERVAL)
            
    except KeyboardInterrupt:
        print("Simulator wird beendet.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Verbindung zum MQTT-Broker wurde getrennt.")

if __name__ == "__main__":
    main()
