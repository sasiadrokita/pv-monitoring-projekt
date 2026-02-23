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

# 1. Projektbericht

## 1.1 Beschreibung des Auftrages

### 1.1.1 Ausgangslage
Die **EcoEnergy Solutions GmbH** betreibt eine ältere Photovoltaikanlage, deren Herzstück ein Wechselrichter älterer Bauart ist. Dieser Wechselrichter verfügt über **keine digitale Schnittstelle** (kein LAN/WLAN) zur direkten Datenausgabe, sondern lediglich über ein LC-Display.

Die **aktuelle Situation** weist folgende Defizite auf:
*   **Manuelle Datenerfassung:** Leistungsdaten (aktuelle Leistung, Tagesertrag) müssen physisch vor Ort abgelesen werden.
*   **Fehlende Historie:** Es erfolgt keine Speicherung historischer Daten. Trends, saisonale Schwankungen oder Leistungsabfälle können nicht analysiert werden.
*   **Keine Fehlererkennung:** Störungen (z.B. Ausfall bei Sonnenschein) fallen oft erst nach Tagen durch Zufall auf, was zu erheblichen Ertragsverlusten führt.
*   **Proprietäre Lösungen unwirtschaftlich:** Eine direkte Aufrüstung des Wechselrichters oder der Kauf proprietärer Kommunikationsmodule ist aufgrund fehlender Ersatzteile und hoher Kosten nicht wirtschaftlich vertretbar.

### 1.1.2 Aufgabenstellung
Ziel des Projektes ist die Konzeption und Realisierung eines **modernen, kostengünstigen Monitoringsystems auf IoT-Basis**. Das System soll die Altanlage "smart" machen ("Retrofitting").

Kernanforderungen:
1.  **Hardware:** Einsatz eines Einplatinencomputers (**Raspberry Pi 4**) als Edge-Device und eines Modbus-Energiezählers (**Eastron SDM120**) zur präzisen Messung am AC-Ausgang.
2.  **Software-Architektur:** Modularer Aufbau mittels **Docker-Containern**.
3.  **Datenerfassung:** Python-Skript (`pv_collector`) für Modbus RTU -> MQTT.
4.  **Speicherung:** Langzeitarchivierung in **InfluxDB**.
5.  **Visualisierung:** Web-Dashboard mit **Grafana**.
6.  **Fernzugriff:** Sicherer Zugriff via **Cloudflare Tunnel**.

### 1.1.3 Projektumfeld
Das Projekt wird innerhalb der **IT-Infrastruktur** der EcoEnergy Solutions GmbH realisiert.

**Physische Umgebung:**
*   **Serverraum:** Der Raspberry Pi wird im zentralen Serverschrank (Rack 2, HE 14) platziert (USV-gesichert).
*   **Technikraum:** Wechselrichter und SDM120-Zähler befinden sich im Untergeschoss.
*   **Verkabelung:** Bestehende CAT7-Leitung wird für die RS485-Kommunikation genutzt.

**Netzwerkumgebung:**
*   **VLAN 20 (IoT):** Isoliertes Netzwerksegment für den Raspberry Pi.
*   **IP:** Statisch `192.168.178.50`.
*   **Firewall:** Blockiert eingehenden Traffic; Raspberry Pi nutzt nur ausgehende Verbindungen (Cloudflare).

**Technische Ressourcen:**
*   **Hardware:** Raspberry Pi 4 (4GB), SanDisk Extreme 32GB SD, Eastron SDM120-Modbus, FTDI USB-RS485 Adapter.
*   **Software:** Raspberry Pi OS Lite (64-bit), Docker v24, InfluxDB v2.7, Grafana v11.

### 1.1.4 Prozessschnittstellen

**Auftraggeber & Ansprechpartner:**
EcoEnergy Solutions GmbH
(Beispielhafter Ansprechpartner: Herr Klaus Meyer, Technischer Leiter)
Musterstraße 1, 12345 Musterstadt

**Auftragnehmer & Ansprechpartner:**
Mateusz Nowak (Auszubildender Fachinformatiker für Digitale Vernetzung)
Berufsförderungswerk des DRK Birkenfeld
Walter-Bleicker-Platz, 55765 Birkenfeld
Tel.: +49 171 1110639
E-Mail: mateusz.nowak.zabrze@gmail.com
(Projektbetreuer: Heiko Grützner)

**Ggf. weitere Beteiligte:**
*   Lokaler IT-Administrator / Netzwerkverantwortlicher der EcoEnergy Solutions GmbH (für Netzwerkanpassungen, VLAN, Firewall-Freigaben gem. Vorgabe)
*   Haustechnik / Facility Management (für Zutritt zum Serverraum und Technikraum)


