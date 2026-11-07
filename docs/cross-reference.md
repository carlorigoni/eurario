---
title: Parametri & Cross-Reference FET
description: Tavola comparativa tecnica tra le impostazioni didattiche di Eurario e i tag XML generati per il motore solutore nativo FET secondo standard ASD-STE100.
---

# 🔬 Cross-Reference: Parametri Eurario & Vincoli XML FET

Il motore solutore di Eurario utilizza il binario nativo **FET** (*Free Timetabling Software*).

Questa pagina descrive la corrispondenza tecnica tra i parametri configurati nell'interfaccia di Eurario e i relativi tag XML generati per FET ([Manuale Ufficiale FET](https://www.timetabling.de/manual/FET-manual.en.html)).

---

## 1. Mappatura Entità Fondamentali

| Concetto in Eurario | Tag XML FET | Descrizione e Utilizzo |
| :--- | :--- | :--- |
| **Docente** | `<Teacher>` | Identificato univocamente dal nome. Contiene la classe di concorso e il monte ore nei commenti. |
| **Classe Ordinaria** | `<Year>` | Rappresenta la coorte degli studenti (es. `1A`, `3B`, `5CSA`). È il gruppo studenti di livello superiore. |
| **Indirizzo / Articolazione** | `<Group>` | Sottogruppo di una classe che condivide lezioni comuni e si separa per indirizzi specifici (es. `3A_INFO`, `3A_TEL`). |
| **Gruppo Linguistico / Laboratorio** | `<Subgroup>` | Unità minima usata per divisioni a metà classe (es. `1A_FRA`, `1A_SPA`). |
| **Materia Scolastica** | `<Subject>` | Disciplina curricolare. La sigla `short_name` compare nelle stampe; FET riceve il nome completo. |
| **Cattedra Didattica** | Gruppo `<Activity>` | Ciascuna cattedra viene scomposta in attività collegate dal medesimo `<Activity_Group_Id>`. |
| **Plesso Scolastico** | `<Building>` | Edificio fisico dell'istituto (es. *Sede Centrale*, *Succursale*). |
| **Aula / Laboratorio** | `<Room>` | Spazio fisico associato a un `<Building>` con capienza massima `<Capacity>`. |

---

## 2. Vincoli Temporali Docenti (`Time_Constraints_List`)

### A. Giorno Libero Contrattuale & Indisponibilità Orarie
* **Interfaccia Eurario**: Scheda *Docenti* &rarr; Matrice settimanale cliccabile (giorni × ore).
* **Tag XML FET**: `<ConstraintTeacherNotAvailableTimes>`
* **Codice XML Generato**:
  ```xml
  <ConstraintTeacherNotAvailableTimes>
    <Weight_Percentage>100</Weight_Percentage>
    <Teacher_Name>Rossi Mario</Teacher_Name>
    <Number_of_Not_Available_Times>6</Number_of_Not_Available_Times>
    <Not_Available_Time>
      <Day>Sab</Day>
      <Hour>1</Hour>
    </Not_Available_Time>
    <!-- ore da 1 a 6 per il sabato libero -->
  </ConstraintTeacherNotAvailableTimes>
  ```
* **Effetto**: Vincolo rigido (*Hard 100%*). FET esclude tassativamente lezioni in quegli slot.

### B. Giorni Massimi e Minimi di Servizio a Settimana
* **Interfaccia Eurario**: Modale Docente &rarr; *Giorni di presenza settimanali* (`min_days` e `max_days`).
* **Tag XML FET**:
  * `<ConstraintTeacherMaxDaysPerWeek>`
  * `<ConstraintTeacherMinDaysPerWeek>`
* **Codice XML Generato**:
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
* **Effetto**: Obbligatorio per part-time verticali ed eliminazione di giorni con una sola ora frammentata.

### C. Finestre Libere (Ore Buche Giornaliere e Settimanali)
* **Interfaccia Eurario**: Impostazioni Istituto &rarr; *Max buchi al giorno* e *Max buchi alla settimana*.
* **Tag XML FET**:
  * `<ConstraintTeacherMaxGapsPerDay>` (Peso 95-100%)
  * `<ConstraintTeacherMaxGapsPerWeek>` (Peso 95-100%)
* **Codice XML Generato**:
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

