# PV-Monitoring System
**Konzeption und Realisierung eines Monitoringsystems für PV-Bestandsanlagen auf Basis von IoT-Technologien**

**Abschlussprüfung Sommer 2026**
**Ausbildungsberuf:** Fachinformatiker für Digitale Vernetzung (AP T2)

**Prüfling:**
Mateusz Nowak
Identnummer: 141-13256
E-Mail: mateusz.nowak.zabrze@gmail.com
Tel.: +49 171 1110639

**Ausbildungsbetrieb:**
Berufsförderungswerk des DRK Birkenfeld
Walter-Bleicker-Platz
55765 Birkenfeld

**Projektbetreuer:**
Heiko Grützner
E-Mail: h.gruetzner@e-s-b.org
Tel.: +49 6782 18-1422

---

[TOC]

---

# 2. Betriebliche Dokumentation

Die vorliegende betriebliche Dokumentation beschreibt die technische Konfiguration des im Projektbericht behandelten PV-Monitoringsystems gemäß den Vorgaben. Sie dient Administratoren als Nachschlagewerk für den laufenden Betrieb, die Wartung und die Fehlerbehebung. Gemäß den Anforderungen wird auf eine ausführliche Systembedienungs-Anleitung verzichtet und stattdessen der Fokus auf die konkreten Konfigurationsparameter gelegt.

## 2.1 Systeminfrastruktur und Hardware

Die Hardware ist im zentralen Serverschrank (Rack 2, HE 14) platziert und über eine USV abgesichert. Der Zähler befindet sich im Technikraum.

| Komponente | Spezifikation / Parameter | Konfiguration / Einsatz |
| :--- | :--- | :--- |
| **Edge-Device** | Raspberry Pi 4 Model B | 4 GB RAM, 64-bit Architektur |
| **Speichermedium** | SanDisk Extreme microSDXC | 32 GB, A2, Class 10 (für OS und DB) |
| **Energiezähler** | Eastron SDM120-Modbus | AC-Messung, Modbus-ID: `001`, Baudrate: `9600` |
| **Schnittstelle** | FTDI USB-RS485 Adapter | `/dev/ttyUSB0`, 8N1, Half-Duplex |

**Pin-Belegung (RS485 - CAT7 Leitungsverbindung):**
*   **A+ (Zähler):** Pin 1
*   **B- (Zähler):** Pin 2
*   **GND (Zähler):** Pin 3 (Schirmung aufgelegt zur Reduzierung von Störeinflüssen)

## 2.2 Eingesetzte Betriebssysteme und Software

Das System ist modular mittels Container-Technologie aufgebaut. Alle Container starten durch die Policy `restart: always` selbständig.

| Software | Version | Verwendungszweck |
| :--- | :--- | :--- |
| **Betriebssystem** | Raspberry Pi OS Lite | Host-System (64-bit), minimaler Footprint |
| **Container-Engine**| Docker v24.x | Orchestrierung und Kapselung der Dienste |
| **MQTT-Broker** | mosquitto:latest | Interner Message Bus (`pv/anlage/data`) |
| **Datenerfassung** | Custom Python (pv_collector) | Modbus RTU nach MQTT Schnittstelle |
| **Data-Connector** | telegraf:latest | Subscription auf MQTT, Schreiben in InfluxDB |
| **Datenbank** | InfluxDB v2.7 | Time-Series Langzeitspeicherung |
| **Visualisierung** | Grafana v11.0 | Web-Dashboard und Alerting |
| **Fernzugriff** | cloudflared | Sicherer HTTPS-Tunnel ohne Portfreigabe |

## 2.3 Netzwerk und IP-Adressen

Das IoT-System ist aus Sicherheitsgründen in einem separaten virtuellen LAN (VLAN) isoliert.

| Parameter | Wert / Konfiguration |
| :--- | :--- |
| **Netzwerksegment** | VLAN 20 (IoT) |
| **Hostname** | `pv-monitor` |
| **IP-Adresse (IPv4)**| `192.168.178.50` (Statisch via DHCP-Reservierung im Gateway) |
| **Subnetzmaske** | `255.255.255.0` (/24) |
| **Standard-Gateway**| `192.168.178.1` (UniFi Dream Machine) |
| **DNS-Server** | `192.168.178.1` |
| **Interne Ports** | `22` (SSH TCP), `1883` (MQTT TCP), `3000` (Grafana TCP), `8086` (InfluxDB TCP) |

