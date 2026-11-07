---
title: User Guide & Real-World Use Cases
description: Step-by-step comprehensive operational user guide conforming to ASD-STE100 principles for secondary school timetabling committees.
---

# 📖 Comprehensive User Guide & Real-World Use Cases

Drafting secondary school timetables requires balancing contractual requirements, educational goals, and physical facility limits. This guide provides direct, action-oriented instructions following Simplified Technical English (ASD-STE100) principles.

All screenshots in this guide use the educational demo dataset **Scuola di Atene** (School of Athens).

---

## 🗺️ End-to-End Operational Workflow

```mermaid
flowchart TD
    F1["1. Time Parameters\n(Days, Hours, Recesses)"] --> F2["2. Ingest Staffing (Organico)\n(Excel / Word .docx)"]
    F2 --> F3["3. Facilities, Buildings & Rooms\n(Labs, Gyms, Campuses)"]
    F3 --> F4["4. Classes & Articulated Groups\n(Language splits, Specializations)"]
    F4 --> F5["5. Assignments & Pedagogical Blocks\n(Co-teaching, Merged Subjects)"]
    F5 --> F6["6. Teacher Rules & Availability\n(Part-time, Shared COE, Day Off)"]
    F6 --> F7["7. Mathematical Solving with FET\n(Live SSE progress streaming)"]
    F7 -->|"If timetable is over-constrained"| F8["8. Diagnostic Relaxation Engine\n(Isolates exact conflict)"]
    F7 -->|"Solution found"| F9["9. On-Duty Balancing Algorithm (D)\n(Plugs gaps & balances substitutes)"]
    F8 --> F5
    F9 --> F10["10. Drag & Drop Refinement & Snapshots"]
    F10 --> F11["11. TimeMachine Simulation\n(Spatiotemporal flows & itinerant faculty)"]
    F11 --> F12["12. Typographic Word (.docx A3) & PDF Export"]
```

<img src="../assets/eurario-dashboard.png" alt="Eurario — Control Dashboard (School of Athens)" class="doc-screenshot">

---

### Step 1: Institutional Time Grid Setup & Parameters

**Purpose:** Configure the weekly grid structure, bell periods, and academic year dates before adding staff or classes.

1. Open **Timetable Settings** (or the **Parameters** view).
2. Select **School Days**:
   * Choose *5-Day Week* (Monday–Friday).
   * Or choose *6-Day Week* (Monday–Saturday).
3. Set **Daily Lesson Periods** (e.g., 6 regular periods: 08:00–14:00).
4. Enable **Afternoon Sessions** (Periods 7 and 8) if required by the curriculum.
5. Set the **School Recess** period (e.g., after Period 3) to apply the institutional break.
6. Set the **Validity Start Date** and **School Year End Date** (defaults to June 8th): this parameter controls weekly recurrence in generated teacher `.ics` files.

<img src="../assets/eurario-parametri.png" alt="Eurario — Comprehensive Educational and Institutional Parameters" class="doc-screenshot">

---

### Step 2: Staffing Ingestion, Snapshots & Version History

**Purpose:** Ingest teacher assignments from external files and manage timetable rollback snapshots.

1. Open **Snapshots & Staffing**.
2. Click **Upload Staffing File** to select an Excel (`.xlsx`), CSV, or official Word (`.docx`) file.
3. Review the Visual Diff modal:
   * 🟢 **Green**: New teachers or course allocations.
   * 🟡 **Yellow**: Allocations with modified weekly hours.
   * 🔴 **Red**: Removed allocations.
4. Click **Apply Changes with Snapshot**. The system creates a rollback checkpoint before updating data.
5. In **Snapshot Management**, browse version history, export the underlying `.fet` file, or restore an earlier milestone with one click.

<img src="../assets/eurario-snapshots.png" alt="Eurario — Snapshot Management and Version Rollback" class="doc-screenshot">

---

### Step 3: Physical Facilities & Campus Logistics

**Purpose:** Register campuses, classrooms, and specialized labs with logistic limits.

1. Register **Campus Buildings**:
   * Create campuses (e.g., *Main Campus* and *Branch Annex*).
   * Set road travel time between locations (e.g., 15 minutes).
2. Add **Standard Classrooms** and assign each room to its campus building.
3. Add **Specialized Facilities** (gymnasiums, computer labs, science labs).
4. Enable the **Lab or Gym** flag (`is_lab_or_gym`) for resources shared across cohorts.

<img src="../assets/eurario-spazi.png" alt="Eurario — Facilities and Rooms Management" class="doc-screenshot">

---

### Step 4: Classes, Tracks & Articulated Groups

**Purpose:** Create student cohorts and configure elective or language splits.

1. Register regular classes (e.g., `1A`, `2B`, `3CSA`).
2. Enter student headcount to validate room seating capacity.
3. Select the **Home Room** permanently assigned to each class.
4. For articulated groups (e.g., foreign language splits), switch to the **Articulated Groups** subview.
5. Create linked sub-entities (`3A_FRA`, `3A_SPA`) and assign dedicated rooms or laboratories.

