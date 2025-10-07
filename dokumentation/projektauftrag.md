# Projektauftrag: PV-Anlagen-Überwachung mit IoT-Technologien

**Projektname:** PV-Monitoring-System (EcoEnergy Solutions)

**Auftraggeber:** Herr Max Mustermann, EcoEnergy Solutions GmbH

**Datum:** [Aktuelles Datum]
**Version:** 1.0

---

## 1. Ausgangssituation

Die Firma EcoEnergy Solutions betreibt eine ältere Photovoltaik-Anlage (PV), welche über keine moderne Echtzeit-Überwachung verfügt. Die Leistungsdaten sind nur manuell am Wechselrichter ablesbar, was eine effiziente Wartung und Fehlerdiagnose erschwert. Es besteht der dringende Bedarf, die Leistungsparameter (Spannung, Strom, Leistung, Tagesertrag) digital zu erfassen, zu archivieren und grafisch darzustellen.

## 2. Projektziel

Entwicklung und Implementierung eines kostengünstigen und wartungsarmen Echtzeit-Überwachungssystems auf Basis eines Raspberry Pi 4. Das System soll die Daten der PV-Anlage über eine serielle Schnittstelle (Modbus RTU via RS-485) auslesen, über MQTT kommunizieren und in einer Docker-Container-Umgebung visualisieren (TICK-Stack/Grafana).

## 3. Anforderungen und Rahmenbedingungen

| Parameter | Beschreibung |
| :--- | :--- |
| **Hardware** | Raspberry Pi 4 Model B, RS-485 zu USB Konverter. |
| **Software** | Linux OS (Raspberry Pi OS), Docker Engine, Docker Compose. |
| **Kommunikation** | MQTT als zentrales Nachrichtenprotokoll. |
| **Daten** | Echtzeit-Erfassung (alle 5-10 Sekunden) und Langzeitarchivierung (mindestens 30 Tage). |
| **Visualisierung** | Web-basiertes Interface (Grafana) mit Dashboard-Ansicht. |
| **Alerting** | Möglichkeit zur Konfiguration von E-Mail-Alarmen bei Leistungsabfall. |
| **Wartbarkeit** | Alle Dienste müssen über Docker Compose verwaltet werden können. |
| **Dokumentation** | Vollständige technische und betriebliche Dokumentation (Lastenheft, Pflichtenheft, Betriebliche Dokumentation) in deutscher Sprache. |

## 4. Abgrenzung

Das Projekt umfasst nicht die Steuerung der PV-Anlage oder die Integration von externen Wetterdaten. Der Fokus liegt auf dem lokalen Monitoring im Firmennetzwerk.

---

## 5. Meilensteine 

1.  Initialisierung und Dokumentation (Lastenheft).
2.  Einrichtung der Docker-Infrastruktur (MQTT, InfluxDB, Grafana, Telegraf).
3.  Entwicklung des Modbus-Publishing-Skripts (Python).
4.  Integration und Test (Datenfluss Modbus -> MQTT -> InfluxDB -> Grafana).
5.  Fertigstellung der Pflichtenheft- und Betrieblichen Dokumentation.
6.  Projektabschluss und Präsentation.