### 2.3.1 Firewallregeln (Gateway)
Die Kommunikation wird durch die zentrale Firewall restriktiv gesteuert (Zero-Trust-Ansatz für IoT):
*   **Ausgehend (Outbound):** Nur HTTPS (Port `443`) zu Cloudflare (für den Tunnel und Updates) sowie NTP (Port `123`) für die Zeitsynchronisierung erlaubt.
*   **Eingehend (Inbound):** Sämtlicher eingehender Traffic aus externen Netzen in das VLAN 20 ist blockiert (`DROP`). Der Zugriff von extern erfolgt ausschließlich reverse über den etablierten Cloudflare-Tunnel.
*   **Intern:** Zugriff via SSH (Port `22`) nur aus dem Administrations-VLAN erlaubt.

## 2.4 Zentrale Konfigurationsdateien

Das gesamte System wird deklarativ über Docker Compose konfiguriert. Der Projektpfad lautet `/home/mateusz/Documents/Workspace/PV-monitoring/`.

### 2.4.1 Container-Orchestrierung (`docker-compose.yml`)
Auszug der wesentlichen Parameter für Netzwerk und Persistenz:
```yaml
networks:
  pv_net:
    driver: bridge # Internes Bridge-Netzwerk für Container-Kommunikation

services:
  influxdb:
    image: influxdb:2.7
    container_name: influxdb
    restart: always
    volumes:
      - ./docker/influxdb/data:/var/lib/influxdb2
      - ./docker/influxdb/config:/etc/influxdb2
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_ORG=home
      - DOCKER_INFLUXDB_INIT_BUCKET=pv_data
    networks:
      - pv_net

  grafana:
    image: grafana/grafana:11.0.0
    container_name: grafana
    restart: always
    ports:
      - "3000:3000"
    volumes:
      - ./docker/grafana/data:/var/lib/grafana
    environment:
      - TZ=Europe/Berlin
    networks:
      - pv_net
```

### 2.4.2 Datenerfassung (Python `pv_collector`)
Wichtige Konfigurationsparameter für die serielle Datenkommunikation (Auszug):
```python
# Modbus RTU Konfiguration
MODBUS_PORT = '/dev/ttyUSB0'
MODBUS_BAUDRATE = 9600
MODBUS_BYTESIZE = 8
MODBUS_PARITY = 'N' # None
MODBUS_STOPBITS = 1
MODBUS_TIMEOUT = 2.0 # Erhöht für Stabilität auf langen Strecken
UNIT_ID = 1

# MQTT Konfiguration
MQTT_BROKER = 'mosquitto' # Docker Service Name (DNS Resolve)
MQTT_PORT = 1883
MQTT_TOPIC = 'pv/anlage/data'
```

## 2.5 Benutzer, Gruppen und Rechte

### 2.5.1 Betriebssystemsebene
*   **Benutzer:** `mateusz` (UID 1000)
*   **Gruppen:** `sudo`, `docker`, `dialout` (Zwingend für den physikalischen Zugriff auf `/dev/ttyUSB0`)
*   **Rechtsschema:** Authentifizierung erfolgt sicherheitsbedingt primär über Public-Key-Verfahren (SSH-Keys).

### 2.5.2 Applikationsebene (Grafana & InfluxDB)
| Applikation | Benutzer / Token | Rolle / Rechte |
| :--- | :--- | :--- |
| **InfluxDB** | `grafana_reader` | *Read-Only* Token speziell für das Dashboard. Beschränkt auf das Bucket `pv_data`. |
| **InfluxDB** | `telegraf_writer`| *Write-Only* Token. Berechtigt ausschließlich zum Schreiben in das Bucket `pv_data`. |
| **Grafana** | `admin` | *Server Admin*. Vollständige Konfigurationsrechte an Dashboards und dem System. |
| **Grafana** | `viewer` | *Viewer*. Lesezugriff zur reinen Betrachtung der Betriebsdaten ohne Änderungsrechte. |
