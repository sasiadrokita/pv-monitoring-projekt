# PV-Monitoring System
**Betriebliche Dokumentation**

**Abschlussprüfung Sommer 2026**
**Fachinformatiker für Digitale Vernetzung (AP T2)**

**Prüfling:** Mateusz Nowak
**Identnummer:** 141-13256

---

[TOC]

---

# 2. Betriebliche Dokumentation

## 2.1 Systemübersicht

### 2.1.1 Hardware-Aufbau
Das System basiert auf einem **Raspberry Pi 4 Model B (4GB RAM)**, der im zentralen Serverschrank (Rack 2) verbaut ist.
Die Datenerfassung erfolgt über einen USB-zu-RS485-Adapter (FTDI-Chipsatz), der mit dem Modbus-Zähler **Eastron SDM120** verbunden ist.

**Anschlussbelegung:**
*   **A+ (Zähler):** Pin 1
*   **B- (Zähler):** Pin 2
*   **GND (Optional):** Pin 3 (bei geschirmter Leitung empfohlen)

### 2.1.2 Netzwerk-Konfiguration
Das System befindet sich im **VLAN 20 (IoT)**.

| Parameter | Wert |
| :--- | :--- |
| **Hostname** | `pv-monitor` |
| **IP-Adresse** | `192.168.178.50` (Statisch) |
| **Subnetmask** | `255.255.255.0` (/24) |
| **Gateway** | `192.168.178.1` (UniFi Dream Machine) |
| **DNS** | `192.168.178.1` (oder `8.8.8.8`) |
| **Offene Ports** | `22` (SSH - Intern), `443` (Cloudflare Tunnel - Outbound) |

## 2.2 Software-Konfiguration

Das System wird vollständig über **Docker Compose** verwaltet. Alle Dienste starten automatisch nach einem Reboot (`restart: always`).

### 2.2.1 Verwendete Container
1.  **mosquitto:** MQTT-Broker für den Nachrichtenaustausch.
2.  **pv-collector:** Python-Skript zur Modbus-Auslesung (Custom Image).
3.  **telegraf:** Sammelt Daten von MQTT und schreibt in InfluxDB.
4.  **influxdb:** Zeitreihen-Datenbank zur Speicherung.
5.  **grafana:** Visualisierung der Daten.

### 2.2.2 Wichtige Konfigurationsdateien
Die Konfiguration liegt unter `/home/mateusz/Documents/Workspace/PV-monitoring/`.

**Auszug `docker-compose.yml`:**
```yaml
services:
  influxdb:
    image: influxdb:2.7
    ports:
      - "8086:8086"
    volumes:
      - influxdb_data:/var/lib/influxdb2
  
  grafana:
    image: grafana/grafana:11.0.0
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=secret
```

### 2.2.3 Datensicherung (Backup)
Ein automatisches Backup erfolgt täglich um 03:00 Uhr via Cronjob.

**Backup-Strategie:**
*   **Ziel:** Google Drive (via `rclone`).
*   **Umfang:** InfluxDB-Dump + Grafana-Datenbank (`grafana.db`).
*   **Skript:** `/usr/local/bin/backup_pv.sh`.

**Restore-Anleitung:**
1.  Container stoppen: `docker compose down`
2.  Datenbank wiederherstellen: `influx restore /backup/dump`
3.  Container starten: `docker compose up -d`

## 2.3 Administration

### 2.3.1 Benutzerverwaltung
| Benutzer | Rolle | Zugriff |
| :--- | :--- | :--- |
| **admin** | Administrator | Vollzugriff (SSH, Grafana, Portainer) |
| **viewer** | Benutzer | Nur Lesezugriff auf Dashboards |

### 2.3.2 Updates
Das System sollte monatlich aktualisiert werden:
1.  OS-Updates: `sudo apt update && sudo apt upgrade -y`
2.  Docker-Images: `docker compose pull && docker compose up -d`

## 2.4 Fehlerbehebung

| Fehlerbild | Mögliche Ursache | Maßnahme |
| :--- | :--- | :--- |
| **Keine Daten im Dashboard** | Modbus-Verbindung unterbrochen | Kabel prüfen, `docker logs pv-collector` eingeben |
| **Zähler unerreicht** | Falsche Baudrate/Adresse | Am Zähler prüfen (Soll: 9600, ID: 001) |
| **System nicht erreichbar** | Cloudflare Tunnel offline | Internetverbindung prüfen, `systemctl status cloudflared` |
