# PV-Monitoring System
**Kundendokumentation (Benutzerhandbuch)**

**Abschlussprüfung Sommer 2026**
**Fachinformatiker für Digitale Vernetzung (AP T2)**

**Prüfling:** Mateusz Nowak
**Identnummer:** 141-13256

---

[TOC]

---

# 3. Kundendokumentation (Benutzerhandbuch)

## 3.1 Einleitung
Herzlichen Glückwunsch zu Ihrem neuen PV-Monitoring-System!
Dieses Handbuch erklärt Ihnen, wie Sie auf das System zugreifen, die Daten interpretieren und was im Störungsfall zu tun ist.

## 3.2 Zugriff auf das System

Das Monitoring-System ist über jeden Webbrowser (PC, Tablet, Smartphone) erreichbar.

**URL:** `https://pv.eco-energy.com`

### 3.2.1 Anmeldung
1.  Öffnen Sie die oben genannte URL.
2.  Geben Sie Ihre Zugangsdaten ein:
    *   **Benutzername:** `admin` (oder Ihr personalisierter Nutzer)
    *   **Passwort:** *(Wurde Ihnen bei der Übergabe mitgeteilt)*
3.  Klicken Sie auf **"Log in"**.

## 3.3 Bedienung des Dashboards

Nach dem Login sehen Sie die Hauptübersicht ("Dashboard").

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

### 3.3.2 Zeitbereich ändern
Oben rechts finden Sie die Zeitauswahl (z.B. "Last 6 hours").
*   Klicken Sie darauf, um z.B. "Last 7 days" oder "This month" auszuwählen.
*   Das Dashboard aktualisiert sich automatisch.

## 3.4 Alarmierung (Benachrichtigungen)

Das System überwacht sich selbst. Sollte ein Fehler auftreten, erhalten Sie eine Nachricht via **Telegram**.

**Wann werde ich benachrichtigt?**
*   Wenn die Leistung tagsüber (zwischen 10:00 und 14:00 Uhr) plötzlich auf 0 Watt fällt.
*   Wenn das System keine Daten mehr empfängt (länger als 15 Minuten).

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
