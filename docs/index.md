---
title: Panoramica Generale
description: Documentazione tecnica e operativa ufficiale di Eurario, suite open source per la gestione e risoluzione dell'orario scolastico con motore euristico FET secondo standard ASD-STE100.
---

# 🎓 Eurario — Documentazione Ufficiale

Benvenuto nella documentazione di **Eurario**, la suite open source per progettare, calcolare, ottimizzare e pubblicare l'orario scolastico nelle scuole secondarie di primo e secondo grado.

Eurario integra un'interfaccia web responsive conforme a Material Design 3 con il motore solutore euristico nativo **FET** (*Free Timetabling Software*), sviluppato da Liviu Lalescu e Volker Dirr.

---

## 🧭 Navigazione Rapida della Guida

<div class="eurario-card-grid">
  <a href="getting-started/" class="eurario-card">
    <h3>🚀 Primo Accesso & Anagrafiche</h3>
    <p>Autenticazione con Google Workspace, gestione multi-istituto, anagrafiche docenti, classi, materie, aule e plessi.</p>
  </a>

  <a href="user-guide/" class="eurario-card">
    <h3>📖 Guida Utente & Casi d'Uso</h3>
    <p>Guida operativa in 14 fasi cronologiche e 10 casi d'uso concreti con schermate di riferimento.</p>
  </a>

  <a href="timetable-flow/" class="eurario-card">
    <h3>⚡ Flusso di Generazione & Ottimizzazione</h3>
    <p>Assegnazione cattedre, scomposizione blocchi didattici, solutore asincrono FET, Relaxation Engine e disposizioni.</p>
  </a>

  <a href="cross-reference/" class="eurario-card">
    <h3>🔬 Parametri & Cross-Reference FET</h3>
    <p>Tavola comparativa tra i parametri di Eurario e i tag XML generati per il motore C++ FET.</p>
  </a>

  <a href="docker-deploy/" class="eurario-card">
    <h3>🐳 Installazione & Deploy con Docker</h3>
    <p>Installazione su server Linux x86/ARM, configurazione Docker Compose, Nginx, Caddy e Cloudflare Tunnel.</p>
  </a>

  <a href="architecture/" class="eurario-card">
    <h3>🏗️ Architettura & DevOps</h3>
    <p>Pipeline CI/CD con GitHub e Docker Hub, controllo di versione e aggiornamenti del server in produzione.</p>
  </a>
</div>

---

## 🏛️ Architettura del Sistema

Eurario adotta un'architettura modulare containerizzata senza librerie esterne pesanti in Python:

```mermaid
graph TB
    subgraph Frontend["Client Web (Browser Moderno)"]
        UI["Interfaccia SPA Reattiva\n(HTML5 / CSS3 / Vanilla JS)"]
        LiveSSE["Streaming Log Solver\n(Server-Sent Events)"]
        DnD["Griglia Orario Interattiva\n(Drag & Drop Disposizioni e Blocchi)"]
    end

    subgraph Backend["Eurario Core Engine (Python 3.10+)"]
        Server["Server HTTP Asincrono Multi-Thread"]
        Auth["Controllo Accessi RBAC & Google OAuth 2.0"]
        DB["Database JSON Multi-Tenant Isolato\n(Controllo Concorrenza Ottimistica OCC)"]
        FETGen["Compilatore & Generatore XML FET"]
        Diag["Relaxation Engine & Conflict Resolver"]
        DispAlgo["Algoritmo Bilanciamento Disposizioni (D)"]
        PrintEng["Motore Tipografico Word (.docx A3) & PDF"]
    end

    subgraph NativeCore["Motore Solutore Euristico"]
        FETCL["Processo Binario Nativo fet-cl (C++)"]
    end

    subgraph Storage["Persistenza Dati (/app/data)"]
        VolData["data/<school_id>/project.json"]
        VolSnap["data/<school_id>/snapshots/*.fet"]
        VolSolv["data/<school_id>/solved_timetable.xml"]
    end

    UI -->|"HTTP REST API (JSON)"| Server
    LiveSSE <-->|"SSE /api/solver/stream"| Server
    DnD -->|"PUT /api/timetable/move"| Server
    Server --> Auth
    Server --> DB
    Server --> PrintEng
    DB <-->|"I/O Atomico & Lock"| Storage
    Server -->|"Compila dataset completo"| FETGen
    FETGen -->|"File .fet su disco"| Storage
    Server -->|"Esegue subprocess asincrono"| FETCL
    FETCL -->|"Flusso streaming stdout/stderr"| Server
    FETCL -->|"Salva orario matematicamente risolto"| Storage
    Server -->|"In caso di stallo matematico"| Diag
    Server -->|"Calcolo buchi e sostituzioni"| DispAlgo
```

