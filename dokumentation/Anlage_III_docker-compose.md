# Anlage III: docker-compose.yml Konfigurationsdatei

## Beschreibung
Die `docker-compose.yml` definiert die gesamte Systemarchitektur des PV-Monitoring-Systems. Sie orchestriert die Container für den MQTT-Broker, die Datenbank, die Visualisierung und den Datensammler.

## Konfiguration mit Kommentaren

### 1. Version und Netzwerke
Das System verwendet Docker Compose Version 3.8 und definiert ein internes Brückennetzwerk `pv-net` für die Kommunikation zwischen den Containern.

```yaml
version: '3.8'

services:
  # --- 1. KOMMUNIKATION ---
  # Mosquitto MQTT Broker: Vermittelt Nachrichten zwischen Collector und Telegraf
  mosquitto:
    image: eclipse-mosquitto:2.0
    container_name: mosquitto
    restart: unless-stopped
    ports:
      - "1883:1883"  # MQTT Port (Intern & Extern erreichbar)
    volumes:
      - ./docker/mosquitto/config:/mosquitto/config
      - ./docker/mosquitto/data:/mosquitto/data
      - ./docker/mosquitto/log:/mosquitto/log
    networks:
      - pv-net

  # --- 2. DATENBANK ---
  # InfluxDB: Speichert Zeitreihendaten (Time-Series Database)
  influxdb:
    image: influxdb:2.7
    container_name: influxdb
    restart: unless-stopped
    ports:
      - "8086:8086"  # Web-Interface & API
    volumes:
      - ./docker/influxdb/data:/var/lib/influxdb2
      - ./docker/influxdb/config:/etc/influxdb2
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_PASSWORD=adminadmin
      - DOCKER_INFLUXDB_INIT_ORG=eco-energy-solutions
      - DOCKER_INFLUXDB_INIT_BUCKET=pv_data
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-token
    networks:
      - pv-net

  # --- 3. VISUALISIERUNG ---
  # Grafana: Erstellt Dashboards aus InfluxDB-Daten
  grafana:
    image: grafana/grafana-oss:11.0.0
    container_name: grafana
    restart: unless-stopped
    ports:
      - "3000:3000"  # Web-Interface
    volumes:
      - ./docker/grafana/data:/var/lib/grafana
    depends_on:
      - influxdb
    environment:
      - GF_INSTALL_PLUGINS=grafana-clock-panel
    networks:
      - pv-net

  # --- 4. DATENERFASSUNG (COLLECTOR) ---
  # PV-Collector: Liest Daten via Modbus und sendet an MQTT
  pv-collector:
    build:
      context: .
      dockerfile: src/Dockerfile
    container_name: pv-collector
    restart: unless-stopped
    depends_on:
      - mosquitto
    networks:
      - pv-net
    volumes:
      - ./docker/pv_collector_data:/app/data  # Für persistente Status-Daten
    devices:
      - "/dev/ttyUSB0:/dev/ttyUSB0"  # USB-RS485 Adapter durchreichen
    environment:
      - MQTT_BROKER_HOST=mosquitto
      - MQTT_TOPIC=pv/anlage/data
      - MODBUS_PORT=/dev/ttyUSB0
      - MODBUS_BAUDRATE=9600

  # --- 5. DATENVERARBEITUNG ---
  # Telegraf: Abonniert MQTT und schreibt in InfluxDB
  telegraf:
    image: telegraf:latest
    container_name: telegraf
    restart: unless-stopped
    volumes:
      - ./docker/telegraf/telegraf.conf:/etc/telegraf/telegraf.conf:ro
    depends_on:
      - mosquitto
      - influxdb
    networks:
      - pv-net

# --- NETZWERK DEFINITION ---
networks:
  pv-net:
    driver: bridge
```
