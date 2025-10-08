# Lastenheft: PV-Anlagen-Überwachungssystem

**Projekt:** PV-Monitoring-System (EcoEnergy Solutions)  
**Auftraggeber:** Herr Max Mustermann, EcoEnergy Solutions GmbH  
**Version:** 1.0  
**Datum:** [Aktuelles Datum]

---

## 1. Einleitung und Zielsetzung

Dieses Dokument beschreibt die Anforderungen an ein Echtzeit-Überwachungssystem für eine bestehende Photovoltaik-Anlage. Ziel ist die digitale Erfassung, Speicherung und Visualisierung von Leistungsdaten, um eine effiziente Wartung und Fehleranalyse zu ermöglichen. Das System soll kostengünstig, wartungsarm und auf Basis von Open-Source-Technologien realisiert werden.

## 2. Ist-Zustand

Die aktuellen Leistungsdaten der PV-Anlage können nur manuell und lokal am Wechselrichter abgelesen werden. Es gibt keine zentrale Datenerfassung, keine Langzeitarchivierung und keine Möglichkeit zur Fernüberwachung oder automatischen Benachrichtigung bei Störungen.

## 3. Funktionale Anforderungen (Was soll das System tun?)

### 3.1 Datenerfassung
- **FR-01:** Das System muss in der Lage sein, die Daten vom Wechselrichter der PV-Anlage auszulesen.
- **FR-02:** Die Kommunikation mit dem Wechselrichter muss über die serielle Schnittstelle Modbus RTU (via RS-485) erfolgen.
- **FR-03:** Folgende Parameter müssen erfasst werden:
    - Spannung (V)
    - Strom (A)
    - Aktuelle Leistung (W)
    - Tagesertrag (kWh)
- **FR-04:** Die Datenerfassung soll in einem regelmäßigen Intervall von 5 bis 10 Sekunden erfolgen.

### 3.2 Datenübertragung und -speicherung
- **FR-05:** Die erfassten Daten müssen über das MQTT-Protokoll im lokalen Netzwerk veröffentlicht werden.
- **FR-06:** Die Daten sollen in einer Zeitreihendatenbank (Time-Series Database) persistent gespeichert werden.
- **FR-07:** Die Datenhistorie muss für einen Zeitraum von mindestens 30 Tagen aufbewahrt werden.

### 3.3 Datenvisualisierung
- **FR-08:** Es muss ein web-basiertes Dashboard zur Visualisierung der Daten bereitgestellt werden.
- **FR-09:** Das Dashboard soll die aktuellen Werte sowie historische Verläufe der erfassten Parameter (siehe FR-03) in Form von Graphen und Anzeigen darstellen.
- **FR-10:** Das Dashboard muss über einen Standard-Webbrowser im Firmennetzwerk erreichbar sein.

### 3.4 Alarmierung
- **FR-11:** Das System soll eine Funktion zur Konfiguration von Alarmen bieten.
- **FR-12:** Bei einem signifikanten Leistungsabfall oder Ausfall der Datenerfassung soll automatisch eine Benachrichtigung per E-Mail an einen konfigurierbaren Empfänger gesendet werden.

## 4. Nicht-funktionale Anforderungen (Wie gut soll das System sein?)

- **NFR-01 (Performance):** Das System muss die Daten in Echtzeit (mit der in FR-04 definierten Latenz) verarbeiten und darstellen können.
- **NFR-02 (Zuverlässigkeit):** Das System soll stabil und für den Dauerbetrieb (24/7) ausgelegt sein. Nach einem Stromausfall oder Neustart müssen alle Dienste automatisch wieder anlaufen.
- **NFR-03 (Wartbarkeit):** Die gesamte Software-Infrastruktur (Datenbank, MQTT-Broker, Visualisierungs-Tool) muss über Docker-Container verwaltet werden. Eine zentrale Konfigurationsdatei (Docker Compose) soll den Start, Stopp und die Aktualisierung aller Dienste ermöglichen.
- **NFR-04 (Kosteneffizienz):** Die Lösung soll auf kostengünstiger Hardware (Raspberry Pi) und primär auf Open-Source-Software basieren.

## 5. Lieferumfang

1.  Vollständig konfigurierte Software-Umgebung auf einem Raspberry Pi 4.
2.  Ein Python-Skript zur Auslesung der Modbus-Daten und Veröffentlichung via MQTT.
3.  Eine Docker-Compose-Konfiguration zum Starten aller benötigten Dienste.
4.  Ein vorkonfiguriertes Grafana-Dashboard zur Visualisierung.
5.  Eine vollständige technische Dokumentation, bestehend aus:
    - Lastenheft (dieses Dokument)
    - Pflichtenheft
    - Betriebliche Dokumentation (Installations- und Wartungsanleitung)

## 6. Abnahmekriterien

Das Projekt gilt als erfolgreich abgeschlossen, wenn:
- alle unter Punkt 3 und 4 genannten Anforderungen nachweislich erfüllt sind.
- der Datenfluss vom Wechselrichter bis zum Dashboard stabil und korrekt funktioniert.
- die Dokumentation vollständig und verständlich ist.
- eine erfolgreiche Präsentation und Übergabe des Systems stattgefunden hat.