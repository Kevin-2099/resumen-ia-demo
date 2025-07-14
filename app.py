
# ============================================
# Instalar dependencias (Colab o Spaces)
# ============================================

!pip install transformers pdfplumber gradio --quiet

# ============================================
# Importar librerías
# ============================================

from transformers import pipeline
import pdfplumber
import gradio as gr
import csv
import os
from datetime import datetime

# ============================================
# Cargar modelo Hugging Face
# ============================================

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# ============================================
# Guardar logs de resúmenes generados
# ============================================

def guardar_log(nombre_archivo, resumen):
    nombre_log = "resumenes_log.csv"
    resumen_corto = resumen[:120].replace("
", " ")
    fila = [datetime.now().isoformat(), nombre_archivo, resumen_corto]
    existe = os.path.isfile(nombre_log)
    with open(nombre_log, mode="a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not existe:
            writer.writerow(["fecha", "archivo", "resumen"])
        writer.writerow(fila)

# ============================================
# Función principal para resumir PDFs
# ============================================

def resumir_archivo(archivo):
    texto = ""
    try:
        with pdfplumber.open(archivo.name) as pdf:
            for pagina in pdf.pages[:10]:  # Limitar a 10 páginas
                contenido = pagina.extract_text()
                if contenido:
                    texto += contenido + "
"
    except:
        return "❌ Error: No se pudo procesar el archivo PDF."

    texto = texto.replace("
", " ").strip()
    if len(texto) < 300:
        return "❌ El documento es demasiado corto para generar un resumen."

    # Dividir texto en chunks
    chunks = [texto[i:i+700] for i in range(0, len(texto), 700)][:5]  # Máx 5 chunks
    resumenes = summarizer(chunks, max_length=100, min_length=30, do_sample=False)
    resumen_total = "
".join([r['summary_text'] for r in resumenes])

    with open("resumen_salida.txt", "w", encoding="utf-8") as f:
        f.write(resumen_total)

    guardar_log(archivo.name, resumen_total)
    return resumen_total, "resumen_salida.txt"

# ============================================
# Interfaz visual con Gradio
# ============================================

interface = gr.Interface(
    fn=resumir_archivo,
    inputs=gr.File(label="📄 Sube tu documento PDF (en español o inglés)"),
    outputs=[
        gr.Textbox(label="🧠 Resumen generado por IA"),
        gr.File(label="⬇️ Descargar resumen")
    ],
    title="📚 Resumen Inteligente de Documentos con IA",
    description="Sube un documento PDF y obtén un resumen automático de alta calidad usando el modelo BART de Facebook.",
    theme="compact"
)

# ============================================
# Lanzar la app (Colab o Hugging Face Spaces)
# ============================================

interface.launch(share=True)

