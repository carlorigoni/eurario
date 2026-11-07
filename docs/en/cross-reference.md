---
title: Parameters & FET Cross-Reference
description: Comprehensive technical mapping between Eurario educational settings and compiled native FET XML tags conforming to ASD-STE100 standards.
---

# 🔬 Cross-Reference: Eurario Settings & FET XML Constraints

The Eurario solving engine is powered by the official high-performance **FET** (*Free Timetabling Software*) binary.

This reference document defines the technical mapping between educational parameters configured in Eurario and their compiled FET XML tags ([Official FET Manual](https://www.timetabling.de/manual/FET-manual.en.html)).

---

## 1. Fundamental Entity Mapping

| Eurario Concept | FET XML Tag | Description and Operational Scope |
| :--- | :--- | :--- |
| **Teacher** | `<Teacher>` | Identified uniquely by name. Holds competition code (CDC) and contract hours in comments. |
| **Standard Class** | `<Year>` | Student cohort (e.g., `1A`, `3B`, `5CSA`). Represents top-level student grouping in FET. |
| **Track / Split Group** | `<Group>` | Class subdivision sharing common subjects but splitting for track-specific courses (e.g., `3A_INFO`, `3A_TEL`). |
| **Language / Lab Group** | `<Subgroup>` | Smallest atomic student unit used for half-class divisions (e.g., `1A_FRA`, `1A_SPA`). |
| **Subject** | `<Subject>` | Curriculum course. Short codes (`short_name`) appear in printed reports; full names go to FET. |
| **Teaching Load** | Group of `<Activity>` | Each teaching load decomposes into sub-activities linked by the same `<Activity_Group_Id>`. |
| **School Building** | `<Building>` | Physical school facility or campus (e.g., *Main Campus*, *Branch Campus*). |
| **Classroom / Lab** | `<Room>` | Physical room assigned to a `<Building>` with a maximum `<Capacity>`. |

---

## 2. Teacher Time Constraints (`Time_Constraints_List`)

### A. Contractual Day Off & Unavailability Hours
* **Eurario Interface**: *Teachers* tab &rarr; Weekly clickable matrix (days × periods).
* **FET XML Tag**: `<ConstraintTeacherNotAvailableTimes>`
* **Generated XML**:
  ```xml
  <ConstraintTeacherNotAvailableTimes>
    <Weight_Percentage>100</Weight_Percentage>
    <Teacher_Name>Rossi Mario</Teacher_Name>
    <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
    <Not_Available_Time>
      <Day>Sat</Day>
      <Hour>1</Hour>
    </Not_Available_Time>
    <!-- periods 1 to 6 for Saturday off -->
  </ConstraintTeacherNotAvailableTimes>
  ```
* **Effect**: Hard constraint (100% weight). FET strictly forbids lessons in selected slots.

### B. Minimum & Maximum Working Days Per Week
* **Eurario Interface**: Teacher modal &rarr; *Working days per week* (`min_days` and `max_days`).
* **FET XML Tags**:
  * `<ConstraintTeacherMaxDaysPerWeek>`
  * `<ConstraintTeacherMinDaysPerWeek>`
* **Generated XML**:
  ```xml
  <ConstraintTeacherMaxDaysPerWeek>
    <Weight_Percentage>100</Weight_Percentage>
    <Teacher_Name>Bianchi Laura</Teacher_Name>
    <Max_Days_Per_Week>4</Max_Days_Per_Week>
  </ConstraintTeacherMaxDaysPerWeek>
  <ConstraintTeacherMinDaysPerWeek>
    <Weight_Percentage>100</Weight_Percentage>
    <Teacher_Name>Bianchi Laura</Teacher_Name>
    <Min_Days_Per_Week>3</Min_Days_Per_Week>
  </ConstraintTeacherMinDaysPerWeek>
  ```
* **Effect**: Essential for part-time schedules and preventing isolated one-hour working days.

### C. Idle Windows (Daily and Weekly Gaps)
* **Eurario Interface**: Institute Settings &rarr; *Max gaps per day* and *Max gaps per week*.
* **FET XML Tags**:
  * `<ConstraintTeacherMaxGapsPerDay>` (Weight 95-100%)
  * `<ConstraintTeacherMaxGapsPerWeek>` (Weight 95-100%)
* **Generated XML**:
  ```xml
  <ConstraintTeacherMaxGapsPerDay>
    <Weight_Percentage>98</Weight_Percentage>
    <Teacher_Name>Verdi Giuseppe</Teacher_Name>
    <Max_Gaps>1</Max_Gaps>
  </ConstraintTeacherMaxGapsPerDay>
  <ConstraintTeacherMaxGapsPerWeek>
    <Weight_Percentage>95</Weight_Percentage>
    <Teacher_Name>Verdi Giuseppe</Teacher_Name>
    <Max_Gaps>2</Max_Gaps>
  </ConstraintTeacherMaxGapsPerWeek>
  ```

### D. Daily Teaching Hour Limits
* **Eurario Interface**: Timetable Settings &rarr; *Maximum daily teaching hours* and *Minimum daily teaching hours*.
* **FET XML Tags**:
  * `<ConstraintTeacherMaxHoursDaily>`: Limits daily load (e.g., max 4 or 5 hours).
  * `<ConstraintTeacherMinHoursDaily>`: Requires minimum load on active working days (e.g., min 2 hours).
  * `<ConstraintTeacherMaxSpanPerDay>`: Limits total span from first to last period of the day.

---

## 3. Student & Class Time Constraints

### A. Compact Student Schedules (Zero Idle Gaps)
* **Eurario Interface**: Permanently enabled for all student cohorts.
* **FET XML Tags**:
  * `<ConstraintStudentsMaxGapsPerDay>`: `<Max_Gaps>0</Max_Gaps>` (Weight 100%)
  * `<ConstraintStudentsMaxGapsPerWeek>`: `<Max_Gaps>0</Max_Gaps>` (Weight 100%)
* **Effect**: Eliminates unsupervised idle periods between lessons for students.

### B. Late Starts at Second Period
* **Eurario Interface**: Institute Settings &rarr; *Max late starts at second period*.
* **FET XML Tag**: `<ConstraintStudentsEarlyMaxBeginningsAtSecondHour>`
* **Generated XML**:
  ```xml
  <ConstraintStudentsEarlyMaxBeginningsAtSecondHour>
    <Weight_Percentage>100</Weight_Percentage>
    <Max_Beginnings_At_Second_Hour>0</Max_Beginnings_At_Second_Hour>
  </ConstraintStudentsEarlyMaxBeginningsAtSecondHour>
  ```
* **Effect**: When set to 0, enforces that classes start at the first period every morning.

### C. Break Times & School Recess
* **Eurario Interface**: Timetable Settings &rarr; *Break Times*.
* **FET XML Tag**: `<ConstraintBreakTimes>`
* **Effect**: Blocks lesson scheduling during official school recess periods.

---

## 4. Subject Constraints & Hour Block Distribution

### A. Spacing Between Lessons of the Same Subject
* **Eurario Interface**: Generated automatically for decomposed teaching loads (e.g., `2+1+1`).
* **FET XML Tag**: `<ConstraintMinDaysBetweenActivities>`
* **Generated XML**:
  ```xml
  <ConstraintMinDaysBetweenActivities>
    <Weight_Percentage>98</Weight_Percentage>
    <Consecutive_If_Same_Day>true</Consecutive_If_Same_Day>
    <Number_of_Activities>3</Number_of_Activities>
    <Activity_Id>101</Activity_Id>
    <Activity_Id>102</Activity_Id>
    <Activity_Id>103</Activity_Id>
    <MinDays>1</MinDays>
  </ConstraintMinDaysBetweenActivities>
  ```
* **Effect**: Distributes blocks across different days. If scheduled on the same day, forces them to be consecutive (`Consecutive_If_Same_Day=true`).

### B. Preferred Time Slots (Early / Late Hours)
* **Eurario Interface**: Subject Modal &rarr; *Preferred Time Slot* (`EARLY`, `LATE`, `ANY`).
* **FET XML Tag**: `<ConstraintActivitiesPreferredTimeSlots>`
* **Effect**:
  * `EARLY`: Gives weight priority to periods 1, 2, and 3 (written tests, math).
  * `LATE`: Gives weight priority to periods 4, 5, and afternoon sessions (gym, art).

### C. Exclude Afternoon Sessions (`no_rientri`)
* **Eurario Interface**: Subject Modal &rarr; *Exclude from Afternoon Sessions*.
* **FET XML Tag**: `<ConstraintActivitiesPreferredTimeSlots>` with 100% negative weight on afternoon periods.

### D. Manually Locked Activities (`Lock`)
* **Eurario Interface**: Padlock icon `🔒` on the lesson card.
* **FET XML Tag**: `<ConstraintActivityPreferredStartingTime>` (Hard 100%). Permanently locks day and starting period.

### E. End-of-Day Activities
* **Eurario Interface**: Teaching Load Settings &rarr; *Place at End of Day*.
* **FET XML Tag**: `<ConstraintActivityEndsStudentsDay>`
* **Effect**: Schedules the activity during the last period of the day for clean early dismissals.

### F. Sequential Lesson Coupling (Theory + Lab)
* **Eurario Interface**: Teaching Load Modal &rarr; *Direct Sequential Coupling*.
* **FET XML Tag**: `<ConstraintTwoActivitiesConsecutive>`
* **Generated XML**:
  ```xml
  <ConstraintTwoActivitiesConsecutive>
    <Weight_Percentage>100</Weight_Percentage>
    <First_Activity_Id>101</First_Activity_Id>
    <Second_Activity_Id>102</Second_Activity_Id>
    <Active>true</Active>
  </ConstraintTwoActivitiesConsecutive>
  ```
* **Effect**: Forces the second activity to run immediately after the first activity on the same day.

### G. Parallel Time Synchronization for Option Tracks
* **Eurario Interface**: Split Group Modal &rarr; *Synchronize Start Time*.
* **FET XML Tag**: `<ConstraintActivitySameStartingTime>`
* **Generated XML**:
  ```xml
  <ConstraintActivitySameStartingTime>
    <Weight_Percentage>100</Weight_Percentage>
    <First_Activity_Id>201</First_Activity_Id>
    <Second_Activity_Id>202</Second_Activity_Id>
    <Active>true</Active>
  </ConstraintActivitySameStartingTime>
  ```
* **Effect**: Locks parallel split activities (e.g., French and Spanish) to the exact same hour slot.

### H. Minimum Overnight Rest Period
* **Eurario Interface**: Teacher Settings &rarr; *Minimum Overnight Rest Period*.
* **FET XML Tag**: `<ConstraintTeacherMinRestingHours>`
* **Effect**: Prevents a teacher ending an evening course at 22:00 from being scheduled at 08:00 the following morning.

---

## 5. Spatial & Multi-Campus Constraints (`Space_Constraints_List`)

### A. Class Base Classroom (Home Room)
* **Eurario Interface**: Class Modal &rarr; *Home Room*.
* **FET XML Tag**: `<ConstraintStudentsSetHomeRoom>`
* **Generated XML**:
  ```xml
  <ConstraintStudentsSetHomeRoom>
    <Weight_Percentage>100</Weight_Percentage>
    <Students>3A</Students>
    <Room>Room 204</Room>
  </ConstraintStudentsSetHomeRoom>
  ```

### B. Shared Labs & Gymnasiums
* **Eurario Interface**: Teaching Load Assignment &rarr; *Lab / Gymnasium*.
* **FET XML Tag**: `<ConstraintActivityPreferredRooms>`
* **Generated XML**:
  ```xml
  <ConstraintActivityPreferredRooms>
    <Weight_Percentage>100</Weight_Percentage>
    <Activity_Id>205</Activity_Id>
    <Number_of_Preferred_Rooms>1</Number_of_Preferred_Rooms>
    <Preferred_Room>Computer_Lab_1</Preferred_Room>
  </ConstraintActivityPreferredRooms>
  ```

### C. Teacher Commute Across Campuses
* **Eurario Interface**: Campus Settings.
* **FET XML Tags**:
  1. `<ConstraintTeachersMaxBuildingChangesPerDay>`: Limits daily campus changes (default max 1).
  2. `<ConstraintTeachersMaxBuildingChangesPerWeek>`: Limits weekly campus changes (default max 2 or 3).
  3. `<ConstraintTeachersMinGapsBetweenBuildingChanges>`: Enforces travel gap time between lessons in different campuses.

### D. Classroom Stability for Back-to-Back Lessons
* **Eurario Interface**: Room Settings &rarr; *Same Room for Back-to-Back Hours*.
* **FET XML Tag**: `<ConstraintActivitiesSameRoomIfConsecutive>`
* **Effect**: Keeps students and teachers in the same classroom during consecutive periods of the same course.

---

## 6. Comparison: Official FET Desktop vs Eurario Suite

<div class="doc-figure">
  <img src="../assets/fet-interfaccia.png" alt="Official FET solver desktop interface" class="doc-screenshot">
  <div class="doc-caption">Figure 4.1: Official FET desktop interface with time and space constraint configuration menus.</div>
</div>

| Feature | FET Desktop GUI | Eurario Suite |
| :--- | :--- | :--- |
| **Teaching Loads** | Fragmented isolated sub-activity list | Unified teacher and class cards with didactic blocks |
| **Multi-Campus** | Generic textual alerts | Color-coded building badges with automated travel gap enforcement |
| **Substitute Standby Periods** | Not supported natively | Dedicated heuristic algorithm for gap filling and balanced standby coverage |
| **Post-Solve Adjustments** | Full recalculation required | Interactive Drag & Drop board with live clash verification |
| **Official Printouts** | Basic raw HTML tables | Ministerial Word (.docx A3 landscape) and pastel PDF schedules |
