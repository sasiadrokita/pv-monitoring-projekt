# 3. Kundendokumentation (Benutzerhandbuch)

## 3.1 Einleitung
Herzlichen Glückwunsch zu Ihrem neuen PV-Monitoring-System!
Dieses Handbuch erklärt Ihnen, wie Sie auf das System zugreifen, die Daten interpretieren und was im Störungsfall zu tun ist.

## 3.2 Zugriff auf das System

Das Monitoring-System ist über jeden Webbrowser (PC, Tablet, Smartphone) erreichbar. Die genaue URL zum Zugriff wird Ihnen zur Sicherheit laufend über den **Monitoring-Bot in Telegram** direkt in den Benachrichtigungen angezeigt.

### 3.2.1 Anmeldung
1.  Öffnen Sie die vom Bot genannte URL.
2.  Geben Sie Ihre Zugangsdaten ein:
    *   **Benutzername:** `admin` (oder Ihr personalisierter Nutzer)
    *   **Passwort:** *(Wurde Ihnen bei der Übergabe mitgeteilt)*
3.  Klicken Sie auf **"Log in"**.

*[Platzhalter für Screenshot: Login-Bildschirm / Cloudflare Access]*

## 3.3 Bedienung des Dashboards

Nach dem Login sehen Sie die Hauptübersicht ("Dashboard").

*[Platzhalter für Screenshot: Hauptansicht Grafana Dashboard]*

### 3.3.1 Die Elemente im Überblick
*   **Aktuelle Leistung (Watt):** Tachometer-Anzeige, die die momentane Leistung anzeigt.
*   **Tagesertrag und kumulierter Tagesertrag (kWh):** Balkendiagramm zur Darstellung der täglichen Energieerzeugung.
*   **Strom (Ampere):** Der aktuell gemessene Stromfluss.
*   **Spannung AC (Volt):** Die aktuelle Netzspannung.
*   **Total (kWh):** Der gesamte Zählerstand seit Inbetriebnahme.
*   **Verlaufsdiagramme (Liniendiagramme):**
    *   Spannungsverlauf
    *   Leistungsverlauf
    *   Stromverlauf
    *   Verlauf des Gesamtertrags (Total kWh)

*[Platzhalter für Screenshot: Detailansicht der Diagramme im Dashboard]*

### 3.3.2 Zeitbereich ändern
Oben rechts finden Sie die Zeitauswahl (z.B. "Last 6 hours").
*   Klicken Sie darauf, um z.B. "Last 7 days" oder "This month" auszuwählen.
*   Das Dashboard aktualisiert sich automatisch.

## 3.4 Alarmierung (Benachrichtigungen)

Das System überwacht sich selbst. Sollte ein Fehler auftreten, erhalten Sie eine Nachricht via **Telegram**.

**Wann werde ich benachrichtigt?**
*   Wenn das System keine Daten mehr empfängt (länger als 15 Minuten).
*   Während eines System-Neustarts (Reboots) des Monitorings.
*   Nach der erfolgreichen Wiederherstellung (Rückkehr zum Normalbetrieb nach vorherigem Fehler oder Ausfall).

*[Platzhalter für Screenshot: Beispiel einer Telegram-Alarmmeldung]*

**Was muss ich tun?**
Prüfen Sie, ob es einen Stromausfall gibt oder ob der Wechselrichter eine Fehlermeldung anzeigt. Falls alles in Ordnung scheint, befolgen Sie Kapitel 3.5.

## 3.5 Erste Hilfe bei Störungen

### 3.5.1 Das Dashboard ist leer / zeigt "No Data"
1.  Warten Sie 5-10 Minuten. Manchmal startet das System neu (z.B. nach Update).
2.  Prüfen Sie, ob der Zähler (im Keller) Strom hat (Display leuchtet?).
3.  Starten Sie das System neu (siehe 3.5.2).

### 3.5.2 System neu starten
Sollte das System hängen, können Sie den Raspberry Pi neu starten:
1.  Ziehen Sie kurz den Netzstecker des Raspberry Pi (im Serverschrank).
2.  Warten Sie 10 Sekunden.
3.  Stecken Sie ihn wieder ein.
4.  Nach ca. 2-3 Minuten ist das System wieder online.

## 3.6 Support-Kontakt

Bei Problemen, die Sie nicht selbst lösen können, wenden Sie sich bitte an den IT-Support:

**Ansprechpartner:** Mateusz Nowak
**Telefon:** +49 171 1110639
**E-Mail:** support@eco-energy.com
**Servicezeiten:** Mo-Fr, 08:00 - 17:00 Uhr
