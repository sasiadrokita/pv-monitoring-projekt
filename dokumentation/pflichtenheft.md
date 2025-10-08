# Pflichtenheft: PV-Anlagen-Überwachung

**Projektname:** PV-Monitoring-System (EcoEnergy Solutions)

**Auftragnehmer:** [Twój Imię i Nazwisko]
**Datum:** [Aktuelles Datum]
**Version:** 1.0

---

## 1. Einführung

Dieses Pflichtenheft beschreibt die technische Umsetzung und das Lösungskonzept des PV-Monitoring-Systems. Es dient als verbindliche Spezifikation zur Erfüllung der im **Lastenheft (Version 1.0)** festgelegten Anforderungen des Auftraggebers.

## 2. Lösungskonzept und Systemarchitektur

Das System basiert auf einer modularen, containerisierten Architektur (Microservices-Ansatz), die auf einem Raspberry Pi 4 Model B betrieben wird. Die Hauptkommunikation innerhalb des Systems erfolgt über das MQTT-Protokoll.

### 2.1. Technologiestack

| Technologie | Funktion | Begründung |
| :--- | :--- | :--- |
| **Hardware** | Raspberry Pi 4 | Kosteneffiziente, energiesparende Edge-Computing-Plattform (NF2). |
| **Containerisierung** | Docker / Docker Compose | Einfache Bereitstellung, Wartbarkeit und Isolation der Dienste (NF4). |
| **Nachrichtenprotokoll** | MQTT (Mosquitto) | Leichtgewichtiges Pub/Sub-Protokoll, ideal für IoT-Umgebungen (F6). |
| **Datenbank** | InfluxDB 1.8 | Spezialisierte Time-Series-Datenbank für schnelle Speicherung und Abfrage zeitgestempelter Daten (F2). |
| **Visualisierung/Alarmierung** | Grafana | Umfangreiche Web-basierte Dashboards und konfigurierbare Alarmfunktionen (F3, F4, F5). |
| **Datenerfassung** | Python Skript (mit `pymodbus`) | Flexible Implementierung zur Steuerung der Modbus-Kommunikation. |

### 2.2. Architekturübersicht

Die Architektur besteht aus vier Hauptschichten:
1.  **Erfassung:** Python-Skript (Publisher) auf dem Host-System (Raspberry Pi).
2.  **Kommunikation:** MQTT-Broker (Mosquitto) im Container.
3.  **Speicherung:** Telegraf und InfluxDB im Container (TICK-Stack).
4.  **Präsentation:** Grafana im Container.

## 3. Detail-Spezifikation der Funktionalität

Die Umsetzung der funktionalen Anforderungen (F1-F7) erfolgt wie folgt:

| Lastenheft ID | Umsetzung (Wie wird es gemacht) |
| :--- | :--- |
| **F1** (Echtzeit-Erfassung) | Ein Python-Skript liest die Modbus-Register des PV-Wechselrichters über den seriellen RS-485-USB-Konverter alle 5 Sekunden aus und publiziert die Daten an das Topic `pv/data/realtime`. |
| **F2** (Datenarchivierung) | Der Telegraf-Container subskribiert das MQTT-Topic (`pv/data/realtime`) und schreibt die empfangenen JSON-Daten in die InfluxDB-Datenbank `pv_data`. Die Retentionsrichtlinie wird auf 90 Tage festgelegt. |
| **F3** (Visualisierung) | Grafana dient als Frontend und greift über die Datenquelle InfluxDB auf die archivierten und aktuellen Daten zu. Das Dashboard ist unter `http://[RPi-IP]:3000` erreichbar. |
| **F4** (Energiebilanz) | Im Grafana Dashboard werden dedizierte Panels mithilfe der Influx Query Language (InfluxQL) erstellt, um die kumulierte Tagesproduktion (`energy_today_kwh`) sowie die Wochen- und Monatsbilanz darzustellen. |
| **F5** (Alarmfunktion) | In Grafana wird ein Alerting-Kanal (z.B. E-Mail-Kontakt des Auftraggebers) konfiguriert. Die Alert-Regel prüft, ob der Wert `power_w` tagsüber (9:00 - 17:00 Uhr) für mehr als 10 Minuten unter 100W liegt. |
| **F6** (Technologieunabhängigkeit) | Die Verwendung von MQTT stellt sicher, dass weitere Sensoren (z.B. Temperatur) einfach durch das Publizieren auf neuen Topics integriert werden können, ohne die bestehende Architektur zu verändern. |
| **F7** (Protokollierung) | Das Python-Skript implementiert Logging für Verbindungsfehler (`pymodbus`) und MQTT-Veröffentlichungsprobleme. Die Logs aller Container sind über `docker logs <Containername>` abrufbar. |

