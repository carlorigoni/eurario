---
title: Architettura & Pipeline DevOps
description: Guida all'architettura software di Eurario, alla pipeline CI/CD con GitHub e Docker Hub, al controllo di versione e agli aggiornamenti in produzione secondo standard ASD-STE100.
---

# 🏗️ Architettura del Software & Pipeline DevOps

Questo documento descrive l'architettura tecnica di Eurario e il flusso operativo di rilascio, distribuzione e aggiornamento.

---

## 1. Mappa E2E dell'Ecosistema Eurario

Il diagramma seguente illustra l'interazione tra ambiente di sviluppo, repository GitHub, registro Docker Hub, rete CDN Cloudflare e server di produzione:

```mermaid
flowchart TD
    subgraph LocalDev["💻 Ambiente di Sviluppo Locale"]
        DevFiles["Sorgenti Eurario\n(Python, HTML5, Vanilla JS, CSS)"]
        LocalFET["Compilatore & Solutore\nFET Nativo (C++)"]
        LocalTest["Test di Integrazione\n& Validazione Vincoli"]
        DevFiles --> LocalFET
        LocalFET --> LocalTest
    end

    subgraph GitHubRepo["🐙 GitHub Repository (carlorigoni/eurario)"]
        MainBranch["Branch main\n(Codice Stabile & Verificato)"]
        GitTag["Git Tag di Rilascio\n(es. v1.9.6)"]
        GHActions["GitHub Actions\n(Validazione Docs & Test Build)"]
        MainBranch --> GitTag
        MainBranch --> GHActions
    end

    subgraph CDNPipeline["☁️ Cloudflare Pages (Edge CDN)"]
        CF_Landing["eurario.it\n(Landing Page & Showcase)"]
        CF_Docs["docs.eurario.it\n(Manuale & Documentazione Zensical)"]
    end

    subgraph ContainerRegistry["🐳 Docker Hub Registry (carlorigoni/eurario)"]
        MultiArchBuild["Build Multi-Architettura\n(linux/amd64 & linux/arm64)"]
        TagLatest["Tag: latest\n(Rolling Production Tag)"]
        TagVersion["Tag Immutabile: vX.Y.Z\n(es. :v1.9.6)"]
        MultiArchBuild --> TagLatest
        MultiArchBuild --> TagVersion
    end

    subgraph ProductionEnv["🏢 Server di Produzione & Istituti Scolastici"]
        subgraph ServerHost["Server Host / VM / NAS"]
            ReverseProxy["Reverse Proxy & TLS\n(Caddy / Nginx / Cloudflare Tunnel)"]
            DockerEngine["Docker Engine Runtime"]
            Watchtower["Watchtower / Update Cron\n(Controllo Notturno Nuove Immagini)"]
            PersistentVol["Volume Dati Persistente\n(/instance <--> ./data host)"]
        end
        subgraph ContainerApp["Container Eurario"]
            PyServer["Server HTTP Python\n(Standard Library nativa)"]
            AuthEngine["Auth & Brute-Force Defense\n(PBKDF2 600k + Rate Limiter)"]
            FETExec["fet-cl Nativo\n(Binario compilato C++)"]
            LocalData["Storage JSON / Snapshot .fet\n(Anagrafiche, Vincoli, Orari)"]
        end
    end

    %% Relazioni tra ambienti
    DevFiles -->|"git commit & git push"| MainBranch
    GitTag -->|"Trigger Build Automatica"| MultiArchBuild
    MainBranch -->|"Webhook Git Deploy"| CF_Landing
    MainBranch -->|"Webhook Git Deploy"| CF_Docs

    TagLatest -.->|"docker pull / auto-update"| DockerEngine
    DockerEngine --> ContainerApp
    ReverseProxy -->|"Proxy pass :8000"| PyServer
    PyServer --> AuthEngine
    PyServer --> FETExec
    PyServer <--> LocalData
    LocalData <--> PersistentVol
    Watchtower -.->|"Interroga Tags"| TagLatest

    ContainerApp -.->|"Verifica Nuove Versioni\nvia Docker Hub API"| ContainerRegistry
```

---

## 2. Componenti Software Interni & Runtime Locale

L'architettura interna elimina librerie terze non necessarie per garantire stabilità a lungo termine.

