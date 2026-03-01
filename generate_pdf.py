"""Generate Policy Brief PDF - Unicode safe."""
from fpdf import FPDF
import os

FONT_DIR = r"C:\Windows\Fonts"

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=20)

# Use a Unicode TTF font
pdf.add_font("dejavu", "", os.path.join(FONT_DIR, "arial.ttf"), uni=True)
pdf.add_font("dejavu", "B", os.path.join(FONT_DIR, "arialbd.ttf"), uni=True)
pdf.add_font("dejavu", "I", os.path.join(FONT_DIR, "ariali.ttf"), uni=True)

pdf.add_page()

# Title
pdf.set_font("dejavu", "B", 9)
pdf.set_text_color(0, 104, 157)
pdf.cell(95, 8, "Observatorio de Seguridad Vial | ANASEVI")
pdf.cell(95, 8, "Policy Brief — Marzo 2026", align="R", new_x="LMARGIN", new_y="NEXT")
pdf.set_draw_color(0, 104, 157)
pdf.line(10, pdf.get_y(), 200, pdf.get_y())
pdf.ln(10)

pdf.set_font("dejavu", "B", 22)
pdf.set_text_color(26, 72, 106)
pdf.multi_cell(0, 12, "Crisis de Motociclistas\nen México")
pdf.ln(4)