<img src="../assets/eurario-classi.png" alt="Eurario — Classes and Articulated Groups" class="doc-screenshot">

<img src="../assets/eurario-gruppi-articolati.png" alt="Eurario — Articulated Language and Elective Groups" class="doc-screenshot">

---

### Step 5: Allocations, Subjects, Pedagogical Blocks & Merging

**Purpose:** Connect teachers, subjects, and classes, defining weekly lesson blocks and color codes.

1. **Subject Management**: Open the **Subjects** view to configure the pastel palette and concise print abbreviations (`short_name`).
2. **Assign Allocations**: Assign the teacher, class, subject, and weekly hours to each allocation.
3. **Block Splitting Rules**: In **Block Rules**, verify automatic pedagogical splitting (`2+1+1` for 4 hours, `2+2+1+1` for 6 hours, single `2` block for gym).
4. **Subject Merging**: Open **Merging Rules** to merge related disciplines taught by the same teacher (e.g., *Math & Physics* 7h $\rightarrow$ `2+2+2+1`).

<img src="../assets/eurario-materie.png" alt="Eurario — Subjects and Didactic Color Palettes" class="doc-screenshot">

<img src="../assets/eurario-cattedre.png" alt="Eurario — Teaching Assignments and Curriculum Blocks" class="doc-screenshot">

<img src="../assets/eurario-regole-blocchi.png" alt="Eurario — Automatic Block Splitting Rules" class="doc-screenshot">

<img src="../assets/eurario-accorpamenti.png" alt="Eurario — Subject Merging Module" class="doc-screenshot">

---

### Step 6: Teacher Contractual Constraints, Availability & Privacy

**Purpose:** Configure contractual hours, days off, shift preferences, faculty-wide availability, and private calendar feeds.

1. Verify contractual target hours (`target_hours`: 18h full-time, or reduced for part-time).
2. Set minimum and maximum active teaching days (`min_days` and `max_days`).
3. In the **weekly availability grid**, click to mark unavailabilities and contractual days off in red.
4. Open **Faculty Availability Board** to inspect a synoptic master grid of all staff availabilities and days off.
5. For shared faculty, enable the **COE** toggle and enter external school hours.
6. In the teacher modal, inspect the **Private Calendar Feed & Cryptographic Token** panel to copy the link or revoke/regenerate the security key.

<img src="../assets/eurario-docenti.png" alt="Eurario — Faculty Roster and Contractual Hours" class="doc-screenshot">

<img src="../assets/eurario-modale-docente.png" alt="Eurario — Teacher Parameters, Shift Preferences, and Private Calendar Token" class="doc-screenshot">

<img src="../assets/eurario-disponibilita-collegio.png" alt="Eurario — Faculty-Wide Weekly Availability Master Matrix" class="doc-screenshot">

---

### Step 7: Mathematical Timetable Solving with FET & Advanced Constraints

**Purpose:** Configure advanced constraints and execute algorithmic solving.

1. Open **Advanced Constraints** to configure:
   * Maximum consecutive teaching hours (e.g., 4 periods).
   * Maximum daily or weekly gaps/windows.
   * Campus transit pause rules and total daily span.
2. Open **Timetable Solver**.
3. Set the desired timeout limit (e.g., 300 seconds or unlimited).
4. Click **Start FET Solver**.
5. Monitor live progress and conflict reports streamed via Server-Sent Events (SSE).
6. Stop execution at any time to save the best partial schedule (*highest stage*).

<img src="../assets/eurario-vincoli-avanzati.png" alt="Eurario — Advanced FET Timetabling Constraints" class="doc-screenshot">

<img src="../assets/eurario-solver.png" alt="Eurario — Real-Time FET Solver Live Dashboard" class="doc-screenshot">

<img src="../assets/eurario-attivita.png" alt="Eurario — Didactic Activities and FET Constraints" class="doc-screenshot">

---

### Step 8: Conflict Diagnosis with the Relaxation Engine

**Purpose:** Isolate conflicting rules when a schedule is mathematically unsolvable.

1. When the solver stops without finding a complete solution, open **Diagnostics & Relaxation Engine**.
2. Read the hierarchical conflict level (Level 1: total hours, Level 2: facilities, Level 3: gaps and active days, Level 4: soft preferences).
3. Review the analytic bottleneck report identifying the exact teachers and classes involved in deadlock.
4. Apply the recommended minimal adjustment and re-run the FET solver.

<img src="../assets/eurario-diagnostica.png" alt="Eurario — 4-Level Relaxation Engine Diagnostic Conflict Report" class="doc-screenshot">

---

### Step 9: Smart On-Duty Placement & Monitoring ("D")

**Purpose:** Place on-duty reserve hours to plug schedule gaps and guarantee substitute coverage.

1. Click **Place On-Duty Automatically**. The algorithm fills gaps and balances substitution readiness.
2. Monitor density badges (`👥 X D`) displayed in every empty timetable cell:
   * **`0 D` (Gray)**: Zero teachers on duty (critical unstaffed period).
   * **`1-2 D` (Green)**: Optimal substitute coverage.
   * **`3+ D` (Purple)**: High density of reserve staff.
