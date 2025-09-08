# ============================================
# Importar librerías
# ============================================

from transformers import pipeline
import pdfplumber
import gradio as gr
import csv
import os
from datetime import datetime
from langdetect import detect

# ============================================
# Cargar modelo Hugging Face
# ============================================

resumidor = pipeline("summarization", model="facebook/bart-large-cnn")

# ============================================
# Guardar registros de resúmenes generados
# ============================================

def guardar_log(nombre_archivo, resumen, idioma):
    nombre_log = "resumenes_log.csv"
    resumen_corto = resumen[:120].replace("\n", " ")
    fila = [datetime.now().isoformat(), nombre_archivo, idioma, resumen_corto]
    existe = os.path.isfile(nombre_log)
    
    with open(nombre_log, mode="a", newline='', encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if not existe:
            escritor.writerow(["fecha", "archivo", "idioma", "resumen"])
        escritor.writerow(fila)

# ============================================
# Función principal para resumir PDF
# ============================================

def resumir_archivo(archivo, progreso=gr.Progress()):
    texto = ""
    num_paginas = 0
    try:
        with pdfplumber.open(archivo.name) as pdf:
            limite = min(10, len(pdf.pages))
            for i, pagina in enumerate(pdf.pages[:limite]):
                contenido = pagina.extract_text()
                if contenido:
                    texto += contenido + "\n"
                progreso((i+1) / limite)  # actualizar progreso
            num_paginas = limite
    except:
        return "❌ Error: No se pudo procesar el archivo PDF.", None

    texto = texto.replace("\n", " ").strip()
    if len(texto) < 300:
        return "❌ El documento es demasiado corto para generar un resumen.", None

    # Detectar idioma del texto
    try:
        idioma = detect(texto)
    except:
        idioma = "desconocido"

    # Dividir texto en fragmentos
    fragmentos = [texto[i:i+700] for i in range(0, len(texto), 700)][:5]  # Máximo 5 fragmentos
    resúmenes = resumidor(fragmentos, max_length=100, min_length=30, do_sample=False)
    resumen_total = " ".join([r["summary_text"] for r in resúmenes])

    # Limpiar texto
    resumen_total = " ".join(resumen_total.split())

    # Estadísticas
    palabras_originales = len(texto.split())
    palabras_resumen = len(resumen_total.split())
    estadisticas = f"\n\n📊 Estadísticas:\n- Páginas procesadas: {num_paginas}\n- Palabras originales: {palabras_originales}\n- Palabras en resumen: {palabras_resumen}"

    with open("resumen_salida.txt", "w", encoding="utf-8") as f:
        f.write(resumen_total + estadisticas)

    guardar_log(archivo.name, resumen_total, idioma)
    return f"🌐 Idioma detectado: {idioma.upper()}\n\n{resumen_total}{estadisticas}", "resumen_salida.txt"

# ============================================
# Interfaz visual con Gradio
# ============================================

interfaz = gr.Interface(
    fn=resumir_archivo,
    inputs=gr.File(label="📄 Sube tu documento PDF (en español o inglés)"),
    outputs=[
        gr.Textbox(label="🧠 Resumen generado por IA"),
        gr.File(label="⬇️ Descargar resumen")
    ],
    title="📚 Resumen Inteligente de Documentos con IA",
    description="Sube un documento PDF y obtén un resumen automático de alta calidad usando el modelo BART de Facebook. Ahora detecta idioma y muestra estadísticas.",
    theme="compact"
)

# ============================================
# Lanzar la aplicación
# ============================================

interfaz.launch(share=True)