---

## 🌟 Caratteristiche Chiave & Normativa CCNL

Eurario è progettato sulle regole contrattuali e didattiche della scuola italiana:

### 1. Rispetto dei Contratti Docenti
* **Cattedre Ordinarie (18 ore)**, **Part-time** (da 2 a 5 giorni settimanali) e **Spezzoni orari**.
* **Cattedre Orario Esterne (COE)**: Gestione di ore e giorni dedicati alla scuola di completamento.
* **Giorno Libero Contrattuale**: Tutela assoluta con vincolo rigido FET al 100%.
* **Controllo Ore Buche**: Limite massimo configurabile per giorno (es. max 1) e per settimana (es. max 2).
* **Minimo Ore Giornaliere**: Soglia minima di presenza (es. min 2 ore) per evitare spostamenti inefficienti.

### 2. Didattica e Articolazioni
* **Scomposizione Automatica in Blocchi Didattici**: Conversione automatica del monte ore in sequenze ottimali (`2+1+1` per 4 ore, `2+1` per 3 ore, `2+2+1+1` per 6 ore).
* **Macro-Materie & Accorpamenti**: Unione delle cattedre affini dello stesso docente (es. *Matematica e Fisica*).
* **Classi Articolate & Sdoppiamenti**: Supporto per lingue comunitarie (*Francese / Spagnolo*) e indirizzi tecnici.
* **Fasce Orarie Preferenziali**: Assegnazione prioritaria nelle prime ore (*PRIME*) o nelle ultime ore (*ULTIME*).
* **Esclusione Rientri Pomeridiani**: Divieto di collocazione nelle ore pomeridiane (7ª e 8ª ora).

### 3. Logistica Multi-Plesso & Aule Speciali
* **Centrale e Succursali**: Gestione dei tempi di trasferimento e limite sui cambi plesso giornalieri.
* **TimeMachine Plessi**: Simulatore ora per ora con mappa metropolitana dei docenti e monitoraggio spostamenti.
* **Palestre e Laboratori**: Capienza controllata e prevenzione di sovrapposizioni.

### 4. Disposizioni & Supplenze ("D")
* **Algoritmo di Bilanciamento**: Assegna le ore a disposizione per chiudere i buchi orari e distribuire la vigilanza.
* **Indicatori di Densità Oraria (`👥 X D`)**: Mostra in tempo reale il numero di docenti a disposizione presenti in ogni ora.
* **Griglia Drag & Drop**: Spostamento manuale delle ore con verifica immediata dei vincoli.

### 5. Esportazioni Tipografiche
* **Tabellone Docenti Word (.docx A3 Orizzontale)**: Conforme alla Procedura 12 con righe di intestazione ripetute.
* **Orario Classi PDF**: Impaginazione con colori pastello o modalità monocromatica per fotocopiatrici.
* **Controllo Concorrenza (OCC)**: Previene la sovrascrittura simultanea dei dati tra più utenti.

---

## 🖥️ Interfaccia Web

<div class="doc-figure">
  <img src="assets/eurario-cattedre.png?v=1.9.57" alt="Eurario — Quadro Cattedre e Assegnazioni Insegnamenti" class="doc-screenshot">
  <div class="doc-caption">Figura 1.1: Schermata di gestione cattedre, assegnazione ore e scomposizione automatica in blocchi.</div>
</div>

---

## 📜 Licenza & Crediti

Eurario è distribuito sotto licenza **GNU Affero General Public License v3 (AGPLv3)**.

* **Sviluppo & Architettura**: [Carlo Rigoni](https://github.com/carlorigoni)
* **Consulenza Metodologica**: Federico Rettore
* **Motore Euristico FET**: Liviu Lalescu e Volker Dirr ([Sito ufficiale FET](https://lalescu.ro/liviu/fet/))
* **Repository Ufficiale GitHub**: [github.com/carlorigoni/eurario](https://github.com/carlorigoni/eurario)