3. Click **📊 On-Duty Board** to open the full weekly reserve matrix.
4. Click any teacher chip to jump directly to their individual schedule.

<img src="../assets/eurario-disposizioni.png" alt="Eurario — Institute-Wide On-Duty Reserve Board" class="doc-screenshot">

---

### Step 10: Interactive Drag & Drop Refinement & Timetable Board

**Purpose:** Manually reposition periods, inspect multiple views (Teachers, Classes, Rooms), lock verified assignments, and access export options.

1. Open the **Solved Timetable** view.
2. Toggle between three master viewports:
   * **👨‍🏫 Teachers**: Individual teacher schedules with on-duty hours and quick export buttons.
   * **🎓 Classes**: Cohort schedule with room assignments and articulated subgroups.
   * **🏫 Rooms & Labs**: Facility utilization matrix to monitor occupancy and saturation.
3. Drag and drop any lesson card to change its time or room.
4. Click the lock icon (`🔒`) to **permanently pin** an activity (`locked="true"`). Pinned lessons show a thicker blue border and remain untouched during solver recalculations.
5. Use header toolbar actions:
   * **🖨️ Print**: View the printable A4 sheet.
   * **📄 PDF**: Download vector A4 printable timetable.
   * **📅 iCal (.ics)**: Download RFC 5545 iCalendar file.
   * **➕ Google Calendar**: Subscribe to the schedule in Google Calendar with 1 click.
   * **📧 Email Timetable**: Open the individual delivery modal.

<img src="../assets/eurario-tabellone.png" alt="Eurario — Solved Master Timetable Board (Teachers View)" class="doc-screenshot">

<img src="../assets/eurario-tabellone-classi.png" alt="Eurario — Solved Master Timetable Board (Classes View)" class="doc-screenshot">

<img src="../assets/eurario-tabellone-aule.png" alt="Eurario — Solved Master Timetable Board (Rooms & Labs View)" class="doc-screenshot">

---

### Step 11: Spatiotemporal Validation with Campus TimeMachine

**Purpose:** Verify physical student flows and travel comfort for itinerant faculty.

1. Open **⏳ TimeMachine Plessi**.
2. Use keyboard arrow keys or click **▶ Play** to simulate the school day period by period.
3. Check the **Transit Highway**: ensure traveling teachers have an intermediate gap or recess between campuses (flags red ⚠️ *Consecutive Periods*).
4. Review **🌅 Off-Site Start** badges for classes starting at a secondary facility.
5. Click **🚇 Metro Map** to inspect weekly journeys for itinerant teachers.

<img src="../assets/eurario-timemachine.png" alt="Eurario — Campus TimeMachine and Travel Flow Simulation" class="doc-screenshot">

<img src="../assets/eurario-timemachine-metro.png" alt="Eurario — TimeMachine Itinerant Faculty Metro Map" class="doc-screenshot">

---

### Step 12: Official Word (.docx) & PDF Export

**Purpose:** Produce formal documentation for noticeboards, staff, and classes.

1. Click **🖨️ Print Classes (PDF)** to open the Procedure 9 generator (A4 Landscape per-class layout with articulated classes and toner-save option).
2. Click **📄 Faculty Board (A3)** to open the Procedure 12 generator (master faculty grid in A3 Landscape Word/PDF with repeating headers).
3. Click **🚗 Transfers (Noticeboard)** to print the campus travel roster for itinerant teachers.

<img src="../assets/eurario-modale-stampa-classi.png" alt="Eurario — Procedure 9 Class Timetable PDF Print Generator" class="doc-screenshot">

<img src="../assets/eurario-modale-stampa-docenti.png" alt="Eurario — Procedure 12 Master Faculty Board A3 Print Generator" class="doc-screenshot">

<img src="../assets/eurario-modale-stampa-spostamenti.png" alt="Eurario — Campus Travel Noticeboard Print Generator" class="doc-screenshot">

---

### Step 13: Faculty Timetable Email Delivery & Calendar Sync (Google & iCal)

**Purpose:** Deliver individual timetables directly to each teacher under strict Zero-Comparison privacy.

1. **Targeted Email Delivery**:
   * Each teacher receives **strictly their own personal schedule** in the email body.
   * Send to individual staff members, selected cohorts, or the entire school.
2. **Administrator Test Delivery**:
   * Send a test message to your admin address to inspect layout, styling, and SMTP delivery before bulk mailing.
3. **Official A4 Landscape Vector PDF Attachment**:
   * Each email attaches `Orario_{Surname_Name}.pdf` ready for printing.
4. **Weekly Recurring iCalendar (.ics) Attachment**:
   * Each email attaches `Orario_{Surname_Name}.ics` conforming to RFC 5545 with weekly recurrence until the end of the school year (configurable parameter, defaults to June 8th).
5. **1-Click Synchronization (Google Calendar / Apple / Outlook)**:
   * Click **➕ Add to Google Calendar** in the email to subscribe immediately.
   * Click **🍏 Apple Calendar / Outlook (Webcal)** to sync iOS, macOS, and Outlook.
