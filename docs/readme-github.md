---
title: README Ufficiale GitHub
description: Documento README ufficiale del repository open source carlorigoni/eurario su GitHub secondo standard ASD-STE100.
---

# 🎓 Eurario — Repository Ufficiale GitHub

[![Docker Hub](https://img.shields.io/badge/docker%20hub-carlorigoni%2Feurario%3Alatest-blue?logo=docker)](https://hub.docker.com/r/carlorigoni/eurario)
[![FET Solver](https://img.shields.io/badge/FET%20engine-C%2B%2B%20native-orange.svg)](https://lalescu.ro/liviu/fet/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-green.svg)](https://www.gnu.org/licenses/agpl-3.0)

> 🔗 **Repository GitHub:** [github.com/carlorigoni/eurario](https://github.com/carlorigoni/eurario)

Eurario è una suite open source per la modellazione, risoluzione e pubblicazione dell'orario scolastico nelle scuole secondarie italiane, integrata con il solutore nativo C++ **FET (Free Timetabling Software)**.

Zero dipendenze esterne Python, interfaccia reattiva in stile Google Classroom / Material 3 e immagine container multi-architettura pronta all'uso su Docker Hub.

---

## 🌟 Caratteristiche Principali

- **Solutore Euristico FET Integrato**:
  - Calcolo orario automatico con log streaming SSE in tempo reale e tracciamento colli di bottiglia.
  - Salvataggio e ripristino istantaneo dello stadio più avanzato (*highest stage*) in caso di timeout.
- **Sistema di Blocco Orario (Locking)**:
  - Fissa intere classi o singole ore nella griglia con vincoli FET permanenti al 100% (`ConstraintActivityPreferredStartingTime` e `ConstraintActivityPreferredRoom`).
- **Gestione Completa dell'Istituto**:
  - **Docenti**: monte ore cattedra, contratti (intere, COE, spezzoni, part-time), ore buche, massimo ore giornaliere, preferenze orarie e giorno libero contrattuale.
  - **Classi e Gruppi**: articolazioni per lingue straniere (es. Francese, Spagnolo) e suddivisioni di indirizzo tecnico.
  - **Aule e Spazi Didattici**: aule base, palestre condivise con gestione capienza e laboratori specialistici.
  - **Macro-Materie e Accorpamenti**: unione delle cattedre affini per ottimizzare la collocazione didattica.
  - **Disposizioni Automatiche**: algoritmo dedicato per chiudere i buchi orari e bilanciare la presenza di supplenze.
- **Sincronizzazione Organico e Modello Word (.docx)**:
  - Download del modello Word precompilato ed esportazione dell'organico della scuola.
  - Sincronizzazione automatica da file Word (.docx) o foglio Excel con anteprima delle differenze (*Diff Viewer*).
- **Dataset Demo "Scuola di Atene"**:
  - Include un istituto scolastico completo e funzionante con orario già risolto al 100% per testare tutte le funzionalità.
  - Funzione di reset a foglio bianco per iniziare una nuova scuola da zero.
- **Architettura Leggera**:
  - Esegue su Python 3.10+ utilizzando esclusivamente i moduli della Standard Library.

---

## 🐳 Immagine Ufficiale Docker Hub

Eurario è distribuito come immagine container ufficiale pre-compilata:

👉 **Docker Hub Repository:** [`carlorigoni/eurario`](https://hub.docker.com/r/carlorigoni/eurario)

Non richiede l'installazione di compilatori o librerie grafiche sul server host.

---

## 🚀 Avvio Rapido con Docker Compose

1. Crea il file `docker-compose.yml`:
   ```yaml
   version: '3.8'

   services:
     eurario:
       container_name: eurario
       image: carlorigoni/eurario:latest
       restart: unless-stopped
       ports:
         - "8000:8000"
       volumes:
         - ./data:/app/data
       environment:
         - PORT=8000
         - PYTHONUNBUFFERED=1
   ```

2. Avvia il container:
   ```bash
   docker compose up -d
   ```

3. Apri il browser all'indirizzo:
   👉 **`http://localhost:8000`**

---

## 📄 Licenza

Rilasciato sotto licenza [GNU Affero General Public License v3 (AGPLv3)](https://www.gnu.org/licenses/agpl-3.0).