### 1.1.5 Notwendige Änderungen gegenüber dem Projektantrag
Es ergaben sich im Projektverlauf keine wesentlichen inhaltlichen oder zeitlichen Abweichungen vom genehmigten Projektantrag.

## 1.2 Beschreibung der Prozessschritte und der erzielten Ergebnisse

### 1.2.1 Zeitaufwand für die Projektschritte (Soll-Ist-Vergleich)

Die folgende Tabelle stellt den geplanten Zeitansatz (gemäß Projektantrag) dem tatsächlichen Zeitaufwand gegenüber.

| Nr. | Phase / Tätigkeit | Zeitansatz (Soll) | Zeitaufwand (Ist) |
| :--- | :--- | :--- | :--- |
| **1** | **Planungsphase** | **8,0 Std.** | **8,0 Std.** |
| 1.1 | Ist-Analyse und Definition der fachlichen Anforderungen | 1,5 Std. | 1,5 Std. |
| 1.2 | Marktanalyse und Evaluierung geeigneter Software-Komponenten | 1,5 Std. | 1,5 Std. |
| 1.3 | Auswahl der Hardware-Komponenten und Peripherie | 1,0 Std. | 1,0 Std. |
| 1.4 | Planung der Netzwerkarchitektur und des Sicherheitskonzepts | 1,5 Std. | 1,5 Std. |
| 1.5 | Kosten-Nutzen-Analyse des Projekts | 1,5 Std. | 1,5 Std. |
| 1.6 | Erstellung des Projektablaufplans | 1,0 Std. | 1,0 Std. |
| **2** | **Entwurfsphase** | **8,0 Std.** | **8,0 Std.** |
| 2.1 | Entwurf des Datenmodells (JSON-Struktur und Datenbank-Schema) | 1,5 Std. | 1,5 Std. |
| 2.2 | Konzeption der Schnittstellen (MQTT-Topics und Telegraf-Mapping) | 1,5 Std. | 1,5 Std. |
| 2.3 | Planung der Container-Orchestrierung (Docker-Compose-Entwurf) | 2,0 Std. | 2,0 Std. |
| 2.4 | Konzeption der Speicher-Strategie | 1,5 Std. | 1,5 Std. |
| 2.5 | Entwurf des Dashboard-Layouts | 1,5 Std. | 1,5 Std. |
| **3** | **Implementierungsphase** | **12,0 Std.** | **12,0 Std.** |
| 3.1 | Installation und Härtung des Betriebssystems (Raspberry Pi OS) | 1,5 Std. | 1,5 Std. |
| 3.2 | Einrichtung der Container-Laufzeitumgebung | 1,0 Std. | **0,5 Std.** |
| 3.3 | Entwicklung des Datenerfassungs-Skripts (Python/MQTT-Client) | 2,0 Std. | **2,5 Std.** |
| 3.4 | Konfiguration des MQTT-Brokers und der Datenbank (InfluxDB) | 1,5 Std. | 1,5 Std. |
| 3.5 | Einrichtung des Data-Collectors (Telegraf) zur Verknüpfung der Dienste | 1,5 Std. | 1,5 Std. |
| 3.6 | Erstellung und Konfiguration der Grafana-Dashboards | 2,0 Std. | 2,0 Std. |
| 3.7 | Implementierung des sicheren Fernzugriffs (Cloudflare Tunnel) | 1,5 Std. | 1,5 Std. |
| 3.8 | Einrichtung der automatischen Alarmierung (Alerting) | 1,0 Std. | 1,0 Std. |
| **4** | **Test- und Qualitätssicherungsphase** | **5,0 Std.** | **5,0 Std.** |
| 4.1 | Funktionstest der lokalen Datenerfassung und -speicherung | 1,5 Std. | 1,5 Std. |
| 4.2 | Überprüfung des externen Zugriffs und der Sicherheitseinstellungen | 1,0 Std. | 1,0 Std. |
| 4.3 | Validierung der Alarmierung bei simulierten Ausfällen | 1,0 Std. | 1,0 Std. |
| 4.4 | Soll-Ist-Vergleich und abschließendes Feintuning | 1,5 Std. | 1,5 Std. |
| **5** | **Dokumentation und Übergabe** | **7,0 Std.** | **7,0 Std.** |
| 5.1 | Erstellung der Projektdokumentation | 6,0 Std. | 6,0 Std. |
| 5.2 | Präsentation und Übergabe an den Auftraggeber | 1,0 Std. | 1,0 Std. |
| | **Gesamtzeit** | **40,0 Std.** | **40,0 Std.** |

*Kommentar zur Abweichung:* Mehraufwand bei der Python-Entwicklung (+0,5h durch Modbus-Timing-Probleme) wurde durch ein effizienteres Docker-Setup (-0,5h dank Nutzung bestehender Templates) ausgeglichen.