6. **Cryptographic Feed Privacy Protection**:
   * Each calendar subscription URL includes an unguessable 128-bit secret token (`?token=...`).
   * Unauthorized requests without a valid token are rejected with **`403 Forbidden`**.
   * Administrators can view the private feed URL and regenerate keys in the teacher profile.

<img src="../assets/eurario-email-modal.png" alt="Eurario — Individual Timetable Email Delivery Modal with Privacy Protection" class="doc-screenshot">

---

### Step 14: Security, User Roles & SMTP Server Configuration

**Purpose:** Manage access permissions, inspect live audit trails, and configure outbound email delivery.

1. Open **Access Management** from the top bar or administration settings.
2. **Roles & Permissions**: Manage user accounts (*Superadmin, School Admin, Timetable Editor, Read-Only Viewer*).
3. **Live Access Audit Log**: Review sign-in history, client IP addresses, and database changes in real time.
4. **SMTP Configuration**: Switch to **Mail Server (SMTP)** to set school credentials (Host, Port, STARTTLS/SSL, User, and App Password).
5. Send an integrated test email to verify server connectivity before emailing faculty timetables.

<img src="../assets/eurario-modale-gestione-accessi.png" alt="Eurario — Access Management, User Roles, and Audit Log" class="doc-screenshot">

<img src="../assets/eurario-modale-configurazione-smtp.png" alt="Eurario — Outgoing SMTP Mail Server Configuration and Test" class="doc-screenshot">

---
   * Administrators can view the private feed URL and regenerate the cryptographic token in the teacher edit modal, immediately revoking outdated links.

---

### Cross-Functional Productivity & Support Tools

#### 1. Global Multi-Subject Filter in Topbar
Located in the main application topbar, this dropdown lets you filter the entire workspace by one or more disciplines:
* **Multi-Selection with Instant Search**: Check off multiple subjects simultaneously (e.g., *Mathematics* and *Physics*, or all foreign languages).
* **Persistent Workspace Filter**: Remains active across the *Chairs*, *Activities*, and *Solved Timetable* views, isolating relevant teachers and classes.
* **Quick Actions**: One-click *Select All* and *Deselect All* with live selection counters on the topbar chip.

#### 2. Co-Teaching & Labs with Independent Subjects
In vocational and technical schools featuring shared laboratory sessions:
* **Independent Subjects for Each Teacher**: The theoretical instructor and the technical lab teacher (ITP) can be assigned to the same activity with distinct subject names (e.g., *Computer Science* and *Computer Science Lab*).
* **Uncompromised Contract Accounting**: Each teacher's official curriculum assignment is preserved accurately in timetables and statutory exports.

#### 3. "Contact Administrator" Support Channel
Accessible directly from the topbar, footer, and login screen:
* **Integrated Inquiries & Feedback**: Enables teachers, timetablers, and coordinators to submit schedule change requests, bug reports, or suggestions directly to the school timetable administrator.

---

## 💼 In-Depth Real-World Use Cases (Secondary School & Official FET Manual)

