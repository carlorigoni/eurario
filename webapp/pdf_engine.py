"""
Eurario - Native Pure-Python Vector PDF & iCalendar Engine
Generatore di documenti PDF vettoriali ad alta risoluzione (PDF 1.4)
e calendari standard iCalendar (.ics RFC 5545) per docenti.
Zero dipendenze esterne: sfrutta solo la libreria standard di Python.
"""

import math
import re
from datetime import datetime, timedelta
from webapp.print_engine import ORARIO_ORE, INTERVALLI_DOPO_ORA, build_subject_color_map, get_day_name, get_default_validity_date

def _hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip("#")
    if len(hex_code) == 3:
        hex_code = "".join(2 * c for c in hex_code)
    try:
        r = int(hex_code[0:2], 16) / 255.0
        g = int(hex_code[2:4], 16) / 255.0
        b = int(hex_code[4:6], 16) / 255.0
        return (r, g, b)
    except Exception:
        return (0.95, 0.95, 0.95)

def _pdf_escape(text):
    if text is None:
        return b"()"
    if not isinstance(text, str):
        text = str(text)
    # Codifica in Windows-1252 (WinAnsiEncoding) per supporto accenti italiani (è, é, à, ò, ù, °, ª)
    try:
        raw_bytes = text.encode("cp1252", errors="replace")
    except Exception:
        raw_bytes = text.encode("latin1", errors="replace")
    out = []
    for b in raw_bytes:
        if b in (ord(b"("), ord(b")"), ord(b"\\")):
            out.append(b"\\" + bytes([b]))
        elif b < 32 or b == 127:
            out.append(f"\\{b:03o}".encode("ascii"))
        else:
            out.append(bytes([b]))
    return b"(" + b"".join(out) + b")"