```mermaid
graph LR
    Browser["🌐 Browser Client\n(Material 3 / Vanilla ES6)"] 
    -->|"HTTP REST API & EventStream"| ServerPy["⚙️ webapp/server.py\n(Python HTTP Server Nativo)"]
    
    subgraph CoreBackend["Backend Eurario (Standard Library)"]
        ServerPy --> AuthPy["🛡️ webapp/auth.py\n(PBKDF2, IP Lockout, Rate Limiter)"]
        ServerPy --> Exporter["📄 Procedura 9 & 12\n(Generatore PDF A3/A4 e Word .docx)"]
        ServerPy --> SolverManager["⚡ Timetable Solver Manager\n(Subprocess fet-cl C++)"]
    end

    subgraph NativeBinary["Solutore ad Alte Prestazioni"]
        SolverManager --> FET["bin/fet-cl\n(C++ Nativo Qt-Free FET Engine)"]
    end

    subgraph DataStorage["Persistenza Dati Atomica (data/)"]
        ServerPy <--> JsonData["project.json\n(Salvataggio Atomico)"]
        ServerPy <--> Snapshots["snapshots/\n(Punti di ripristino .fet)"]
        FET --> SolutionXML["solved_timetable.xml\n(Risultato calcolo FET)"]
    end
```

### Dettaglio dei Singoli Componenti

#### 1. Frontend (Vanilla Web Stack)
* Sviluppato in HTML5 semantico, Vanilla JavaScript ES6+ e CSS moderno con variabili custom.
* Supporta il tema chiaro e il tema scuro in modo nativo.
* Interfaccia grafica conforme alle linee guida Material Design 3.
* Nessun bundler in fase di esecuzione. Il caricamento nel browser è immediato.
* Controllo della cache con query string di versione (`?v=X.Y.Z`).

#### 2. Backend Python (`webapp/server.py` & `webapp/auth.py`)
* Esegue su Python 3.10+ senza framework esterni.
* Utilizza esclusivamente la Standard Library di Python (`http.server`, `urllib`, `json`, `hashlib`, `subprocess`).
* Sicurezza accessi: hash password con PBKDF2-HMAC-SHA256 a 600.000 iterazioni e salting a 16 byte.
* Protezione brute-force: ritardo progressivo e blocco temporizzato per indirizzo IP.

#### 3. Motore Solutore Euristico (`bin/fet-cl`)
* Binario nativo C++ compilato dal sorgente ufficiale FET di Liviu Lalescu e Volker Dirr.
* Viene eseguito come subprocess asincrono headless senza interfaccia Qt.
* Comunica lo stato di avanzamento al server tramite standard output (stdout).

#### 4. Persistenza Atomica (`data/`)
* I dati scolastici risiedono in file JSON strutturati (`project.json`).
* Le scritture su disco sono atomiche: salvataggio su file temporaneo seguito da `os.replace`.
* Previene la corruzione dei dati in caso di spegnimento improvviso del server.

---

## 3. Gestione Versioni & Flusso Git

Eurario segue la specifica **Semantic Versioning (SemVer 2.0.0)** nel formato `vMAJOR.MINOR.PATCH`:
* **`MAJOR`**: Modifiche architetturali rilevanti o cambi di struttura dati non retrocompatibili.
* **`MINOR`**: Nuove funzionalità didattiche, nuove stampe o estensione dei vincoli FET.
* **`PATCH`**: Correzioni di bug, miglioramenti prestazionali e aggiornamenti di sicurezza.

### File Sincronizzati al Rilascio di Versione

| File | Variabile / Riferimento | Scopo |
| :--- | :--- | :--- |
| `webapp/server.py` | `APP_VERSION = "1.9.6"` | Risposta API e log di avvio server |
| `webapp/static/app.js` | `const APP_VERSION = '1.9.6'` | Verifica aggiornamenti su Docker Hub |
| `webapp/static/index.html` | Etichette interfaccia e cache buster | Sidebar, About modal e invalidazione asset browser |
| `landing/content/site_data.json` | `"current_version": "v1.9.6"` | Versione mostrata sul sito eurario.it |
| `landing/index.html` | Tag immagine Docker consigliata | Visualizzazione comando di download nella hero section |
| `zensical.toml` | Parametri asset CSS/JS | Cache busting della documentazione docs.eurario.it |

---

## 4. Pipeline di Pubblicazione su Docker Hub

Alla creazione di un nuovo tag Git (es. `git tag v1.9.6 && git push origin v1.9.6`), la pipeline esegue i seguenti passaggi:

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Sviluppatore / Maintainer
    participant Git as GitHub (carlorigoni/eurario)
    participant Hub as Registro Docker Hub
    participant Prod as Server di Produzione

    Dev->>Git: git push origin vX.Y.Z
    Git->>Hub: Compilazione automatica multi-arch (linux/amd64 e linux/arm64)
    Hub->>Hub: Pubblicazione immagine carlorigoni/eurario:latest
    Hub->>Hub: Creazione tag immutabile carlorigoni/eurario:vX.Y.Z

    loop Verifica Periodica
        Prod->>Hub: GET /v2/repositories/carlorigoni/eurario/tags
        Hub-->>Prod: Elenco ultimi tag disponibili
    end

    alt Nuova Versione Disponibile
        Prod->>Prod: Mostra notifica aggiornamento
        Prod->>Hub: docker compose pull && docker compose up -d
        Prod->>Prod: Riavvio a caldo con dati intatti
    else Versione Allineata
        Prod->>Prod: Mostra badge verde "Versione Aggiornata"
    end