## 4. Schnittstellenspezifikation

### 4.1. Hardware-Schnittstelle (Modbus RTU)

*   **Schnittstellenpfad:** `/dev/ttyUSB0` (wird vom Python-Skript verwendet).
*   **Kommunikationsparameter:** Baudrate 9600, 8 Datenbits, No Parity, 1 Stoppbit.
*   **Slave ID:** 1.
*   **Wichtige Register (Beispiele):**
    *   `Aktuelle Leistung (W)`: 40001
    *   `Tagesertrag (kWh)`: 40003
    *   `DC-Spannung (V)`: 40005

### 4.2. MQTT-Schnittstelle

*   **Broker:** `mosquitto:1883` (im Docker-Netzwerk).
*   **Authentifizierung:** Zunächst keine Authentifizierung (kann in zukünftigen Versionen implementiert werden).
*   **Haupt-Topic:** `pv/data/realtime`
*   **Datenformat (JSON):**
    ```json
    {
      "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
      "power_w": 2550.5,
      "energy_today_kwh": 12.3,
      "voltage_v": 240.2
    }
    ```

### 4.3. Datenbank-Schnittstelle (InfluxDB)

*   **Host:** `influxdb:8086`.
*   **Datenbankname:** `pv_data`.
*   **Measurement:** `pv_metrics` (Messwertreihe).
*   **Tags (Indizes):** `host` (z.B. RPi-1), `inverter_id`.
*   **Fields (Werte):** `power_w`, `energy_today_kwh`, `voltage_v`.

### 4.4. Externe Ports (Zugriff durch den Benutzer)

| Dienst | Protokoll | Port (Host/RPi) | Zweck |
| :--- | :--- | :--- | :--- |
| **Dashboard** (Grafana) | HTTP | 3000 | Web-Interface für den Kunden (F3). |

## 5. Implementierung und Wartung (Nicht-funktionale Anforderungen)

| Lastenheft ID | Umsetzung (Maßnahmen) |
| :--- | :--- |
| **NF1** (Performance) | Die Erfassungsrate von 5 Sekunden und die Verwendung von InfluxDB (TSDB) garantieren eine hohe Antwortzeit im Dashboard. |
| **NF4** (Wartbarkeit) | Alle Konfigurationsdateien (`docker-compose.yml`, `mosquitto.conf`, `telegraf.conf`, Grafana provisioning) werden versionskontrolliert im Git-Repository gespeichert. Updates erfolgen durch `docker-compose pull` und Neustart. |
| **NF6** (Sicherheit) | Der Zugriff auf das Grafana Dashboard wird durch einen Anmeldemechanismus geschützt (Standard `admin`/`adminpassword`). Der Zugriff erfolgt nur über das lokale Netzwerk. |
| **NF7** (Dokumentation) | Es wird eine detaillierte **Betriebliche Dokumentation** erstellt, die alle Installations-, Konfigurations- und Wartungsschritte (inklusive Troubleshooting) beinhaltet. |

## 6. Testkonzept

Das Testkonzept aus dem Lastenheft wird durch folgende Schritte untermauert:

1.  **Unit Tests (Python):** Überprüfung der Modbus-Lese- und MQTT-Publikationslogik im Python-Skript.
2.  **Integrations-Tests (Docker):** Sicherstellung, dass alle Container (Mosquitto, Telegraf, InfluxDB, Grafana) miteinander kommunizieren können und der Datenfluss T1-T3 funktioniert.
3.  **Akzeptanz-Tests (Grafana):** Validierung der Dashboard-Anzeige und der Alarmfunktionalität durch den Auftraggeber (T3, T4).

---