Before examining specific scenarios, it is essential to understand the **algorithmic architecture and philosophy** established in the [Official FET Manual](https://www.timetabling.de/manual/FET-manual.en.html), which is seamlessly embedded within Eurario's solving engine.

### 🧠 The Three Algorithmic Pillars of the Official FET Manual

#### 1. "The Golden Rule" and Incremental Generation
School timetabling is a known NP-complete mathematical problem. The single most common mistake made by timetabling committees is loading 100% of all constraints, individual preferences, and soft teacher requests on the very first solving attempt. When the calculation fails to converge, isolating which exact rule or combination caused the bottleneck becomes nearly impossible.
* **Phase A (Structural Baseline 100%)**: Input strictly non-negotiable entities: Days, Hours, Classes, Teachers, Curricular allocations, Hard unavailabilities (statutory days off, part-time schedules), and Mandatory room reservations (specialized labs and gymnasiums). Verify that this baseline converges within seconds. If it fails, an inescapable arithmetic flaw exists in your staffing allocations (e.g., total assigned hours exceed available time slots).
* **Phase B (Pedagogical Quality & Well-Being)**: Introduce distribution constraints across the week (`Min days between activities`), teacher continuous teaching limits (`Max hours continuously`), and weekly free period caps (`Max gaps per week`).
* **Phase C (Soft Optimization & Desiderata)**: Layer in subjective preferences (requested early departures or late arrivals), room nomadism caps, and specialized group syncs.

#### 2. Constraint Weight Mechanics ($0.0\% - 100.0\%$)
Every constraint in the FET engine carries a percentage weight property (`Weight_Percentage`):
* **Hard Constraints (100% Weight)**: Non-negotiable mandatory rules. FET's search heuristic will never accept a timetable that violates even a single 100% constraint. If two 100% rules contradict each other, the algorithm will loop indefinitely in mathematical deadlock.
* **Soft Constraints (Weights such as 85%, 95%, 99%)**: Qualitative preferences. During recursive heuristic swapping, FET is permitted to temporarily and locally violate a soft rule to complete the placement of remaining assignments. A constraint set to 98% or 99% often allows FET to find an outstanding pedagogical timetable in seconds, whereas a rigid 100% would cause a complete standstill.

#### 3. Mathematical Deadlock Isolation
As emphasized by FET creators Liviu Lalescu and Volker Dirr, solving failures are never random: they stem from circular over-constrained models. Eurario includes an automated **Relaxation Engine** that systematically deactivates soft rules and parses conflict traces to pinpoint the exact teachers, classes, or rooms causing the impasse.

---

### Use Case 1: Teacher on External Shared Schedule (COE)
* **Scenario**: Dr. Marco Bianchi (Math & Physics) has an 18-hour contract: **12 hours** at your campus and **6 external hours** at a neighboring school 25 km away, scheduled on **Tuesday and Thursday**.
* **Configuration in Eurario**:
  1. Set `target_hours: 18`.
  2. Toggle **External Shared Schedule (COE)** on.
  3. Enter `External Hours: 6`. Eurario verifies that exactly $18 - 6 = 12$ internal hours must be allocated.
  4. In the weekly availability grid, mark all periods on **Tuesday** and **Thursday** in red (unavailable).
  5. Set `max_days: 3` (Monday, Wednesday, Friday).
* **FET Solver Result**: FET translates this into `<ConstraintTeacherNotAvailableTimes>` at 100% weight for Tuesday and Thursday and places the 12 internal hours strictly across the remaining 3 days.

---

### Use Case 2: Vertical Part-Time Teacher (10 Hours over 3 Days)
* **Scenario**: Prof. Laura Conti teaches Literature on a 10-hour part-time contract, with a formal agreement to work on **at most 3 days per week**. She teaches two classes: 6 hours and 4 hours.
* **Configuration in Eurario**:
  1. Set `target_hours: 10`, `contract_type: part-time`.
  2. Set `max_days: 3` and `min_days: 3`.
  3. Configure blocks:
     * 6-hour allocation: `2+2+2` (instead of `2+2+1+1`, which would require 4 days).
     * 4-hour allocation: `2+2` (instead of `2+1+1`, which would require 3 days).
  4. Eurario's `check_cattedra_feasibility` confirms that the sub-activities can fit comfortably inside 3 days.
* **FET Solver Result**: FET compiles `<ConstraintTeacherMaxDaysPerWeek>3</ConstraintTeacherMaxDaysPerWeek>` and schedules the 10 hours across exactly 3 days.

---

### Use Case 3: Merged Composite Curriculum (Math & Physics 7 Hours)
* **Scenario**: In senior science tracks (class 3B), a single teacher is allocated **4 hours of Mathematics** and **3 hours of Physics**. Handling them independently creates competing day-spacing constraints.
* **Configuration in Eurario**:
  1. Open **Merging Rules** and click **Find Candidates**.
  2. The system detects the shared instructor for both disciplines in class 3B.
  3. Click **Apply Merge**:
     * Eurario creates a 7-hour unified allocation with optimized block splitting `2+2+2+1`.
     * It distributes the lessons across 4 or 5 days of the week.
  4. On official printed outputs, compact codes (`MATH`, `PHYS`) ensure every period is clearly and accurately designated.

---

### Use Case 4: Articulated Foreign Language Split (French & Spanish)
* **Scenario**: In class 2A, 14 students study French (Prof. Dubois) and 12 students study Spanish (Prof. Martinez). Both groups must have their 3 weekly hours simultaneously in separate rooms.
* **Configuration in Eurario**:
  1. Under **Classes & Groups**, select class `2A` and click **Add Articulation**:
     * Subgroup `2A_FRA` (14 students), preferred room: `Room 105`.
     * Subgroup `2A_SPA` (12 students), preferred room: `Language Lab`.
  2. Assign French 3h (`2+1`) to `2A_FRA`.
  3. Assign Spanish 3h (`2+1`) to `2A_SPA`.
* **FET Solver Result**: FET groups the activities (`ConstraintTwoActivitiesGrouped`), ensuring both subgroups are taught at the exact same periods without schedule collisions for the parent class.

---

### Use Case 5: Co-Teaching in Specialized Labs (Theory + Lab Instructor)
* **Scenario**: In 4th-year Computer Science, *Systems & Networks* (4 hours/week) requires 2 consecutive hours of co-teaching with the theoretical instructor (Prof. Verdi) and the practical lab assistant (Prof. Neri) in the *Networking Lab*.
* **Configuration in Eurario**:
  1. Create a 2-hour regular allocation (`1+1`) for Prof. Verdi in the standard classroom.
  2. Create a second 2-hour block (`2`) selecting **both teachers** simultaneously in the teacher dropdown.
  3. Assign the mandatory room `Networking Lab`.
* **FET Solver Result**: FET compiles a single activity with both `<Teacher>Verdi</Teacher>` and `<Teacher>Neri</Teacher>`, locking them to the same period in the designated lab.

---

### Use Case 6: Multi-Campus Commute with Travel Time (Main & Branch)
* **Scenario**: A high school operates a Main Campus and a Branch Campus located 4 km apart (approx. 20 minutes travel time). 6 teachers teach classes at both sites.
* **Configuration in Eurario**:
  1. In **Buildings**, register `Main` and `Branch`.
  2. Set `Travel Time: 20 min` and `Max Building Changes per Day: 1`.
  3. Assign each student class to its home building.
* **FET Solver Result**: FET enforces:
  * `<ConstraintTeachersMaxBuildingChangesPerDay>`: Caps campus changes to at most 1 per day.
  * `<ConstraintTeachersMinGapsBetweenBuildingChanges>`: Guarantees a mandatory free hour between classes held at different sites for safe travel.

---

### Use Case 7: Shared Gymnasiums & Capacity-Constrained Facilities
* **Scenario**: The school has a single large gymnasium that can host at most 2 classes simultaneously (separated by a dividing curtain), offering 40 available periods per week. The school has 24 classes (each requiring 2 hours of PE = 48 total hours).
* **Configuration in Eurario**:
  1. Register two rooms: `Gym Court A` and `Gym Court B` (capacity: 30 students each).
  2. For each class PE allocation (block `2`), select both `Gym Court A` and `Gym Court B` as allowed rooms.
  3. Eurario's capacity calculator verifies feasibility: $48 \text{ hours required} \le 60 \text{ hours capacity}$, confirming a comfortable 20% margin.
* **FET Solver Result**: FET places classes across both courts (`ConstraintActivityPreferredRooms`) without ever exceeding the 2-class concurrent ceiling.

---

### Use Case 8: Deadlock Resolution via the Relaxation Engine
* **Scenario**: When running FET, the solver reaches 94% of activities but gets stuck in a mathematical deadlock (*Over-constrained Timetable*).
* **Diagnosis in Eurario**:
  1. Open the **Relaxation Engine** report.
  2. The diagnostic engine identifies:
     > *"Conflict located at Level 3 (Teacher Gaps and Working Days): Prof. Ferrari has 18 hours across 4 classes, a day off on Friday, and a strict limit of 1 gap hour per week. However, two of his assigned classes have no periods on Monday due to afternoon sessions."*
  3. **Remedy**: Temporarily increase Prof. Ferrari's weekly gap allowance to 2 hours or shift his day off to Thursday.
  4. Re-running the solver finds an optimal schedule in 35 seconds.

---

### Use Case 9: Optimized On-Duty Hour Placement ("D")
* **Scenario**: Prof. Alberto Galli teaches 15 curricular hours. Under his 18-hour contract, he owes **3 on-duty reserve hours** for substitutions and student supervision.
* **Configuration in Eurario**:
  1. With the solved curricular timetable displayed, click **Place On-Duty Automatically**.
  2. Eurario's greedy heuristic:
     * Identifies a gap at period 3 on Tuesday (between periods 2 and 4): places the first on-duty hour there, eliminating the gap.
     * Appends the second hour at period 5 on Wednesday following his classes.
     * Places the third hour at period 1 on Friday to reinforce morning entrance coverage.
  3. The administration designates Friday's hour for lab coordination: type *"Computer Lab Support"* in the custom label (`custom_desc`).
  4. Click the lock icon: the slot is permanently pinned (`locked`) against future recalculations.

---

### Use Case 10: Preliminary vs Final Timetable Transitions via Snapshots
* **Scenario**: In mid-September, the school opens with a **preliminary 4-period day** while temporary substitute teachers are being assigned. In mid-October, the school transitions to the **official 6-period permanent schedule**.
* **Configuration in Eurario**:
  1. **Preliminary Setup**: Set 4 periods per day, exclude unfilled assignments, and run FET.
  2. Click **Create Snapshot** and label it *"2026_09_Preliminary_4h"*.
  3. Download the generated `.fet` file as a timestamped backup.
  4. **Transition to Permanent Schedule**:
     * Extend the school day to 6 periods (plus afternoon returns).
     * Input the finalized permanent staff appointments.
     * Run the FET solver for the complete master schedule.
     * Save the snapshot *"2026_10_Official_Permanent"*.
  5. If unforeseen disruptions occur, you can revert to the preliminary schedule with a single click.

---

### Use Case 11: Fortnightly / Alternating Week Classes (Asymmetric Curricula)
* **FET Manual Reference**: Section *Add a fortnightly activity*.
* **Scenario**: In 9th and 10th grades, *Design & Technology* requires 1 regular weekly lecture in standard classrooms and 1 computer lab session taught once every two weeks (Week A / Week B), amounting to an average of 1.5 hours per week or 1 hour bi-weekly.
* **The Two Official FET Workarounds**:
  1. **Solution 1 (Recommended Edge Placement)**: Add the fortnightly lesson as a standard weekly activity, but lock it to the boundary of the students' school day:
     * Apply `<ConstraintActivityEndsStudentsDay>` or set an early-period time preference.
     * This ensures that during the off-week when the lesson does not meet, students never suffer an empty idle period in the middle of their day; they simply arrive one period later or dismiss one period earlier.
  2. **Solution 2 (Paired Mirror Scheduling)**: If two different fortnightly subjects (e.g., *CAD Drafting* and *Applied Chemistry*) or two separate cohorts (e.g., Class 1A and Class 1B) share the same lab:
     * Unify them into a single joint FET activity scheduled weekly in the exact same time slot and room.
     * Noticeboards and syllabus sheets specify that Week A attends Subject 1 while Week B attends Subject 2, guaranteeing 100% room and instructor utilization with zero vacant timetable slots.

---

### Use Case 12: Pedagogical Ordering & Consecutiveness: Theory & Laboratory
* **FET Manual Reference**: Sections *Two activities are consecutive*, *Activities are grouped*, *Two activities are ordered*.
* **Scenario**: In 11th Grade Electronics, a 4-hour course consists of 2 theoretical lecture hours and 2 hands-on laboratory hours with a technical co-teacher. The department requires tight pedagogical coordination between both components.
* **The 3 FET Modeling Rules**:
  * **Consecutive Activities (`Two activities are consecutive`)**:
    * Forces both activities onto the **same day, immediately back-to-back**, without any idle gap or intervening subject (recess is permitted).
    * Best used for: Classroom theory directly succeeded by practical lab execution on the same morning.
  * **Grouped Activities (`Activities are grouped`)**:
    * Forces both activities onto the same day without gaps, **but the execution order is flexible** (lab can precede or follow theory).
    * *FET Manual Tip*: This rule is far less restrictive than rigid consecutiveness and vastly speeds up solver convergence while preventing room-hopping.
  * **Ordered Activities Across the Week (`Two activities are ordered`)**:
    * Strictly mandates that Activity 1 (e.g., Monday/Tuesday lecture) must precede Activity 2 (Thursday/Friday exercise) across the calendar week.
    * *Warning from FET Authors*: Volker Dirr cautions against over-using this rule. If Activity 1 is cancelled due to a Monday bank holiday, teacher illness, or an assembly, the planned sequence breaks down. Use only when pedagogically essential.

---

### Use Case 13: Nighttime Rest Protection Across Day and Evening Programs
* **FET Manual Reference**: Section *Min resting hours*.
* **Scenario**: A comprehensive institute operates both standard daytime classes ($08:00 - 14:00$) and evening adult diploma programs ($17:30 - 22:00$). Several teachers hold mixed dual-track assignments. If an instructor finishes at 22:00 on Monday evening and is scheduled for period 1 at 08:00 on Tuesday morning, the overnight rest window is under 10 hours, violating labor regulations.
* **Configuration in Eurario**:
  1. Open the Teacher modal and enable **Minimum Overnight Rest**.
  2. Set `Min Resting Hours: 11` (or 12 hours).
  3. Alternatively, apply interval caps: if an instructor teaches in the late evening block ($19:00 - 22:00$) on Day $N$, they cannot teach in the early morning block ($08:00 - 10:00$) on Day $N+1$.
* **FET Compilation**: FET generates `<ConstraintTeacherMinRestingHours>` at 100% weight: whenever the teacher is placed in the final evening period, FET categorically forbids assignments in periods 1 and 2 the next morning, delaying their arrival to period 3 ($10:00$).

---

### Use Case 14: Pseudo-Activities for Faculty Meetings, Councils and Cafeteria
* **FET Manual Reference**: Sections *Pseudo activities*, *Not available teachers, students or rooms & breaks*.
* **Scenario**:
  1. *Department Meetings*: On Thursday at period 6, all 12 STEM faculty members must be freed from class instruction to hold their curriculum alignment assembly.
  2. *Staggered Cafeteria Lunch*: In extended-day technical high schools, students require a guaranteed lunch period at period 5 or 6 without overcrowding the dining hall.
* **Configuration in Eurario**:
  * **Department Meeting (Teachers without students)**:
    * Create a synthetic "pseudo-activity" listing all 12 participating faculty members, **leaving the student set empty**.
    * Label the subject *STEM Department Meeting* and set an exact time lock on Thursday period 6 (`ConstraintActivityPreferredStartingTime`) at 100% weight. FET marks all 12 teachers as actively occupied, ensuring no class lessons are booked during that hour.
  * **Cafeteria Lunch (Students without teachers)**:
    * *Global Recess Approach*: If all students dine simultaneously, apply `<ConstraintBreakTimes>`.
    * *Staggered Pseudo-Activity*: If grade 9 dines during period 5 and grade 11 dines during period 6, create student-only activities with the room assigned to *Cafeteria Refectory*.

---

### Use Case 15: Student Room Nomadism and Classroom Stability
* **FET Manual Reference**: Sections *Home room(s)*, *Preferred room(s)*, *A set of activities occupies max different rooms*, *A set of activities are in the same room if they are consecutive*.
* **Scenario**: In facilities with tight physical space, students frequently face changing rooms 4 or 5 times a day ("room nomadism"), leading to hall congestion, lost instructional minutes, and logistical disorder.
* **Configuration in Eurario**:
  1. **Home Rooms**: Designate a permanent home base for each class (e.g., Class 1A &rarr; *Room 204*). All standard lectures default here automatically.
  2. **Preferred Specialized Rooms**: Restrict room mobility exclusively to disciplines requiring physical apparatus:
     * Physical Education &rarr; *Gymnasium*.
     * Chemistry & Biology &rarr; *Science Lab*.
     * Computer Science &rarr; *Multimedia Lab*.
  3. **Room Stability for Consecutive Lessons**: Enable *Same room if consecutive* (`ConstraintActivitiesSameRoomIfConsecutive`). When a class or teacher has two successive periods, room transitions are strictly prohibited.
  4. **Daily Room Change Cap**: Enforce `<ConstraintStudentsSetMaxDifferentRoomsPerDay>` with a maximum value of 2 rooms per day (the home room plus at most one lab/gym rotation).

---

### Use Case 16: Mid-Year Timetable Adjustments and Activity Locking
* **FET Manual Reference**: Sections *Before changing a running timetable*, *Changing a running timetable*.
* **Scenario**: In November, two months into the academic year, a Humanities teacher commences maternity leave. A replacement teacher is hired with a statutory day off on Friday. The committee must adjust the schedule without upsetting the daily routines of hundreds of students, families, and colleagues.
* **Protected Recalculation Flow in Eurario**:
  1. **Freeze Existing Stable Schedules (Locking)**:
     * Click **Lock All Current Activities** (`locked="true"` on every timetable cell except the target maternity assignment).
     * FET treats all 800 pre-existing class periods as unchangeable constants.
  2. **Audit Newly Arrived Constraints**:
     * As Volker Dirr highlights: *"Never focus solely on the departed teacher; audit the new arrival's real-world constraints"*. Enter the replacement teacher's availability and day-off rules.
  3. **Targeted Relaxation**:
     * If the new teacher's rules conflict with the prior schedule, unlock only the assignments across the 3 specific classes taught by that teacher, keeping the other 95% of the school completely frozen.
  4. **Surgical Resolving**:
     * Run the FET solver: the engine recalculates the local permutation in under 2 seconds, guaranteeing zero collateral disruption across unaffected classes.

---

### Use Case 17: Gap Taxonomy and Equitable Free Period Distribution
* **FET Manual Reference**: Section *Teachers' Free Periods*.
* **Scenario**: Teacher dissatisfaction often centers on uneven free period allocations, where some staff have compact schedules while others endure multiple disconnected gaps.
* **Official FET Gap Taxonomy in Eurario**:
  * **Single Gap**: An isolated 1-hour opening between lessons (e.g., teaching periods 1, 3, and 4, with period 2 free). *Eurario Strategy*: This is optimal for automated On-Duty ("D") assignment, immediately plugging dead time with compensated reserve supervision.
  * **Border Gaps**: Delayed arrivals (period 2 start) or early departures (period 4 dismissal). *Eurario Strategy*: Regarded as favorable for staff; Eurario balances early-arrival mornings across departments to ensure fairness.
  * **Big Gaps**: Multi-hour idle blocks (e.g., teaching period 1, then periods 5 and 6). *Eurario Strategy*: Highly undesirable. Eurario enforces `<ConstraintTeacherMaxGapsPerDay>1</ConstraintTeacherMaxGapsPerDay>` and heavily penalizes multi-hour gaps to eliminate Big Gaps campus-wide.

---

### Use Case 18: Maximum Simultaneous Activities on Shared Resources
* **FET Manual Reference**: Section *Max simultaneous activities from a set in selected time slots*.
* **Scenario**:
  1. *Divided Sports Complex*: A large fieldhouse can safely host at most 3 class groups simultaneously under local fire code regulations.
  2. *Off-Campus Field Visits*: To prevent security bottlenecks at school gates, the administration mandates that no more than 2 senior classes may conduct off-campus museum or library visits at the same time.
* **Configuration in Eurario**:
  1. Label target activities with a shared **Activity Tag** (e.g., `SPORTS_FACILITY` or `EXTERNAL_VISIT`).
  2. In Resource Constraints, configure:
     * Tag: `SPORTS_FACILITY`.
     * Maximum Simultaneous Limit: `3`.
* **FET Compilation**: FET generates `<ConstraintActivitiesMaxSimultaneousInSelectedTimeSlots>`: for every single weekly period, the engine verifies that the active count of tagged lessons is $\le 3$, guaranteeing safety and preventing resource contention.

---

## 💡 Operational Best Practices for Timetable Committees

1. **Iterative Approximation**: Never apply all soft preferences simultaneously on the first run. Always verify baseline mathematical feasibility using only hard constraints (days off, room limits, total hours).
2. **Watch for Competing Days Off**: Avoid assigning multiple teachers of the same class a day off on the same day, especially in full-time cohorts with 30–32 weekly periods.
3. **Always Set Short Print Abbreviations (`short_name`)**: Configure concise acronyms (e.g., `LAW` for *Economics & Business Law*) to keep official Word (.docx) A3 tables compact and readable.
4. **Snapshot Every Major Milestone**: Save a named snapshot before applying major bulk updates (organico import, subject merging, teacher schedule changes).
