# Pflichtenheft: PV-Monitoring-System

**Projekt:** PV-Monitoring-System (EcoEnergy Solutions)  
**Version:** 1.0  
**Status:** Phase 1 - Implementierung & Simulation  
**Datum:** [Aktuelles Datum]

---

## 1. Zielbestimmung
Das Ziel des Projekts ist die Implementierung eines skalierbaren, containerbasierten Monitoring-Systems für Photovoltaikanlagen. In der ersten Phase wird die Datenquelle durch einen Simulator ersetzt, um die Infrastruktur (Datenbank, Dashboards, Remote-Zugriff) zu validieren. Das System ist so konzipiert, dass der Wechsel auf echte Hardware (Modbus-Auslesung) nur den Austausch eines einzigen Software-Moduls erfordert.

## 2. Systemarchitektur & Technologie-Stack

Das System basiert auf einer Microservices-Architektur, die mittels Docker und Docker Compose orchestriert wird.

### 2.1 Hardware-Basis
*   **Server:** Raspberry Pi 4 (4GB RAM empfohlen)
*   **Speicher:** microSD (min. 32GB, Class A1/A2)
*   **Betriebssystem:** Raspberry Pi OS Lite (64-bit)

### 2.2 Software-Komponenten (Container)
1.  **PV-Simulator (Custom Python App):**
    *   Generiert realistische Leistungsdaten (Tagesverlauf, Wettereinflüsse).
    *   Implementiert Persistenz (speichert Zählerstand `tagesertrag_kWh` bei Neustart).
    *   Schnittstelle: MQTT Publisher.
2.  **Mosquitto (MQTT Broker):**
    *   Zentraler Nachrichtenbus.
    *   Version: 2.0
    *   Port: 1883
3.  **Telegraf (Data Collector):**
    *   Fungiert als "Übersetzer" zwischen MQTT und Datenbank.
    *   Abonniert MQTT-Topics und schreibt Metriken in InfluxDB v2.
4.  **InfluxDB v2 (Time-Series Database):**
    *   Speichert hochfrequente Messwerte.
    *   Authentifizierung via Tokens.
    *   Organisation: `eco-energy-solutions`, Bucket: `pv_data`.
5.  **Grafana (Visualisierung):**
    *   Dashboard-Oberfläche.
    *   Datenquelle: InfluxDB (Flux Query Language).
    *   Port: 3000.

### 2.3 Remote-Zugriff (Edge-Layer)
*   **Technologie:** Cloudflare Tunnel (Cloudflared).
*   **Implementierung:** Systemd Service (Native auf dem Host, außerhalb von Docker).
*   **Sicherheit:** Verschlüsselter Tunnel ohne Portfreigabe am Router.
*   **Feature:** Automatischer Start bei Boot, URL-Anzeige via SSH-Login-Skript.

## 3. Funktionale Spezifikation (Umsetzung)

### 3.1 Datenerfassung & Datenmodell
Das System verarbeitet Daten im JSON-Format.
**Topic:** `pv/anlage/data`
**Intervall:** 5-10 Sekunden (konfigurierbar via `SIMULATION_INTERVAL`).

**Datenstruktur (JSON-Payload):**
```json
{
  "spannung_V": 230.5,      // Float: Aktuelle Spannung
  "strom_A": 10.2,          // Float: Aktueller Strom
  "leistung_W": 2350.0,     // Float: Aktuelle Leistung
  "tagesertrag_kWh": 12.5,  // Float: Kumulierter Tagesertrag (persistent)
  "timestamp": 1715608000   // Int: Unix Timestamp
}
### 3.2 Datenfluss
1.  `pv-simulator` berechnet Werte und publiziert JSON an Mosquitto.
2.  `telegraf` empfängt JSON, parst Felder und sendet sie an InfluxDB.
3.  `influxdb` speichert die Werte mit Zeitstempel.
4.  `grafana` fragt InfluxDB ab und visualisiert die Kurven.

### 3.3 Persistenz & Ausfallsicherheit
*   **Container:** Alle Container nutzen `restart: unless-stopped`.
*   **Daten:** InfluxDB und Grafana nutzen Docker Volumes (`./docker/...`), um Daten bei Container-Neustarts zu behalten.
*   **Simulation:** Der Simulator speichert den Zählerstand in `simulation_state.json`, um Datenverlust bei Neustarts zu verhindern.

## 4. Benutzeroberfläche (Dashboard)
Das Grafana-Dashboard beinhaltet:
*   **Live-Anzeige:** Aktuelle Leistung (W) als Gauge.
*   **Historie:** Graph für Leistung (W) über den Tag.
*   **Ertrag:** Balkendiagramm oder Text für Tagesertrag (kWh).
*   **Technik:** Status-Anzeigen für Datenbank und Broker.

## 5. Erweiterbarkeit (Phase 2)
Das System ist "Hardware-Ready". Um echte Wechselrichter anzubinden, muss lediglich der Container `pv-simulator` durch einen `modbus-reader` Container ersetzt werden, der:
1.  Die gleiche JSON-Struktur an das gleiche MQTT-Topic sendet.
2.  Die Hardware-Schnittstelle (`/dev/ttyUSB0`) nutzt.
Die restliche Infrastruktur (Telegraf, InfluxDB, Grafana, Cloudflare) bleibt unverändert.

## 6. Abnahmekriterien (Erfüllungsgrad)
*   [x] Docker-Environment läuft stabil.
*   [x] Datenfluss Simulator -> Dashboard funktioniert.
*   [x] Remote-Zugriff via Cloudflare ist eingerichtet.
*   [x] Neustart-Resistenz (Persistenz) ist gewährleistet.