pdf.set_font("dejavu", "", 12)
pdf.set_text_color(100)
pdf.cell(0, 8, "Análisis de microdatos de mortalidad vial INEGI 2015-2023", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

pdf.set_font("dejavu", "I", 10)
pdf.cell(0, 6, "Dr. Arturo Cervantes Trejo", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 6, "Académico, Universidad Anáhuac | Investigador independiente | Presidente, ANASEVI", new_x="LMARGIN", new_y="NEXT")
pdf.ln(8)

# Executive Summary
pdf.set_font("dejavu", "B", 14)
pdf.set_text_color(0, 104, 157)
pdf.cell(0, 10, "Resumen Ejecutivo", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("dejavu", "", 10)
pdf.set_text_color(45)
pdf.multi_cell(0, 5.5, "Entre 2015 y 2023, las muertes de motociclistas en México aumentaron un 87%, pasando de 1,541 a 2,885 defunciones anuales. Esta es la única categoría de usuario vial con crecimiento sostenido. Mientras las muertes de peatones y ocupantes de vehículos disminuyen, los motociclistas mueren cada vez más. La mitad de las víctimas son jóvenes de 15 a 29 años. Las muertes de mujeres motociclistas se duplicaron (+108%). México va en sentido contrario a la meta del Decenio de Acción por la Seguridad Vial.")
pdf.ln(6)

# Key findings
pdf.set_font("dejavu", "B", 14)
pdf.set_text_color(0, 104, 157)
pdf.cell(0, 10, "Hallazgos Clave", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("dejavu", "", 10)
pdf.set_text_color(45)

findings = [
    "+87% de muertes en motociclistas entre 2015 y 2023",
    "2,885 motociclistas muertos en 2023 — récord histórico",
    "50% son jóvenes de 15 a 29 años (1,449 en 2023)",
    "Mujeres: +108% de aumento (de 144 a 300 muertes)",
    "Jalisco, Guanajuato y Edo. de México: mayor mortalidad",
    "Única categoría de usuario vial en crecimiento sostenido",
    "México va en sentido contrario a la meta del Decenio de Acción",
]
for f in findings:
    pdf.cell(5)
    pdf.cell(0, 6, f"•  {f}", new_x="LMARGIN", new_y="NEXT")
pdf.ln(6)

# Table helper
def draw_table(headers, data, col_w):
    pdf.set_font("dejavu", "B", 8)
    pdf.set_fill_color(0, 104, 157)
    pdf.set_text_color(255)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(45)
    for row in data:
        is_last = row[0] == data[-1][0]
        pdf.set_font("dejavu", "B" if is_last else "", 8)
        if is_last:
            pdf.set_fill_color(255, 240, 240)
        for i, val in enumerate(row):
            pdf.cell(col_w[i], 6, val, border=1, fill=is_last, align="C")
        pdf.ln()
    pdf.ln(6)

# National data
pdf.set_font("dejavu", "B", 14)
pdf.set_text_color(0, 104, 157)
pdf.cell(0, 10, "Datos Nacionales por Año", new_x="LMARGIN", new_y="NEXT")

draw_table(
    ["Año", "Tránsito", "Motociclistas", "Peatones", "Vehículo", "Ciclistas"],
    [
        ["2015", "16,645", "1,541", "4,765", "3,159", "267"],
        ["2016", "16,761", "1,844", "4,559", "3,211", "280"],
        ["2017", "16,419", "1,935", "4,017", "3,046", "253"],
        ["2018", "16,035", "1,890", "3,753", "2,656", "220"],
        ["2019", "15,156", "1,948", "3,294", "2,304", "205"],
        ["2020", "14,020", "1,986", "2,642", "1,992", "177"],
        ["2021", "15,119", "2,244", "2,732", "2,335", "155"],
        ["2022", "16,414", "2,481", "2,844", "2,254", "158"],
        ["2023", "17,280", "2,885", "3,104", "2,159", "190"],
    ],
    [20, 30, 35, 28, 30, 27]
)

# Motorcyclists detail
pdf.set_font("dejavu", "B", 14)
pdf.set_text_color(0, 104, 157)
pdf.cell(0, 10, "Motociclistas: Perfil Demográfico", new_x="LMARGIN", new_y="NEXT")

draw_table(
    ["Año", "Total", "Hombres", "Mujeres", "Jóvenes 15-29"],
    [
        ["2015", "1,541", "1,397", "144", "867"],
        ["2016", "1,844", "1,654", "190", "1,013"],
        ["2017", "1,935", "1,760", "175", "1,128"],
        ["2018", "1,890", "1,704", "186", "1,040"],
        ["2019", "1,948", "1,763", "185", "1,027"],
        ["2020", "1,986", "1,789", "197", "1,082"],
        ["2021", "2,244", "2,000", "244", "1,183"],
        ["2022", "2,481", "2,205", "276", "1,268"],
        ["2023", "2,885", "2,585", "300", "1,449"],
    ],
    [25, 30, 30, 30, 35]
)

# Top 10 states
pdf.set_font("dejavu", "B", 14)
pdf.set_text_color(0, 104, 157)
pdf.cell(0, 10, "Top 10 Estados — Mortalidad Vial 2023", new_x="LMARGIN", new_y="NEXT")

draw_table(
    ["#", "Estado", "Defunciones"],
    [
        ["1", "Jalisco", "1,341"], ["2", "Guanajuato", "1,183"],
        ["3", "México", "866"], ["4", "Chihuahua", "838"],
        ["5", "Michoacán", "825"], ["6", "Ciudad de México", "816"],
        ["7", "Oaxaca", "723"], ["8", "Puebla", "697"],
        ["9", "Chiapas", "669"], ["10", "San Luis Potosí", "620"],
    ],
    [15, 50, 35]
)

# Infographics
img_dir = "assets"
images = sorted([f for f in os.listdir(img_dir) if f.endswith(".png")])

pdf.add_page()
pdf.set_font("dejavu", "B", 14)
pdf.set_text_color(0, 104, 157)
pdf.cell(0, 10, "Infografías", new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)

for img_file in images:
    img_path = os.path.join(img_dir, img_file)
    try:
        if pdf.get_y() > 160:
            pdf.add_page()
        pdf.image(img_path, x=15, w=180)
        pdf.ln(8)
    except Exception as e:
        print(f"Skipped {img_file}: {e}")

# Source
pdf.ln(10)
pdf.set_font("dejavu", "I", 9)
pdf.set_text_color(100)
pdf.multi_cell(0, 5, "Fuente: INEGI, Estadísticas de Defunciones Registradas 2015-2023.\nAnálisis: Dr. Arturo Cervantes Trejo, ANASEVI.\nObservatorio de Seguridad Vial — observatoriovial.mx")

output = "assets/policy-brief-motociclistas-2024.pdf"
pdf.output(output)
print(f"PDF generated: {output} ({os.path.getsize(output):,} bytes)")
