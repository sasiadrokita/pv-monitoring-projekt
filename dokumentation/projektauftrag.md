1. Ausgangssituation und Projektidee

Die Leistungsdaten der firmeneigenen Photovoltaik-Anlage werden aktuell manuell und nur lokal am Wechselrichter abgelesen. Dieser Prozess ist zeitaufwendig und erlaubt keine kontinuierliche Überwachung oder historische Auswertung der Anlageneffizienz. Bei Störungen oder Leistungsabfällen erfolgt eine Reaktion nur mit erheblicher Verzögerung.

Die Idee dieses Abschlussprojekts ist die Entwicklung einer eigenständigen, kosteneffizienten und wartungsarmen Lösung zur automatisierten Erfassung und Visualisierung dieser Betriebsdaten in Echtzeit.

2. Projektziele

Hauptziel:
Die Erstellung eines voll funktionsfähigen Prototyps für ein Monitoring-System, das die Daten einer PV-Anlage erfasst, speichert und in einem webbasierten Dashboard visualisiert.

Funktionale Ziele:

Automatische Datenerfassung: Das System soll selbstständig und in regelmäßigen Intervallen Daten direkt vom Wechselrichter auslesen.
Zentrale Visualisierung: Die erfassten Daten (aktuelle Leistung, Tagesertrag etc.) sollen über einen Webbrowser in Form von Graphen und Anzeigen zugänglich gemacht werden.
Proaktive Alarmierung: Bei signifikanten Störungen (z.B. starker Leistungsabfall) soll das System automatisch eine Benachrichtigung per E-Mail versenden können.
Modulare Architektur: Die gesamte Software-Lösung soll auf Open-Source-Technologien basieren und mithilfe von Docker-Containern aufgebaut werden. Dies gewährleistet eine hohe Wartbarkeit und einfache Skalierbarkeit für die Zukunft.
Nicht-Ziele (Was ist nicht Teil des Projekts?):

Die aktive Steuerung der PV-Anlage.
Funktionen zur Abrechnung oder Einspeisevergütungsberechnung.
3. Erwarteter Nutzen

Der Nutzen des Projekts liegt in der Steigerung der Betriebssicherheit und Effizienz der PV-Anlage. Durch die Echtzeit-Überwachung und automatische Alarmierung können Ertragsverluste minimiert werden. Zudem wird der manuelle Kontrollaufwand erheblich reduziert. Das Projekt schafft eine wertvolle Datengrundlage für zukünftige Optimierungen und dient als skalierbarer Prototyp für weitere Anlagen.

4. Benötigte Ressourcen zur Projektdurchführung

Um dieses Projekt erfolgreich realisieren zu können, werden die folgenden Sachmittel benötigt. Die Auswahl zielt auf eine zuverlässige und für den 24/7-Dauerbetrieb ausgelegte Lösung ab.


a) Hardware

Kernkomponenten (Edge-Device):

1x Edge-Computer: Raspberry Pi 4 (4 GB RAM) oder neuer.
Begründung: Bietet ausreichend Leistung für die parallele Ausführung der benötigten Dienste (Datenbank, Webserver etc.).
1x Stromversorgung: Offizielles USB-C Netzteil.
Begründung: Eine stabile Stromversorgung ist kritisch, um Systemabstürze und Datenkorruption zu vermeiden.
1x Speichermedium: High-Endurance microSD-Karte (mind. 32 GB).
Begründung: Diese Karten sind für den Dauerbetrieb ausgelegt und haben eine höhere Lebensdauer als Standardkarten.
1x Gehäuse: Gehäuse mit passiver oder aktiver Kühlung.
Begründung: Gewährleistet die thermische Stabilität im Dauerbetrieb und verhindert Leistungsverluste durch Überhitzung.
Schnittstellen-Hardware:

1x USB-zu-RS485-Adapter:
Begründung: Wird zur physischen Anbindung an die serielle Schnittstelle (Modbus RTU) des Wechselrichters benötigt.
Optionale Empfehlung für erhöhte Langlebigkeit:

1x Externe USB-SSD (mind. 128 GB):
Begründung: Zur Auslagerung der Datenbank, um die microSD-Karte zu schonen und die Lebensdauer des Gesamtsystems zu maximieren.


b) Software

Für dieses Projekt wird ausschließlich lizenzkostenfreie Open-Source-Software verwendet. Es fallen keine zusätzlichen Softwarekosten an.
Technologie-Stack: Docker, Python, InfluxDB (Datenbank), Grafana (Visualisierung), Mosquitto (MQTT).
Zugang: Administratorrechte auf dem Entwicklungsrechner zur Installation der benötigten Entwicklungswerkzeuge (z.B. VS Code).