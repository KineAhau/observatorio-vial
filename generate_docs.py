"""Convert markdown documents to PDF for the Observatorio - v2."""
from fpdf import FPDF
import os, re

FONT_DIR = r"C:\Windows\Fonts"
ASSETS = r"C:\Users\Ahau Kine\.openclaw\workspace-dev\projects\observatorio\site\assets"

class ObservatorioPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("main", "", os.path.join(FONT_DIR, "arial.ttf"))
        self.add_font("main", "B", os.path.join(FONT_DIR, "arialbd.ttf"))
        self.add_font("main", "I", os.path.join(FONT_DIR, "ariali.ttf"))
        self.set_auto_page_break(auto=True, margin=20)
    
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("main", "B", 8)
        self.set_text_color(0, 104, 157)
        self.cell(95, 6, "Observatorio de Seguridad Vial | ANASEVI")
        self.cell(95, 6, f"Pagina {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 104, 157)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)


def clean_text(text):
    """Remove markdown formatting and problematic unicode."""
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = text.replace('\u2014', ' - ')
    text = text.replace('\u2013', '-')
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2022', '-')
    text = text.replace('\u00b2', '2')
    text = text.replace('\u209c', 't')
    text = text.replace('\u00b9', '1')
    text = text.replace('\u00b3', '3')
    return text


def render_table(pdf, rows):
    if not rows:
        return
    n_cols = len(rows[0])
    avail = 190
    
    if n_cols > 8:
        fs = 6
    elif n_cols > 5:
        fs = 7
    else:
        fs = 8
    
    col_w = avail / n_cols
    if col_w < 10:
        col_w = 10
    
    # Check if table fits on page
    if pdf.get_y() > 240:
        pdf.add_page()
    
    pdf.set_x(10)
    pdf.set_font("main", "B", fs)
    pdf.set_fill_color(0, 104, 157)
    pdf.set_text_color(255)
    for cell in rows[0]:
        t = clean_text(cell)[:25]
        pdf.cell(col_w, 5.5, t, border=1, fill=True, align="C")
    pdf.ln()
    
    pdf.set_font("main", "", fs)
    pdf.set_text_color(45)
    for row in rows[1:]:
        pdf.set_x(10)
        if pdf.get_y() > 270:
            pdf.add_page()
        for cell in row:
            t = clean_text(cell)[:25]
            pdf.cell(col_w, 5, t, border=1, align="C")
        pdf.ln()
    
    pdf.set_x(10)
    pdf.ln(4)


def md_to_pdf(md_path, output_name, title, subtitle=""):
    with open(md_path, encoding="utf-8") as f:
        lines = f.readlines()
    
    pdf = ObservatorioPDF()
    pdf.add_page()
    
    # Cover
    pdf.set_font("main", "B", 9)
    pdf.set_text_color(0, 104, 157)
    pdf.cell(95, 8, "Observatorio de Seguridad Vial | ANASEVI")
    pdf.cell(95, 8, "Marzo 2026", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(0, 104, 157)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(12)
    
    pdf.set_font("main", "B", 20)
    pdf.set_text_color(26, 72, 106)
    pdf.set_x(10)
    pdf.multi_cell(0, 10, clean_text(title))
    pdf.ln(3)
    
    if subtitle:
        pdf.set_font("main", "I", 12)
        pdf.set_text_color(100)
        pdf.set_x(10)
        pdf.multi_cell(0, 7, clean_text(subtitle))
        pdf.ln(3)
    
    pdf.set_font("main", "", 10)
    pdf.set_text_color(100)
    pdf.cell(0, 6, "Dr. Arturo Cervantes Trejo", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "ANASEVI | Universidad Anahuac | Investigador independiente", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    
    # Process content
    in_table = False
    table_rows = []
    skip_title = True  # skip first H1
    
    for line in lines:
        line = line.rstrip("\n")
        stripped = line.strip()
        
        # Skip author lines
        if any(x in stripped for x in ["Autor de correspondencia", "afiliacion previa"]):
            continue
        if stripped == "---":
            if in_table:
                render_table(pdf, table_rows)
                in_table = False
                table_rows = []
            pdf.ln(2)
            continue
        
        # Tables
        if "|" in stripped and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if all(set(c) <= set("- :") for c in cells if c):
                continue
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            continue
        elif in_table:
            render_table(pdf, table_rows)
            in_table = False
            table_rows = []
        
        # Headers
        if stripped.startswith("# ") and not stripped.startswith("## "):
            if skip_title:
                skip_title = False
                continue
            pdf.add_page()
            pdf.set_font("main", "B", 18)
            pdf.set_text_color(26, 72, 106)
            pdf.set_x(10)
            pdf.multi_cell(0, 9, clean_text(stripped[2:]))
            pdf.ln(4)
        elif stripped.startswith("## "):
            pdf.ln(6)
            pdf.set_font("main", "B", 14)
            pdf.set_text_color(0, 104, 157)
            pdf.set_x(10)
            pdf.multi_cell(0, 8, clean_text(stripped[3:]))
            pdf.ln(2)
        elif stripped.startswith("### "):
            pdf.ln(4)
            pdf.set_font("main", "B", 12)
            pdf.set_text_color(26, 72, 106)
            pdf.set_x(10)
            pdf.multi_cell(0, 7, clean_text(stripped[4:]))
            pdf.ln(2)
        elif stripped.startswith("#### "):
            pdf.ln(3)
            pdf.set_font("main", "B", 11)
            pdf.set_text_color(45)
            pdf.set_x(10)
            pdf.multi_cell(0, 6, clean_text(stripped[5:]))
            pdf.ln(1)
        elif stripped == "":
            pdf.ln(3)
        else:
            pdf.set_font("main", "", 10)
            pdf.set_text_color(45)
            text = clean_text(stripped)
            if text.startswith("- ") or text.startswith("* "):
                text = "  - " + text[2:]
            elif re.match(r'^\d+\.\s', text):
                text = "  " + text
            pdf.set_x(10)
            pdf.multi_cell(0, 5.5, text)
    
    if in_table:
        render_table(pdf, table_rows)
    
    # Footer
    pdf.ln(8)
    pdf.set_font("main", "I", 9)
    pdf.set_text_color(100)
    pdf.set_x(10)
    pdf.multi_cell(0, 5, "Fuente: INEGI, Estadisticas de Defunciones Registradas 2015-2023.\nObservatorio de Seguridad Vial | ANASEVI\nobservatoriovial.mx")
    
    out = os.path.join(ASSETS, output_name)
    pdf.output(out)
    sz = os.path.getsize(out)
    print(f"OK: {output_name} ({sz:,} bytes, {pdf.page_no()} pages)")


# Generate all three documents
docs = [
    {
        "title": "Mortalidad de motociclistas en Mexico, 2015-2023",
        "subtitle": "Analisis de tendencias mediante tasas estandarizadas por edad a nivel nacional y subnacional",
        "md": r"C:\Users\Ahau Kine\Downloads\articulo-motociclistas-borrador.md",
        "out": "articulo-motociclistas-2026.pdf"
    },
    {
        "title": "Crisis de mortalidad en motociclistas en Mexico: una emergencia que se acelera",
        "subtitle": "Policy Brief - ANASEVI",
        "md": r"C:\Users\Ahau Kine\Downloads\policy-brief-motociclistas-2025.md",
        "out": "policy-brief-motociclistas-2025.pdf"
    },
    {
        "title": "Mortalidad Vial en Mexico: Tasas Estandarizadas",
        "subtitle": "Analisis de Microdatos 2015-2023 - Fase 2b",
        "md": r"C:\Users\Ahau Kine\Downloads\reporte-fase2b-tasas-estandarizadas.md",
        "out": "reporte-fase2b-tasas-estandarizadas.pdf"
    }
]

for d in docs:
    try:
        md_to_pdf(d["md"], d["out"], d["title"], d["subtitle"])
    except Exception as e:
        import traceback
        print(f"ERROR {d['out']}: {e}")
        traceback.print_exc()
