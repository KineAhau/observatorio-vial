"""Convert markdown documents to PDF for the Observatorio."""
from fpdf import FPDF
import os, re

FONT_DIR = r"C:\Windows\Fonts"
ASSETS = r"C:\Users\Ahau Kine\.openclaw\workspace-dev\projects\observatorio\site\assets"

def create_pdf(title, subtitle, md_path, output_name):
    with open(md_path, encoding="utf-8") as f:
        lines = f.readlines()
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_font("main", "", os.path.join(FONT_DIR, "arial.ttf"))
    pdf.add_font("main", "B", os.path.join(FONT_DIR, "arialbd.ttf"))
    pdf.add_font("main", "I", os.path.join(FONT_DIR, "ariali.ttf"))
    
    pdf.add_page()
    
    # Header bar
    pdf.set_font("main", "B", 9)
    pdf.set_text_color(0, 104, 157)
    pdf.cell(95, 8, "Observatorio de Seguridad Vial | ANASEVI")
    pdf.cell(95, 8, "2026", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(0, 104, 157)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    
    # Title
    pdf.set_font("main", "B", 20)
    pdf.set_text_color(26, 72, 106)
    pdf.multi_cell(0, 10, title)
    pdf.ln(3)
    
    if subtitle:
        pdf.set_font("main", "I", 11)
        pdf.set_text_color(100)
        pdf.multi_cell(0, 6, subtitle)
        pdf.ln(3)
    
    pdf.set_font("main", "", 10)
    pdf.set_text_color(100)
    pdf.cell(0, 6, "Dr. Arturo Cervantes Trejo", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "ANASEVI | Universidad Anahuac | Investigador independiente", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    
    # Process markdown lines
    in_table = False
    table_rows = []
    
    for line in lines:
        line = line.rstrip("\n")
        stripped = line.strip()
        
        # Skip metadata lines we already used
        if stripped.startswith("**Arturo Cervantes") or stripped.startswith("**Autor de correspondencia"):
            continue
        if stripped == "---":
            if not in_table:
                pdf.ln(4)
            continue
        
        # Tables
        if "|" in stripped and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if all(set(c) <= set("- :") for c in cells):
                continue  # separator row
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            continue
        elif in_table:
            # Flush table
            _flush_table(pdf, table_rows)
            in_table = False
            table_rows = []
        
        # Headers
        if stripped.startswith("# ") and not stripped.startswith("## "):
            # Skip top-level title (we already have it)
            continue
        elif stripped.startswith("## "):
            pdf.ln(6)
            pdf.set_font("main", "B", 14)
            pdf.set_text_color(0, 104, 157)
            text = stripped.lstrip("#").strip()
            text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
            pdf.multi_cell(0, 8, text)
            pdf.ln(2)
        elif stripped.startswith("### "):
            pdf.ln(4)
            pdf.set_font("main", "B", 12)
            pdf.set_text_color(26, 72, 106)
            text = stripped.lstrip("#").strip()
            text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
            pdf.multi_cell(0, 7, text)
            pdf.ln(2)
        elif stripped.startswith("#### "):
            pdf.ln(3)
            pdf.set_font("main", "B", 11)
            pdf.set_text_color(45)
            text = stripped.lstrip("#").strip()
            text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
            pdf.multi_cell(0, 6, text)
            pdf.ln(1)
        elif stripped == "":
            pdf.ln(3)
        else:
            pdf.set_font("main", "", 10)
            pdf.set_text_color(45)
            # Clean markdown formatting
            text = stripped
            text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
            text = re.sub(r'\*([^*]+)\*', r'\1', text)
            # Bullet points
            if text.startswith("- ") or text.startswith("* "):
                text = "  " + chr(8226) + " " + text[2:]
            elif re.match(r'^\d+\.\s', text):
                text = "  " + text
            pdf.set_x(10)
            pdf.multi_cell(0, 5.5, text)
    
    # Flush remaining table
    if in_table:
        _flush_table(pdf, table_rows)
    
    # Footer
    pdf.ln(10)
    pdf.set_font("main", "I", 9)
    pdf.set_text_color(100)
    pdf.multi_cell(0, 5, "Fuente: INEGI, Estadisticas de Defunciones Registradas 2015-2023.\nObservatorio de Seguridad Vial - observatoriovial.mx")
    
    out = os.path.join(ASSETS, output_name)
    pdf.output(out)
    print(f"OK: {output_name} ({os.path.getsize(out):,} bytes)")


def _flush_table(pdf, rows):
    if not rows:
        return
    n_cols = len(rows[0])
    avail = 190
    
    # If too many columns, switch to landscape or reduce font
    if n_cols > 8:
        font_size = 6
        trunc = 14
    elif n_cols > 5:
        font_size = 7
        trunc = 18
    else:
        font_size = 8
        trunc = 22
    
    if n_cols > 7:
        avail = 270  # landscape-ish: we just use smaller cells
    col_w = max(avail / n_cols, 12)
    total_w = col_w * n_cols
    
    # Header row
    pdf.set_font("main", "B", font_size)
    pdf.set_fill_color(0, 104, 157)
    pdf.set_text_color(255)
    for cell in rows[0]:
        pdf.cell(col_w, 5, cell[:trunc], border=1, fill=True, align="C")
    pdf.ln()
    
    # Data rows
    pdf.set_font("main", "", font_size)
    pdf.set_text_color(45)
    for row in rows[1:]:
        for i, cell in enumerate(row):
            text = cell[:trunc] if i < len(row) else ""
            pdf.cell(col_w, 4.5, text, border=1, align="C")
        pdf.ln()
    pdf.set_x(10)
    pdf.ln(4)


# Generate all three documents
docs = [
    {
        "title": "Mortalidad de motociclistas en Mexico, 2015-2023",
        "subtitle": "Analisis de tendencias mediante tasas estandarizadas por edad a nivel nacional y subnacional",
        "md": r"C:\Users\Ahau Kine\Downloads\articulo-motociclistas-borrador.md",
        "out": "articulo-motociclistas-2026.pdf"
    },
    {
        "title": "Policy Brief: Crisis de mortalidad en motociclistas en Mexico",
        "subtitle": "Una emergencia que se acelera",
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
        create_pdf(d["title"], d["subtitle"], d["md"], d["out"])
    except Exception as e:
        import traceback
        print(f"ERROR {d['out']}: {e}")
        traceback.print_exc()