```

### Supporto Multi-Architettura
La build genera un unico manifest multi-piattaforma per:
* **`linux/amd64`**: server Intel/AMD x86_64 e macchine virtuali cloud.
* **`linux/arm64`**: Apple Silicon (M-series), server ARM e Raspberry Pi 5.

---

## 5. Procedure di Aggiornamento in Produzione

### Procedura Manuale da Terminale
1. Accedi via SSH al server della scuola.
2. Posizionati nella directory di Eurario:
   ```bash
   cd /opt/eurario
   ```
3. Scarica la nuova immagine container:
   ```bash
   docker compose pull
   ```
4. Riavvia i container:
   ```bash
   docker compose up -d
   ```
5. Tutti i dati memorizzati nel volume `./data` rimangono preservati.

### Procedura di Aggiornamento Automatico con Watchtower
Per abilitare l'aggiornamento automatico orario senza intervento manuale:
1. Inserisci il servizio Watchtower nel file `docker-compose.yml`:
   ```yaml
   watchtower:
     image: containrrr/watchtower
     container_name: eurario_watchtower
     restart: unless-stopped
     environment:
       - DOCKER_API_VERSION=1.41
       - WATCHTOWER_HTTP_API_UPDATE=true
       - WATCHTOWER_HTTP_API_TOKEN=eurario-update-token
     volumes:
       - /var/run/docker.sock:/var/run/docker.sock
     command: --interval 3600 --cleanup eurario
   ```
2. Salva e riavvia con `docker compose up -d`.

### Procedura di Aggiornamento In-App ("Aggiorna ora")
1. Apri la barra laterale di Eurario nel browser.
2. Se è disponibile un aggiornamento, il badge di versione diventa ambra.
3. Fai clic sul badge di versione per aprire il modale di aggiornamento.
4. Fai clic sul pulsante **🚀 Aggiorna ora**.
5. Il server attiva l'aggiornamento tramite Watchtower o socket Docker locale.
6. Al termine del riavvio, fai clic su **Ricarica Pagina**.

---

## 6. Ruolo di Cloudflare nell'Ecosistema

Cloudflare gestisce la distribuzione CDN, la sicurezza perimetrale e l'accesso remoto on-premise:

```mermaid
flowchart LR
    subgraph InternetUsers["🌐 Docenti, Studenti & Visitatori"]
        BrowserDocs["Consultazione Documentazione\n(docs.eurario.it)"]
        BrowserLanding["Sito Istituzionale\n(eurario.it)"]
        BrowserApp["Dirigente & Commissione Orario\n(app.eurario.it)"]
    end

    subgraph CloudflareGlobal["☁️ Rete Edge Globale Cloudflare"]
        EdgeDNS["DNS Anycast + WAF + Anti-DDoS"]
        EdgeTLS["Terminazione SSL/TLS + HTTP/3"]
        CFPages["Cloudflare Pages (Hosting Statico Edge)"]
        CFTunnel["Cloudflare Tunnel (Zero-Trust Ingress)"]
    end

    subgraph SchoolInfrastructure["🏫 Rete Scolastica On-Premise"]
        Cloudflared["Demone cloudflared (Container)"]
        EurarioContainer["Container Eurario WebApp (:8000)"]
        SchoolData["Storage Dati Persistenti (data/)"]
    end

    BrowserDocs --> EdgeDNS --> EdgeTLS --> CFPages
    BrowserLanding --> EdgeDNS --> EdgeTLS --> CFPages
    BrowserApp --> EdgeDNS --> EdgeTLS --> CFTunnel
    CFTunnel <-->|"Tunnel Crittografato Outbound"| Cloudflared
    Cloudflared -->|"HTTP Locale :8000"| EurarioContainer
    EurarioContainer <--> SchoolData
```

### Vantaggi dell'Infrastruttura Edge
* **Cloudflare Pages**: ospita `eurario.it` e `docs.eurario.it` con build automatica su push Git e distribuzione edge globale.
* **WAF e Protezione DDoS**: blocca attacchi volumetrici e applicativi ai livelli 3, 4 e 7.
* **Cloudflare Tunnel**: consente l'accesso sicuro a Eurario da remoto senza aprire porte nel firewall scolastico e senza richiedere IP pubblico statico.
