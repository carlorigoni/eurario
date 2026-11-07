---
title: General Overview
description: Official technical and operational documentation for Eurario, an open-source timetabling suite powered by the FET heuristic solver according to ASD-STE100 standards.
---

# 🎓 Eurario — Official Documentation

Welcome to the documentation for **Eurario**, the open-source suite designed to build, solve, optimize, and publish school timetables for secondary schools.

Eurario pairs a responsive Material Design 3 web client with the official native **FET** (*Free Timetabling Software*) heuristic engine developed by Liviu Lalescu and Volker Dirr.

---

## 🧭 Documentation Map

<div class="eurario-card-grid">
  <a href="getting-started/" class="eurario-card">
    <h3>🚀 Getting Started & Master Data</h3>
    <p>Google Workspace authentication, multi-school management, teachers, classes, subjects, rooms, and campuses.</p>
  </a>

  <a href="user-guide/" class="eurario-card">
    <h3>📖 User Guide & Use Cases</h3>
    <p>Step-by-step operational guide in 14 chronological phases and 10 concrete use cases with interface screenshots.</p>
  </a>

  <a href="timetable-flow/" class="eurario-card">
    <h3>⚡ Generation & Optimization Flow</h3>
    <p>Teaching loads, didactic block decomposition, asynchronous FET solver, Relaxation Engine, and standby periods.</p>
  </a>

  <a href="cross-reference/" class="eurario-card">
    <h3>🔬 Parameters & FET Cross-Reference</h3>
    <p>Comprehensive mapping table between Eurario settings and compiled native C++ FET XML tags.</p>
  </a>

  <a href="docker-deploy/" class="eurario-card">
    <h3>🐳 Docker Installation & Deployment</h3>
    <p>Deployment on Linux x86/ARM servers, Docker Compose recipes, Nginx, Caddy, and Cloudflare Tunnel.</p>
  </a>

  <a href="architecture/" class="eurario-card">
    <h3>🏗️ Architecture & DevOps</h3>
    <p>GitHub and Docker Hub CI/CD pipelines, semantic versioning, and zero-downtime production upgrades.</p>
  </a>
</div>

---

## 🏛️ System Architecture

Eurario uses a containerized modular architecture without external Python dependencies:

```mermaid
graph TB
    subgraph Frontend["Web Client (Modern Browser)"]
        UI["Reactive SPA Interface\n(HTML5 / CSS3 / Vanilla JS)"]
        LiveSSE["Solver Log Streaming\n(Server-Sent Events)"]
        DnD["Interactive Timetable Grid\n(Drag & Drop Standby Hours & Blocks)"]
    end

    subgraph Backend["Eurario Core Engine (Python 3.10+)"]
        Server["Multi-Thread Async HTTP Server"]
        Auth["RBAC Access Control & Google OAuth 2.0"]
        DB["Isolated Multi-Tenant JSON Database\n(Optimistic Concurrency Control OCC)"]
        FETGen["FET XML Compiler & Generator"]
        Diag["Relaxation Engine & Conflict Resolver"]
        DispAlgo["Standby Hours Balancing Algorithm (D)"]
        PrintEng["Typography Engine Word (.docx A3) & PDF"]
    end

    subgraph NativeCore["Native Heuristic Solver"]
        FETCL["Native fet-cl Binary Process (C++)"]
    end

    subgraph Storage["Persistent Storage (/app/data)"]
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
    DB <-->|"Atomic File I/O & Lock"| Storage
    Server -->|"Compile complete dataset"| FETGen
    FETGen -->|".fet file on disk"| Storage
    Server -->|"Spawn async subprocess"| FETCL
    FETCL -->|"Live stdout/stderr stream"| Server
    FETCL -->|"Write solved timetable"| Storage
    Server -->|"On mathematical deadlock"| Diag
    Server -->|"Fill gaps & substitute periods"| DispAlgo
```

---

## 🌟 Key Features & Contractual Compliance

Eurario is built to satisfy educational constraints and Italian collective bargaining agreements (CCNL Scuola):

### 1. Teacher Contract Safeguards
* **Standard Loads (18 hours)**, **Part-time** (2 to 5 working days), and **Fractional loads**.
* **External Split Appointments (COE)**: Automatically deducts external days and hours from the weekly internal schedule.
* **Contractual Day Off**: Protected by a 100% hard constraint in the FET solver.
* **Idle Window Limits**: Strict daily (e.g., max 1) and weekly (e.g., max 2) gap limits.
* **Minimum Daily Hours**: Enforces a minimum load per active day (e.g., min 2 hours) to avoid inefficient one-hour trips.

### 2. Curriculum & Split Cohorts
* **Automatic Didactic Block Split**: Decomposes total subject hours into optimal blocks (`2+1+1` for 4 hours, `2+1` for 3 hours, `2+2+1+1` for 6 hours).
* **Macro-Subjects & Subject Merges**: Combines related subjects taught by the same teacher (e.g., *Math & Physics*).
* **Split Groups & Tracks**: Native support for language tracks (*French / Spanish*) and vocational specialties.
* **Preferred Time Slots**: Prioritizes early morning periods (*EARLY*) or afternoon periods (*LATE*).
* **Afternoon Block Exclusion**: Prohibits scheduling specified academic subjects during afternoon periods.

### 3. Multi-Campus Logistics & Shared Facilities
* **Main & Branch Campuses**: Manages road travel times and limits daily campus changes for traveling teachers.
* **Campus TimeMachine**: Hour-by-hour visual simulator with subway-style teacher commute routes.
* **Gymnasiums & Labs**: Tracks facility capacities to prevent room clashing.

### 4. Standby Periods & Substitution Coverage ("D")
* **Balancing Algorithm**: Assigns standby periods to close idle gaps and balance cover hours across every period.
* **Hourly Density Badges (`👥 X D`)**: Displays real-time counts of available standby teachers per period.
* **Drag & Drop Grid**: Allows manual fine-tuning with instant constraint checks.

### 5. Document Exports
* **Master Teacher Timetable Word (.docx A3 Landscape)**: Complies with official ministerial layouts with repeating header rows.
* **Student Class Schedules PDF**: High-contrast pastel palettes or monochrome toner-save output.
* **Optimistic Concurrency Control (OCC)**: Prevents accidental data overwrites when multiple committee members work concurrently.

---

## 🖥️ User Interface

<div class="doc-figure">
  <img src="../assets/eurario-cattedre.png" alt="Eurario — Teaching Loads and Assignments" class="doc-screenshot">
  <div class="doc-caption">Figure 1.1: Teaching loads management interface with automated didactic block breakdown.</div>
</div>

---

## 📜 License & Project Credits

Eurario is open-source software released under the **GNU Affero General Public License v3 (AGPLv3)**.

* **Development & Architecture**: [Carlo Rigoni](https://github.com/carlorigoni)
* **Methodological Guidance**: Federico Rettore
* **FET Solver Engine**: Liviu Lalescu and Volker Dirr ([FET Official Website](https://lalescu.ro/liviu/fet/))
* **Official GitHub Repository**: [github.com/carlorigoni/eurario](https://github.com/carlorigoni/eurario)