### D. Limite Ore Giornaliere di Lezione
* **Interfaccia Eurario**: Impostazioni Orario &rarr; *Massimo ore al giorno* e *Minimo ore al giorno*.
* **Tag XML FET**:
  * `<ConstraintTeacherMaxHoursDaily>`: Limita il carico didattico giornaliero (es. max 4 o 5 ore).
  * `<ConstraintTeacherMinHoursDaily>`: Impone un minimo di ore nei giorni lavorativi (es. min 2 ore).
  * `<ConstraintTeacherMaxSpanPerDay>`: Limita l'ampiezza dell'orario giornaliero (dalla prima all'ultima ora).

---

## 3. Vincoli Temporali Studenti & Classi

### A. Compattezza Orario Studenti (Zero Ore Buche)
* **Interfaccia Eurario**: Attivo in modo permanente per tutte le classi.
* **Tag XML FET**:
  * `<ConstraintStudentsMaxGapsPerDay>`: `<Max_Gaps>0</Max_Gaps>` (Peso 100%)
  * `<ConstraintStudentsMaxGapsPerWeek>`: `<Max_Gaps>0</Max_Gaps>` (Peso 100%)
* **Effetto**: Impedisce finestre vuote tra le lezioni degli studenti.

### B. Ingressi Posticipati alla Seconda Ora
* **Interfaccia Eurario**: Impostazioni Istituto &rarr; *Massimo ingressi alla seconda ora*.
* **Tag XML FET**: `<ConstraintStudentsEarlyMaxBeginningsAtSecondHour>`
* **Codice XML Generato**:
  ```xml
  <ConstraintStudentsEarlyMaxBeginningsAtSecondHour>
    <Weight_Percentage>100</Weight_Percentage>
    <Max_Beginnings_At_Second_Hour>0</Max_Beginnings_At_Second_Hour>
  </ConstraintStudentsEarlyMaxBeginningsAtSecondHour>
  ```
* **Effetto**: Con valore 0, tutte le classi iniziano le lezioni alla prima ora del mattino.

### C. Pause Didattiche e Intervallo
* **Interfaccia Eurario**: Impostazioni Orario &rarr; *Intervallo Ricreazione*.
* **Tag XML FET**: `<ConstraintBreakTimes>`
* **Effetto**: Blocca la collocazione di lezioni durante l'intervallo deliberate dal collegio.

---

## 4. Vincoli sulle Discipline & Suddivisione Cattedre

### A. Distanziamento tra Lezioni della Stessa Materia
* **Interfaccia Eurario**: Calcolato automaticamente per cattedre con blocchi orari (es. `2+1+1`).
* **Tag XML FET**: `<ConstraintMinDaysBetweenActivities>`
* **Codice XML Generato**:
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
* **Effetto**: Colloca i blocchi in giorni diversi. Se collocati nello stesso giorno, impone la consecutività (`Consecutive_If_Same_Day=true`).

### B. Fascia Oraria Preferita (Prime / Ultime Ore)
* **Interfaccia Eurario**: Modale Materia &rarr; *Fascia Oraria Preferita* (`PRIME`, `ULTIME`, `INDIFFERENTE`).
* **Tag XML FET**: `<ConstraintActivitiesPreferredTimeSlots>`
* **Effetto**:
  * `PRIME`: Assegna priorità alle ore 1, 2 e 3 (verifiche scritte, matematica).
  * `ULTIME`: Assegna priorità alle ore 4, 5 e pomeridiane (educazione motoria, arte).

### C. Esclusione Rientri Pomeridiani (`no_rientri`)
* **Interfaccia Eurario**: Modale Materia &rarr; *Escludi dai Rientri Pomeridiani*.
* **Tag XML FET**: `<ConstraintActivitiesPreferredTimeSlots>` impostato con divieto assoluto sulle ore pomeridiane (7ª e 8ª ora).

### D. Attività Bloccate Manualmente (`Lock`)
* **Interfaccia Eurario**: Icona Lucchetto `🔒` sulla scheda dell'attività.
* **Tag XML FET**: `<ConstraintActivityPreferredStartingTime>` (Hard 100%). Fissa in modo inamovibile giorno e ora di inizio.

### E. Attività a Termine Giornata
* **Interfaccia Eurario**: Impostazioni Cattedra &rarr; *Colloca a Fine Giornata*.
* **Tag XML FET**: `<ConstraintActivityEndsStudentsDay>`
* **Effetto**: Colloca l'attività nell'ultima ora della giornata per consentire uscite anticipate senza generare ore buche.

### F. Consecutività Didattica (Teoria + Laboratorio)
* **Interfaccia Eurario**: Modale Cattedra &rarr; *Lega in Consecutività Diretta*.
* **Tag XML FET**: `<ConstraintTwoActivitiesConsecutive>`
* **Codice XML Generato**:
  ```xml
  <ConstraintTwoActivitiesConsecutive>
    <Weight_Percentage>100</Weight_Percentage>
    <First_Activity_Id>101</First_Activity_Id>
    <Second_Activity_Id>102</Second_Activity_Id>
    <Active>true</Active>
  </ConstraintTwoActivitiesConsecutive>
  ```
* **Effetto**: La seconda attività si svolge nello stesso giorno nell'ora immediatamente successiva alla prima.

### G. Sincronizzazione Oraria per Opzioni & Articolazioni
* **Interfaccia Eurario**: Modale Articolazione &rarr; *Sincronizza Orario di Inizio*.
* **Tag XML FET**: `<ConstraintActivitySameStartingTime>`
* **Codice XML Generato**:
  ```xml
  <ConstraintActivitySameStartingTime>
    <Weight_Percentage>100</Weight_Percentage>
    <First_Activity_Id>201</First_Activity_Id>
    <Second_Activity_Id>202</Second_Activity_Id>
    <Active>true</Active>
  </ConstraintActivitySameStartingTime>
  ```
* **Effetto**: Sincronizza l'inizio di due attività parallele (es. Francese e Spagnolo) nella stessa classe.

### H. Riposo Notturno Minimo (Serale & Diurno)
* **Interfaccia Eurario**: Scheda Docente &rarr; *Intervallo Minimo di Riposo Notturno*.
* **Tag XML FET**: `<ConstraintTeacherMinRestingHours>`
* **Effetto**: Impedisce che un docente con lezioni serali fino alle 22:00 sia assegnato alla prima ora del mattino seguente.

---

## 5. Vincoli Spaziali & Multi-Plesso (`Space_Constraints_List`)

### A. Aula Base della Classe (Home Room)
* **Interfaccia Eurario**: Modale Classe &rarr; *Aula Base*.
* **Tag XML FET**: `<ConstraintStudentsSetHomeRoom>`
* **Codice XML Generato**:
  ```xml
  <ConstraintStudentsSetHomeRoom>
    <Weight_Percentage>100</Weight_Percentage>
    <Students>3A</Students>
    <Room>Aula 204</Room>
  </ConstraintStudentsSetHomeRoom>
  ```

### B. Laboratori & Palestre Condivise
* **Interfaccia Eurario**: Assegnazione Cattedra &rarr; *Laboratorio / Palestra*.
* **Tag XML FET**: `<ConstraintActivityPreferredRooms>`
* **Codice XML Generato**:
  ```xml
  <ConstraintActivityPreferredRooms>
    <Weight_Percentage>100</Weight_Percentage>
    <Activity_Id>205</Activity_Id>
    <Number_of_Preferred_Rooms>1</Number_of_Preferred_Rooms>
    <Preferred_Room>Lab_Informatica_1</Preferred_Room>
  </ConstraintActivityPreferredRooms>
  ```

### C. Spostamento Docenti tra Plessi
* **Interfaccia Eurario**: Impostazioni Plessi & Sedi.
* **Tag XML FET**:
  1. `<ConstraintTeachersMaxBuildingChangesPerDay>`: Limita i cambi plesso nello stesso giorno (default max 1).
  2. `<ConstraintTeachersMaxBuildingChangesPerWeek>`: Limita i cambi plesso settimanali (default max 2 o 3).
  3. `<ConstraintTeachersMinGapsBetweenBuildingChanges>`: Impone un intervallo vuoto minimo tra plessi per il tempo di viaggio.

### D. Stabilità d'Aula per Ore Consecutive
* **Interfaccia Eurario**: Impostazioni Aule &rarr; *Stessa Aula se Ore Consecutive*.
* **Tag XML FET**: `<ConstraintActivitiesSameRoomIfConsecutive>`
* **Effetto**: Mantiene studenti e docenti nella stessa stanza se svolgono lezioni consecutive della stessa disciplina.

---

## 6. Confronto: FET Nativo vs Eurario

<div class="doc-figure">
  <img src="assets/fet-interfaccia.png" alt="Interfaccia grafica ufficiale del motore solutore FET" class="doc-screenshot">
  <div class="doc-caption">Figura 4.1: Interfaccia desktop ufficiale di FET con gestione vincoli temporali e spaziali.</div>
</div>

| Funzionalità | Interfaccia Grafica Desktop FET | Suite Eurario |
| :--- | :--- | :--- |
| **Rappresentazione Cattedre** | Elenco frammentato in sotto-attività isolate | Visualizzazione unificata per docente e classe con blocchi didattici |
| **Multi-Plesso** | Avvisi testuali generici | Badge colorati per plesso e calcolo automatico tempi di viaggio |
| **Disposizioni & Supplenze** | Non supportate nativamente | Algoritmo proprietario di riempimento buchi e bilanciamento |
| **Modifiche Post-Calcolo** | Ricalcolo completo obbligatorio | Griglia interattiva Drag & Drop con controllo collisioni in tempo reale |
| **Esportazione Finale** | Tabelle HTML di base | Word (.docx) A3 Orizzontale ministeriale e PDF tipografici |
