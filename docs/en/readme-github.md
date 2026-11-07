---
title: Official GitHub README
description: Official README document for the carlorigoni/eurario open-source repository on GitHub according to ASD-STE100 standards.
---

# 🎓 Eurario — Official GitHub Repository

[![Docker Hub](https://img.shields.io/badge/docker%20hub-carlorigoni%2Feurario%3Alatest-blue?logo=docker)](https://hub.docker.com/r/carlorigoni/eurario)
[![FET Solver](https://img.shields.io/badge/FET%20engine-C%2B%2B%20native-orange.svg)](https://lalescu.ro/liviu/fet/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-green.svg)](https://www.gnu.org/licenses/agpl-3.0)

> 🔗 **GitHub Repository:** [github.com/carlorigoni/eurario](https://github.com/carlorigoni/eurario)

Eurario is an open-source timetabling suite for secondary schools, integrated with the high-performance native C++ **FET (Free Timetabling Software)** solver.

Zero external Python dependencies, a responsive Material 3 interface, and ready-to-run multi-arch container images on Docker Hub.

---

## 🌟 Key Features

- **Integrated FET Heuristic Solver**:
  - Real-time solving with live SSE log streaming and bottleneck activity tracking.
  - Automatic saving and one-click recovery of the highest partial solve stage on timeout.
- **Activity Locking System**:
  - Lock entire classes or single lesson hours onto the timetable grid with permanent 100% hard constraints (`ConstraintActivityPreferredStartingTime` and `ConstraintActivityPreferredRoom`).
- **Complete Institutional Management**:
  - **Teachers**: target hours, contracts (full-time, split COE, fractional, part-time), gaps, max daily hours, preferences, and contractual day off.
  - **Classes & Groups**: split groups for foreign languages (e.g., French, Spanish) and technical specialties.
  - **Classrooms & Shared Facilities**: home rooms, shared gyms with capacity checks, and specialized laboratories.
  - **Macro-Subjects & Merges**: combine related teaching loads for balanced pedagogical distribution.
  - **Automated Standby Periods**: dedicated algorithm to fill idle gaps and balance substitute coverage.
- **Word (.docx) & Excel Roster Synchronization**:
  - Direct download of official Word template or export of current staff assignments.
  - Automated sync with Diff Viewer preview before applying updates.
- **Pre-filled Demo Dataset ("School of Athens")**:
  - Comes with a complete, fully solved school dataset to test all features immediately.
  - Clean slate reset feature to create a new empty institution.
- **Lightweight Architecture**:
  - Runs on Python 3.10+ using only standard library modules.

---

## 🐳 Official Docker Hub Image

Eurario is published as an official pre-built container image:

👉 **Docker Hub Repository:** [`carlorigoni/eurario`](https://hub.docker.com/r/carlorigoni/eurario)

No need to install C++ compilers or desktop GUI libraries on the host.

---

## 🚀 Quick Start with Docker Compose

1. Create a `docker-compose.yml` file:
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

2. Start the container:
   ```bash
   docker compose up -d
   ```

3. Open your browser:
   👉 **`http://localhost:8000`**

---

## 📄 License

Released under the [GNU Affero General Public License v3 (AGPLv3)](https://www.gnu.org/licenses/agpl-3.0).