### 1.2.2 Beschreibung der Vorgehensweise (Methodik)
Für die Durchführung des Projektes wurde das **Wasserfallmodell** gewählt.
Begründung: Die Anforderungen waren durch den Projektantrag und das Lastenheft bereits zu Projektbeginn fest definiert ("Monitoringsystem mit spezifischem Hardware-Setup"). Ein agiles Vorgehen (z.B. Scrum) wäre aufgrund der geringen Teamgröße (Einzelprojekt) und der kurzen Laufzeit (40 Stunden) nicht zielführend gewesen.

Der Projektablauf gliederte sich in fünf definierte Phasen:

**Phase 1: Analyse & Planung**
Marktanalyse und "Make-or-Buy"-Entscheidung. Proprietäre Lösungen (>500€) wurden verworfen. Open-Source-Ansatz gewählt.

**Phase 2: Entwurf**
Festlegung der Architektur: Sensor -> Modbus -> Python -> MQTT -> Telegraf -> InfluxDB -> Grafana (TIG-Stack).

**Phase 3: Implementierung**
Realisierung in logischer Reihenfolge: Hardware-Aufbau -> OS-Installation -> Software-Entwicklung -> Integration.

**Phase 4: Test & Qualitätssicherung**
Modultests und Integrationstests. Validierung der Messwerte gegen Referenzmessgerät (Fluke Multimeter).

**Phase 5: Abschluss**
Dokumentation und Einweisung des Auftraggebers.

### 1.2.3 Aufgetretene Probleme und Lösungen

1.  **Modbus-Stabilität:**
    *   *Problem:* Timeouts bei langen Leitungen.
    *   *Lösung:* Erhöhung des Timeouts im Python-Skript (1s -> 2s) und Retry-Logik.

2.  **Zeitzonen:**
    *   *Problem:* UTC-Zeitstempel in Grafana verwirrend.
    *   *Lösung:* `TZ=Europe/Berlin` in Docker-Containern gesetzt.

3.  **Netzwerk:**
    *   *Problem:* Container fanden Broker nicht über `localhost`.
    *   *Lösung:* Nutzung von Docker Service-Namen (`mosquitto`) im internen Bridge-Netzwerk.

### 1.2.4 Evaluierung der Entscheidungen

#### 1.2.4.1 Hardware (Controller)
| Option | Raspberry Pi 4 (Gewählt) | ESP32 | Intel NUC |
| :--- | :--- | :--- | :--- |
| **Kosten** | ~60€ | ~10€ | >300€ |
| **Leistung** | Hoch (DB & GUI möglich) | Gering (Nur Erfassung) | Sehr hoch |
| **OS** | Linux (Docker) | MicroPython | Linux/Windows |
| **Fazit** | **Optimal** | Zu schwach für InfluxDB | Zu teuer |

#### 1.2.4.2 Datenbank
| Option | InfluxDB (Gewählt) | SQL (MySQL) | Prometheus |
| :--- | :--- | :--- | :--- |
| **Typ** | Time-Series | Relational | Time-Series (Pull) |
| **IoT** | Sehr gut (Push) | Mäßig | Gut (Pull) |
| **Fazit** | **Optimal für IoT-Sensordaten** | Unnötiger Overhead | Setup komplexer |

### 1.2.5 Darstellung der Ergebnisse
Das System läuft stabil und liefert kontinuierlich Daten.

#### 1.2.5.1 Dashboard
*(Platzhalter für Screenshots)*
*   [SCREENSHOT: Grafana Dashboard - Hauptansicht]
*   [SCREENSHOT: Telegram Alert]

### 1.2.6 Qualitätssicherung (Testprotokoll)

| ID | Testfall | Erwartung | Ergebnis | Status |
| :--- | :--- | :--- | :--- | :--- |
| T01 | Hardware-Erkennung | USB-Adapter `/dev/ttyUSB0` vorhanden | `ls -l` zeigt Device | **OK** |
| T02 | Modbus-Read | Spannung ~230V | Wert: 231.5V (Valide) | **OK** |
| T03 | Docker-Status | Alle Container `Up` | `docker ps`: Up 24h | **OK** |
| T04 | Datenfluss | InfluxDB erhält Daten | Abfrage via CLI erfolgreich | **OK** |
| T05 | Fernzugriff | Login via Cloudflare möglich | SSL-Zertifikat gültig | **OK** |
| T06 | Alerting (Sim.) | Telegram bei 0 Watt | Nachricht empfangen (2 min) | **OK** |

### 1.2.7 Abweichung
Keine signifikanten Abweichungen.

### 1.2.8 Anhänge
*   Netzwerkplan
*   Source Code
*   Configs

### 1.2.9 Glossar
*   **IoT:** Internet of Things
*   **MQTT:** Message Queuing Telemetry Transport