class PDFCanvas:
    """Canvas vettoriale 2D per emissione comandi PDF 1.4 su A4 Landscape."""
    def __init__(self, width=841.89, height=595.28):
        self.width = width
        self.height = height
        self.ops = []

    def save_state(self):
        self.ops.append(b"q")

    def restore_state(self):
        self.ops.append(b"Q")

    def set_stroke_color(self, r, g, b):
        self.ops.append(f"{r:.3f} {g:.3f} {b:.3f} RG".encode("ascii"))

    def set_fill_color(self, r, g, b):
        self.ops.append(f"{r:.3f} {g:.3f} {b:.3f} rg".encode("ascii"))

    def set_line_width(self, w):
        self.ops.append(f"{w:.2f} w".encode("ascii"))

    def rect(self, x, y, w, h, fill=True, stroke=True):
        self.ops.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re".encode("ascii"))
        if fill and stroke:
            self.ops.append(b"B")
        elif fill:
            self.ops.append(b"f")
        elif stroke:
            self.ops.append(b"S")

    def line(self, x1, y1, x2, y2):
        self.ops.append(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S".encode("ascii"))

    def get_text_width(self, text, font="F1", size=10):
        if not text:
            return 0.0
        bold_factor = 1.12 if font == "F2" else 1.0
        w = 0.0
        for ch in text:
            if ch in "ijl|!.,:;' ":
                w += 0.28 * size * bold_factor
            elif ch in "mwMW_@#%":
                w += 0.82 * size * bold_factor
            elif ch.isupper() or ch in "0123456789":
                w += 0.62 * size * bold_factor
            else:
                w += 0.52 * size * bold_factor
        return w

    def draw_text(self, text, x, y, font="F1", size=10, r=0, g=0, b=0, align="left", max_width=None):
        if not text:
            return
        self.save_state()
        self.set_fill_color(r, g, b)
        
        text_w = self.get_text_width(text, font, size)
        if max_width and text_w > max_width and len(text) > 3:
            while len(text) > 3 and (self.get_text_width(text + "...", font, size) > max_width):
                text = text[:-1]
            text = text + "..."
            text_w = self.get_text_width(text, font, size)

        tx = x
        if align == "center":
            tx = x - (text_w / 2.0)
        elif align == "right":
            tx = x - text_w

        esc = _pdf_escape(text)
        self.ops.append(f"BT /{font} {size:.2f} Tf {tx:.2f} {y:.2f} Td {esc.decode('latin1')} Tj ET".encode("latin1"))
        self.restore_state()

    def get_stream(self):
        return b"\n".join(self.ops) + b"\n"

def build_pdf_document(canvases):
    """Costruisce i byte completi del documento PDF 1.4 multi-pagina o singola pagina."""
    objects = []
    
    catalog_id = 1
    pages_id = 2
    
    page_count = len(canvases)
    page_ids = [3 + i * 2 for i in range(page_count)]
    content_ids = [4 + i * 2 for i in range(page_count)]
    
    font_f1_id = 3 + page_count * 2      # Helvetica
    font_f2_id = font_f1_id + 1          # Helvetica-Bold
    font_f3_id = font_f1_id + 2          # Helvetica-Oblique
    
    obj_catalog = f"{catalog_id} 0 obj\n<< /Type /Catalog /Pages {pages_id} 0 R >>\nendobj\n".encode("latin1")
    kids_str = " ".join(f"{pid} 0 R" for pid in page_ids)
    obj_pages = f"{pages_id} 0 obj\n<< /Type /Pages /Kids [{kids_str}] /Count {page_count} >>\nendobj\n".encode("latin1")
    
    objs = [obj_catalog, obj_pages]
    
    for i, c in enumerate(canvases):
        pid = page_ids[i]
        cid = content_ids[i]
        stream_bytes = c.get_stream()
        
        page_dict = (
            f"{pid} 0 obj\n"
            f"<< /Type /Page /Parent {pages_id} 0 R "
            f"/MediaBox [0 0 {c.width:.2f} {c.height:.2f}] "
            f"/Resources << /Font << /F1 {font_f1_id} 0 R /F2 {font_f2_id} 0 R /F3 {font_f3_id} 0 R >> >> "
            f"/Contents {cid} 0 R >>\n"
            f"endobj\n"
        ).encode("latin1")
        
        content_dict = (
            f"{cid} 0 obj\n"
            f"<< /Length {len(stream_bytes)} >>\n"
            f"stream\n"
        ).encode("latin1") + stream_bytes + b"endstream\nendobj\n"
        
        objs.append(page_dict)
        objs.append(content_dict)
        
    obj_f1 = f"{font_f1_id} 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>\nendobj\n".encode("latin1")
    obj_f2 = f"{font_f2_id} 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>\nendobj\n".encode("latin1")
    obj_f3 = f"{font_f3_id} 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>\nendobj\n".encode("latin1")
    objs.extend([obj_f1, obj_f2, obj_f3])
    
    header = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
    offsets = [len(header)]
    body = b""
    for obj in objs:
        offsets.append(offsets[-1] + len(obj))
        body += obj
        
    xref_offset = len(header) + len(body)
    total_objs = len(objs) + 1
    xref = f"xref\n0 {total_objs}\n0000000000 65535 f \n".encode("latin1")
    for off in offsets[:-1]:
        xref += f"{off:010d} 00000 n \n".encode("latin1")
        
    trailer = (
        f"trailer\n"
        f"<< /Size {total_objs} /Root {catalog_id} 0 R >>\n"
        f"startxref\n"
        f"{xref_offset}\n"
        f"%%EOF\n"
    ).encode("latin1")
    
    return header + body + xref + trailer


# =====================================================================
# GENERATORE PDF ORARIO DOCENTE (A4 LANDSCAPE)
# =====================================================================

def generate_teacher_timetable_pdf(data, teacher_name, options=None):
    """
    Genera il documento PDF A4 Orizzontale ad alta risoluzione dell'orario
    settimanale individuale del docente.
    """
    options = options or {}
    validity_date = options.get("validity_date") or get_default_validity_date()
    institution = data.get("institution", 'I.I.S. "Rolando da Piazzola"')
    school_year = data.get("school_year") or "2026/2027"
    days = data.get("days", ["Lun", "Mar", "Mer", "Gio", "Ven"])

    from webapp.fet_engine import build_timetable_views
    views = build_timetable_views(data)
    by_teacher = views["by_teacher"]
    teacher_stats = views["teacher_stats"]

    if teacher_name not in by_teacher:
        raise ValueError(f"Docente '{teacher_name}' non trovato nell'orario risolto.")

    t_matrix = by_teacher[teacher_name]
    stats = teacher_stats.get(teacher_name, {})
    tot_h = stats.get("total_hours", 0)
    teach_h = stats.get("teaching_hours", tot_h)
    disp_h = stats.get("disp_hours", 0)

    # Dati anagrafici docente
    from webapp.database import compute_teacher_email
    email_domain = data.get("teacher_email_domain") or data.get("parameters", {}).get("Dominio email istituzionale docenti") or "rolandodapiazzola.edu.it"
    t_record = next((t for t in data.get("teachers", []) if t.get("name") == teacher_name), {})
    cdc = (t_record.get("cdc") or "").strip()
    email = (t_record.get("email") or "").strip().lower() or compute_teacher_email(teacher_name, email_domain)
    free_days = {t_record.get("free_day_1", ""), t_record.get("free_day_2", "")} - {"", None}

    subjects_list = [s["name"] for s in data.get("subjects", [])]
    color_map = build_subject_color_map(subjects_list)

    # Inizializza Canvas A4 Landscape
    PAGE_W = 841.89
    PAGE_H = 595.28
    c = PDFCanvas(PAGE_W, PAGE_H)

    # Margini
    ML = 26.0
    MR = PAGE_W - 26.0
    MT = PAGE_H - 22.0
    MB = 22.0
    W = MR - ML

    # 1. HEADER
    c.save_state()
    # Titolo Istituto (con limite larghezza per evitare collisioni con la data di validità)
    c.draw_text(institution.upper(), ML, MT - 14, font="F2", size=14, r=0.06, g=0.09, b=0.16, max_width=W - 220.0)
    c.draw_text(f"ORARIO SETTIMANALE INDIVIDUALE DELLE LEZIONI • A.S. {school_year}", ML, MT - 27, font="F1", size=8.5, r=0.28, g=0.33, b=0.41, max_width=W - 220.0)

    # Box a destra: validità
    c.draw_text(f"In vigore dal: {validity_date}", MR, MT - 14, font="F2", size=9.5, r=0.06, g=0.09, b=0.16, align="right")
    c.draw_text("STRETTAMENTE RISERVATO • Ad uso esclusivo del docente", MR, MT - 27, font="F1", size=7.5, r=0.39, g=0.45, b=0.55, align="right")

    # Linea separatrice Header
    c.set_stroke_color(0.06, 0.09, 0.16)
    c.set_line_width(1.5)
    c.line(ML, MT - 33, MR, MT - 33)
    c.restore_state()

    # 2. BANNER DOCENTE (Y da MT-38 a MT-64, altezza 26 pt)
    BY = MT - 62
    BH = 25.0
    c.save_state()
    c.set_fill_color(0.973, 0.980, 0.988) # #f8fafc
    c.set_stroke_color(0.796, 0.835, 0.882) # #cbd5e1
    c.set_line_width(0.8)
    c.rect(ML, BY, W, BH, fill=True, stroke=True)

    # 1. Sezione Destra: Ore Cattedra (ancorato a destra con margine sicuro)
    hours_txt = f"Ore Cattedra: {tot_h}h ({teach_h}h lez" + (f", {disp_h}h disp)" if disp_h else ")")
    hours_w = c.get_text_width(hours_txt, font="F2", size=9.5)
    c.draw_text(hours_txt, MR - 10.0, BY + 8.5, font="F2", size=9.5, r=0.114, g=0.306, b=0.847, align="right")
    hours_left_bound = MR - 10.0 - hours_w

    # 2. Sezione Sinistra: Nome Docente (Prof. ...)
    name_txt = f"Prof. {teacher_name}"
    name_w = c.get_text_width(name_txt, font="F2", size=11.5)
    c.draw_text(name_txt, ML + 10.0, BY + 8.0, font="F2", size=11.5, r=0.06, g=0.09, b=0.16)
    badge_start_x = ML + 10.0 + name_w + 10.0

    # 3. Sezione Centro: Email istituzionale (dinamicamente posizionata per non collidere con destra/sinistra)
    email_txt = f"Email: {email}" if email else "Email: non presente"
    email_w = c.get_text_width(email_txt, font="F1", size=8.5)
    center_x = (ML + MR) / 2.0
    email_x_left = center_x - (email_w / 2.0)
    email_x_right = center_x + (email_w / 2.0)
    if email_x_right > hours_left_bound - 15.0:
        email_x_right = hours_left_bound - 15.0
        email_x_left = email_x_right - email_w
    c.draw_text(email_txt, (email_x_left + email_x_right) / 2.0, BY + 8.5, font="F1", size=8.5, r=0.20, g=0.25, b=0.33, align="center")

    # 4. Badge CDC e Descrizione Disciplina (dinamico, non si accavalla mai con nome docente o email)
    avail_cdc_w = (email_x_left - 12.0) - badge_start_x
    if cdc and avail_cdc_w > 15.0:
        if " - " in cdc:
            cdc_code, cdc_desc = cdc.split(" - ", 1)
            cdc_code = cdc_code.strip()
            cdc_desc = cdc_desc.strip()
        elif " " in cdc and len(cdc.split()[0]) <= 8:
            parts = cdc.split(None, 1)
            cdc_code = parts[0].strip()
            cdc_desc = parts[1].strip()
        else:
            cdc_code = cdc.strip()
            cdc_desc = ""

        code_w = c.get_text_width(cdc_code, font="F2", size=8.5)
        badge_w = max(36.0, code_w + 12.0)
        if badge_w > avail_cdc_w:
            badge_w = max(24.0, avail_cdc_w)

        c.set_fill_color(0.878, 0.906, 0.996) # #e0e7ff
        c.set_stroke_color(0.757, 0.804, 0.988)
        c.rect(badge_start_x, BY + 5.5, badge_w, 14.0, fill=True, stroke=True)
        c.draw_text(cdc_code, badge_start_x + (badge_w / 2.0), BY + 9.2, font="F2", size=8.5, r=0.118, g=0.227, b=0.541, align="center", max_width=badge_w - 4.0)

        # Se è presente una descrizione della disciplina (es. "Scienze Matematiche Applicate")
        if cdc_desc:
            desc_x = badge_start_x + badge_w + 6.0
            avail_desc_w = (email_x_left - 12.0) - desc_x
            if avail_desc_w > 30.0:
                c.draw_text(cdc_desc, desc_x, BY + 9.0, font="F1", size=8.5, r=0.28, g=0.33, b=0.45, align="left", max_width=avail_desc_w)

    c.restore_state()

    # 3. TABELLA GRIGLIA ORARIO
    FOOTER_TOP = MB + 28
    GRID_TOP = BY - 7.0
    GRID_BOTTOM = FOOTER_TOP + 6.0
    GRID_HEIGHT = GRID_TOP - GRID_BOTTOM

    HEADER_ROW_H = 20.0
    BODY_HEIGHT = GRID_HEIGHT - HEADER_ROW_H

    NUM_HOURS = 8
    ACTIVE_INTERVALS = [2, 4]
    INT_ROW_H = 9.5
    total_int_h = len(ACTIVE_INTERVALS) * INT_ROW_H
    LESSON_ROW_H = (BODY_HEIGHT - total_int_h) / NUM_HOURS

    # Larghezze colonne
    COL_ORA_W = 62.0
    COL_DAY_W = (W - COL_ORA_W) / max(1, len(days))

    # Header Tabella (Giorni)
    c.save_state()
    c.set_fill_color(0.06, 0.09, 0.16) # Dark Navy #0f172a
    c.set_stroke_color(0.20, 0.25, 0.33)
    c.set_line_width(0.8)

    # Cella "ORA"
    c.rect(ML, GRID_TOP - HEADER_ROW_H, COL_ORA_W, HEADER_ROW_H, fill=True, stroke=True)
    c.draw_text("ORA", ML + (COL_ORA_W / 2.0), GRID_TOP - 13.5, font="F2", size=8.5, r=1, g=1, b=1, align="center")

    # Colonne Giorni
    for di, d in enumerate(days):
        gx = ML + COL_ORA_W + (di * COL_DAY_W)
        is_free = (d in free_days)
        c.rect(gx, GRID_TOP - HEADER_ROW_H, COL_DAY_W, HEADER_ROW_H, fill=True, stroke=True)
        d_name = get_day_name(d, lang="it", full=True).upper()
        
        if is_free:
            c.draw_text(d_name, gx + (COL_DAY_W / 2.0), GRID_TOP - 11.5, font="F2", size=8.5, r=1, g=1, b=1, align="center")
            c.draw_text("(GIORNO LIBERO)", gx + (COL_DAY_W / 2.0), GRID_TOP - 18.0, font="F1", size=6.5, r=0.576, g=0.773, b=0.992, align="center")
        else:
            c.draw_text(d_name, gx + (COL_DAY_W / 2.0), GRID_TOP - 13.5, font="F2", size=9.0, r=1, g=1, b=1, align="center")
    c.restore_state()

    # Righe Ore & Lezioni
    current_y = GRID_TOP - HEADER_ROW_H

    for h_num in range(1, NUM_HOURS + 1):
        h_str = str(h_num)
        h_info = ORARIO_ORE.get(h_num, {"inizio": "", "fine": ""})
        h_time_str = f"{h_info['inizio']} - {h_info['fine']}" if h_info.get("inizio") else ""

        current_y -= LESSON_ROW_H

        # Colonna Ora
        c.save_state()
        c.set_fill_color(0.973, 0.980, 0.988) # #f8fafc
        c.set_stroke_color(0.796, 0.835, 0.882) # #cbd5e1
        c.set_line_width(0.6)
        c.rect(ML, current_y, COL_ORA_W, LESSON_ROW_H, fill=True, stroke=True)
        c.draw_text(f"{h_num}\xaa ora", ML + (COL_ORA_W / 2.0), current_y + (LESSON_ROW_H / 2.0) + 3.0, font="F2", size=10, r=0.06, g=0.09, b=0.16, align="center")
        c.draw_text(h_time_str, ML + (COL_ORA_W / 2.0), current_y + (LESSON_ROW_H / 2.0) - 7.5, font="F1", size=7.5, r=0.39, g=0.45, b=0.55, align="center")
        c.restore_state()

        # Colonne Lezioni per giorno
        for di, d in enumerate(days):
            gx = ML + COL_ORA_W + (di * COL_DAY_W)
            is_free_day = (d in free_days)
            slots = t_matrix.get(d, {}).get(h_str, [])

            c.save_state()
            if is_free_day:
                # Giorno libero: tratteggio / sfondo neutro
                c.set_fill_color(0.965, 0.973, 0.980)
                c.set_stroke_color(0.85, 0.88, 0.92)
                c.set_line_width(0.5)
                c.rect(gx, current_y, COL_DAY_W, LESSON_ROW_H, fill=True, stroke=True)
                c.draw_text("LIBERO", gx + (COL_DAY_W / 2.0), current_y + (LESSON_ROW_H / 2.0) - 2.5, font="F2", size=7.5, r=0.60, g=0.65, b=0.72, align="center")
            elif not slots:
                # Ora buca / nessuna lezione
                c.set_fill_color(1.0, 1.0, 1.0)
                c.set_stroke_color(0.85, 0.88, 0.92)
                c.set_line_width(0.5)
                c.rect(gx, current_y, COL_DAY_W, LESSON_ROW_H, fill=True, stroke=True)
            else:
                slot = slots[0]
                is_disp = slot.get("is_disposizione", False) or "disposiz" in (slot.get("subject") or "").lower()

                if is_disp:
                    # Cella Disposizione (Ambra chiaro)
                    c.set_fill_color(0.996, 0.953, 0.780) # #fef3c7
                    c.set_stroke_color(0.961, 0.620, 0.043) # #f59e0b
                    c.set_line_width(0.8)
                    c.rect(gx, current_y, COL_DAY_W, LESSON_ROW_H, fill=True, stroke=True)

                    desc = (slot.get("custom_desc") or "Sede Centrale").strip()
                    c.draw_text("DISPOSIZIONE", gx + (COL_DAY_W / 2.0), current_y + (LESSON_ROW_H / 2.0) + 4.0, font="F2", size=9.5, r=0.706, g=0.325, b=0.035, align="center")
                    c.draw_text(desc, gx + (COL_DAY_W / 2.0), current_y + (LESSON_ROW_H / 2.0) - 6.5, font="F1", size=7.5, r=0.573, g=0.251, b=0.055, align="center", max_width=COL_DAY_W - 6)
                else:
                    # Cella Lezione normale con colore materia pastello
                    subj = slot.get("subject", "")
                    students = slot.get("students", [])
                    cls_str = " + ".join(students) if students else ""
                    room = slot.get("room", "")
                    bld = slot.get("building", "")
                    room_badge = f"{room}{f' ({bld})' if bld and bld != 'Centrale' else ''}" if room else ""
                    co_teachers = [other for other in slot.get("teachers", []) if other != teacher_name]
                    co_str = f"con {', '.join(co_teachers)}" if co_teachers else ""

                    hex_bg, hex_txt = color_map.get(subj, ("#f1f5f9", "#0f172a"))
                    rb, gb, bb = _hex_to_rgb(hex_bg)
                    rt, gt, bt = _hex_to_rgb(hex_txt)

                    c.set_fill_color(rb, gb, bb)
                    c.set_stroke_color(0.796, 0.835, 0.882) # #cbd5e1
                    c.set_line_width(0.6)
                    c.rect(gx, current_y, COL_DAY_W, LESSON_ROW_H, fill=True, stroke=True)

                    # Testi della cella distribuiti verticalmente
                    cy = current_y + (LESSON_ROW_H / 2.0)
                    if co_str:
                        c.draw_text(cls_str, gx + (COL_DAY_W / 2.0), cy + 11.5, font="F2", size=10.0, r=rt, g=gt, b=bt, align="center", max_width=COL_DAY_W - 4)
                        c.draw_text(subj, gx + (COL_DAY_W / 2.0), cy + 1.5, font="F1", size=7.8, r=rt, g=gt, b=bt, align="center", max_width=COL_DAY_W - 4)
                        c.draw_text(room_badge, gx + (COL_DAY_W / 2.0), cy - 7.5, font="F2", size=7.2, r=0.28, g=0.33, b=0.41, align="center", max_width=COL_DAY_W - 4)
                        c.draw_text(co_str, gx + (COL_DAY_W / 2.0), cy - 15.5, font="F3", size=6.8, r=0.01, g=0.41, b=0.63, align="center", max_width=COL_DAY_W - 4)
                    else:
                        c.draw_text(cls_str, gx + (COL_DAY_W / 2.0), cy + 8.5, font="F2", size=10.5, r=rt, g=gt, b=bt, align="center", max_width=COL_DAY_W - 4)
                        c.draw_text(subj, gx + (COL_DAY_W / 2.0), cy - 2.0, font="F1", size=8.2, r=rt, g=gt, b=bt, align="center", max_width=COL_DAY_W - 4)
                        if room_badge:
                            c.draw_text(room_badge, gx + (COL_DAY_W / 2.0), cy - 12.0, font="F2", size=7.5, r=0.28, g=0.33, b=0.41, align="center", max_width=COL_DAY_W - 4)
            c.restore_state()

        # Inserimento riga Intervallo se applicabile
        if h_num in ACTIVE_INTERVALS and h_num in INTERVALLI_DOPO_ORA:
            interv = INTERVALLI_DOPO_ORA[h_num]
            int_label = f"--- {interv.get('label', 'Intervallo')} ({interv.get('inizio')} - {interv.get('fine')}) ---"

            current_y -= INT_ROW_H

            c.save_state()
            c.set_fill_color(0.945, 0.961, 0.976) # #f1f5f9
            c.set_stroke_color(0.75, 0.80, 0.85)
            c.set_line_width(0.5)
            c.rect(ML, current_y, W, INT_ROW_H, fill=True, stroke=True)
            c.draw_text(int_label, ML + (W / 2.0), current_y + 2.5, font="F2", size=6.8, r=0.39, g=0.45, b=0.55, align="center")
            c.restore_state()

    # Bordo esterno principale della tabella
    c.save_state()
    c.set_stroke_color(0.06, 0.09, 0.16)
    c.set_line_width(1.2)
    c.rect(ML, GRID_BOTTOM, W, GRID_TOP - GRID_BOTTOM, fill=False, stroke=True)
    c.restore_state()

    # 4. FOOTER (Note di Riservatezza & Firme)
    c.save_state()
    c.set_stroke_color(0.796, 0.835, 0.882) # #cbd5e1
    c.set_line_width(0.8)
    c.line(ML, FOOTER_TOP, MR, FOOTER_TOP)

    # Note legali
    c.draw_text("Documento ufficiale ad uso strettamente personale del docente. Nessuna diffusione non autorizzata.", ML, FOOTER_TOP - 11, font="F1", size=7.2, r=0.39, g=0.45, b=0.55)
    c.draw_text("Generato con Eurario FET Suite • Algoritmo di Ottimizzazione Euristica", ML, FOOTER_TOP - 20, font="F3", size=6.8, r=0.60, g=0.65, b=0.72)

    # Firme
    c.draw_text("Firma del Docente per Presa Visione:  _______________________________", MR - 280, FOOTER_TOP - 11, font="F1", size=7.8, r=0.20, g=0.25, b=0.33)
    c.draw_text("Il Dirigente Scolastico:  _______________________________", MR - 280, FOOTER_TOP - 22, font="F1", size=7.8, r=0.20, g=0.25, b=0.33)
    c.restore_state()

    return build_pdf_document([c])


# =====================================================================
# GENERATORE iCALENDAR (.ICS) CON RICORRENZA SETTIMANALE
# =====================================================================

def _parse_until_date(end_date_str, school_year="2026/2027"):
    """
    Estrae una data di fine ricorrenza compatibile con RFC 5545 (YYYYMMDD).
    Default: 8 giugno della primavera dell'anno scolastico (es. 2027-06-08).
    """
    clean = str(end_date_str or "").strip()
    
    # Prova DD/MM/YYYY
    m = re.match(r"^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})$", clean)
    if m:
        day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"{year:04d}{month:02d}{day:02d}"

    # Prova YYYY-MM-DD
    m = re.match(r"^(\d{4})[/.-](\d{1,2})[/.-](\d{1,2})$", clean)
    if m:
        year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"{year:04d}{month:02d}{day:02d}"

    # Prova DD/MM (senza anno)
    m = re.match(r"^(\d{1,2})[/.-](\d{1,2})$", clean)
    if m:
        day, month = int(m.group(1)), int(m.group(2))
        end_year = 2027
        if "/" in school_year:
            try:
                end_year = int(school_year.split("/")[1])
            except Exception:
                pass
        return f"{end_year:04d}{month:02d}{day:02d}"

    # Default assoluto: 8 Giugno 2027 (o anno scolastico corrente)
    end_year = 2027
    if "/" in school_year:
        try:
            end_year = int(school_year.split("/")[1])
        except Exception:
            pass
    return f"{end_year:04d}0608"

def _escape_ics_text(text):
    if not text:
        return ""
    text = str(text)
    text = text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
    text = text.replace("\r\n", "\\n").replace("\n", "\\n")
    return text

def _fold_line(line, limit=75):
    """
    RFC 5545 Section 3.1: Lines of text SHOULD NOT be longer than 75 octets.
    Long lines are folded by inserting CRLF followed by a single space.
    """
    encoded = line.encode("utf-8")
    if len(encoded) <= limit:
        return line
    out_lines = []
    curr = b""
    first = True
    for ch in line:
        ch_enc = ch.encode("utf-8")
        max_bytes = limit if first else (limit - 1)
        if len(curr) + len(ch_enc) > max_bytes:
            out_lines.append(curr.decode("utf-8") if first else (" " + curr.decode("utf-8")))
            curr = ch_enc
            first = False
        else:
            curr += ch_enc
    if curr:
        out_lines.append(curr.decode("utf-8") if first else (" " + curr.decode("utf-8")))
    return "\r\n".join(out_lines)

def generate_teacher_timetable_ical(data, teacher_name, options=None):
    """
    Genera il file standard iCalendar (.ics) RFC 5545 per l'orario del singolo docente.
    Ogni lezione o disposizione è inserita come evento settimanale ricorrente (RRULE:FREQ=WEEKLY)
    fino alla data di termine lezioni dell'anno scolastico.
    Importabile con 1 clic in Google Calendar, Apple Calendar, Outlook e Thunderbird.
    """
    options = options or {}
    institution = data.get("institution", 'I.I.S. "Rolando da Piazzola"')
    school_year = data.get("school_year") or "2026/2027"
    days = data.get("days", ["Lun", "Mar", "Mer", "Gio", "Ven"])

    # Risoluzione termine anno scolastico
    end_date_param = options.get("school_year_end_date") or data.get("school_year_end_date")
    if not end_date_param:
        end_date_param = data.get("parameters", {}).get("Data termine lezioni (fine anno scolastico)", "08/06/2027")
    until_ymd = _parse_until_date(end_date_param, school_year)

    from webapp.fet_engine import build_timetable_views
    views = build_timetable_views(data)
    by_teacher = views["by_teacher"]

    if teacher_name not in by_teacher:
        raise ValueError(f"Docente '{teacher_name}' non trovato nell'orario.")

    t_matrix = by_teacher[teacher_name]

    # Mappa giorni della settimana su RFC 5545 BYDAY e indice giorno
    # Lunedì = 0 ... Sabato = 5
    DAY_TO_BYDAY = {
        "lun": ("MO", 0), "lunedì": ("MO", 0), "lunedi": ("MO", 0), "mon": ("MO", 0),
        "mar": ("TU", 1), "martedì": ("TU", 1), "martedi": ("TU", 1), "tue": ("TU", 1),
        "mer": ("WE", 2), "mercoledì": ("WE", 2), "mercoledi": ("WE", 2), "wed": ("WE", 2),
        "gio": ("TH", 3), "giovedì": ("TH", 3), "giovedi": ("TH", 3), "thu": ("TH", 3),
        "ven": ("FR", 4), "venerdì": ("FR", 4), "venerdi": ("FR", 4), "fri": ("FR", 4),
        "sab": ("SA", 5), "sabato": ("SA", 5), "sat": ("SA", 5),
    }

    # Calcola il lunedì di riferimento della settimana corrente
    now = datetime.now()
    monday_offset = (0 - now.weekday()) % 7
    if monday_offset == 0 and now.hour > 18:
        # Se siamo di lunedì sera, parte dal lunedì prossimo
        ref_monday = (now + timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        ref_monday = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

    safe_teacher = re.sub(r"[^a-zA-Z0-9]", "_", teacher_name).lower()
    now_stamp = now.strftime("%Y%m%dT%H%M%SZ")

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Eurario FET Suite//Timetable Engine//IT",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:Orario - Prof. {teacher_name}",
        f"X-WR-CALDESC:Orario delle lezioni per {teacher_name} - {institution} (A.S. {school_year})",
        "X-WR-TIMEZONE:Europe/Rome",
        "BEGIN:VTIMEZONE",
        "TZID:Europe/Rome",
        "X-LIC-LOCATION:Europe/Rome",
        "BEGIN:DAYLIGHT",
        "TZOFFSETFROM:+0100",
        "TZOFFSETTO:+0200",
        "TZNAME:CEST",
        "DTSTART:19700329T020000",
        "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU",
        "END:DAYLIGHT",
        "BEGIN:STANDARD",
        "TZOFFSETFROM:+0200",
        "TZOFFSETTO:+0100",
        "TZNAME:CET",
        "DTSTART:19701025T030000",
        "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU",
        "END:STANDARD",
        "END:VTIMEZONE"
    ]

    event_count = 0
    for d in days:
        d_lower = d.lower().strip()
        byday_info = DAY_TO_BYDAY.get(d_lower)
        if not byday_info:
            for k, v in DAY_TO_BYDAY.items():
                if d_lower.startswith(k[:3]):
                    byday_info = v
                    break
        if not byday_info:
            continue

        byday_code, day_idx = byday_info
        event_date = ref_monday + timedelta(days=day_idx)
        date_str = event_date.strftime("%Y%m%d")

        for h_str, slots in t_matrix.get(d, {}).items():
            if not slots:
                continue
            try:
                h_num = int(h_str)
            except ValueError:
                continue

            slot = slots[0]
            is_disp = slot.get("is_disposizione", False) or "disposiz" in (slot.get("subject") or "").lower()

            h_info = ORARIO_ORE.get(h_num, {"inizio": "08:00", "fine": "08:55"})
            t_start = (h_info.get("inizio") or "08:00").replace(":", "") + "00"
            t_end = (h_info.get("fine") or "08:55").replace(":", "") + "00"

            dtstart = f"{date_str}T{t_start}"
            dtend = f"{date_str}T{t_end}"

            uid = f"eurario-{safe_teacher}-{byday_code.lower()}-{h_num}-{now.year}@eurario.it"

            if is_disp:
                desc = (slot.get("custom_desc") or "Sede Centrale").strip()
                summary = f"Disposizione ({desc})"
                location = desc
                description = f"Ora a disposizione per supplenze o sorveglianza.\\nDocente: Prof. {teacher_name}\\nIstituto: {institution}\\n{h_num}\xaa ora ({h_info.get('inizio')} - {h_info.get('fine')})"
            else:
                subj = slot.get("subject", "")
                students = slot.get("students", [])
                cls_str = " + ".join(students) if students else ""
                room = slot.get("room", "")
                bld = slot.get("building", "")
                co_teachers = [other for other in slot.get("teachers", []) if other != teacher_name]
                co_str = f" [con Prof. {', '.join(co_teachers)}]" if co_teachers else ""

                summary = f"{subj} ({cls_str}){co_str}" if cls_str else subj
                location = f"{room}{f' - {bld}' if bld and bld != 'Centrale' else ''}".strip()
                description = (
                    f"Materia: {subj}\\n"
                    f"Classe: {cls_str}\\n"
                    f"Docente: Prof. {teacher_name}\\n"
                    f"Aula / Spazio: {room or 'N/D'}{f' ({bld})' if bld else ''}\\n"
                    f"Orario: {h_num}\xaa ora ({h_info.get('inizio')} - {h_info.get('fine')})\\n"
                    f"Istituto: {institution}"
                )
                if co_teachers:
                    description += f"\\nCompresenza: Prof. {', '.join(co_teachers)}"

            lines.append("BEGIN:VEVENT")
            lines.append(f"UID:{uid}")
            lines.append(f"DTSTAMP:{now_stamp}")
            lines.append(f"DTSTART;TZID=Europe/Rome:{dtstart}")
            lines.append(f"DTEND;TZID=Europe/Rome:{dtend}")
            lines.append(f"RRULE:FREQ=WEEKLY;UNTIL={until_ymd}T235959Z;BYDAY={byday_code}")
            lines.append(f"SUMMARY:{_escape_ics_text(summary)}")
            if location:
                lines.append(f"LOCATION:{_escape_ics_text(location)}")
            lines.append(f"DESCRIPTION:{description}")
            lines.append("STATUS:CONFIRMED")
            lines.append("TRANSP:OPAQUE")
            lines.append("END:VEVENT")
            event_count += 1

    lines.append("END:VCALENDAR")
    folded = [_fold_line(line) for line in lines]
    return "\r\n".join(folded) + "\r\n"
