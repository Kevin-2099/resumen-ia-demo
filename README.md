# 📚 Resumen Inteligente de Documentos con IA (resumen-ia-demo)
Este es un proyecto educativo de Micro SaaS que permite subir documentos PDF y obtener un resumen automático generado con IA (modelo BART de Facebook).
> ⚠️ Este proyecto es un demo **sin fines comerciales**. Su propósito es **formativo y educativo**.

## 👨‍💻 Tecnologías usadas
- Python
- Hugging Face Transformers
- Gradio
- pdfplumber

## 🚀 Demo en vivo
👉 [Ver la demo en Hugging Face](https://huggingface.co/spaces/Kevin-2099/resumen-ia-demo)

## 📂 Cómo usar localmente
1.Clona el repositorio:

git clone https://github.com/Kevin-2099/resumen-ia-demo.git

cd resumen-ia-demo

2.Instala las dependencias:

pip install -r requirements.txt

-Si no tienes requirements.txt, puedes usar:

pip install transformers pdfplumber gradio

3.Ejecuta la aplicación:

python app.py


## 📌 Características
✅ Subida de archivos PDF

✅ Extracción de texto con pdfplumber

✅ Generación de resumen con modelo BART

✅ Interfaz amigable usando Gradio

✅ Detección automática de idioma (español/inglés) 🌐

✅ Barra de progreso durante el procesamiento ⏳

✅ Estadísticas rápidas: número de páginas, palabras originales y palabras del resumen 📊

✅ Fácil de ejecutar localmente o en la nube (Hugging Face Spaces)

## 🧠 Autor
Proyecto desarrollado como parte de la formación técnica en IA de un estudiante de 16 años interesado en productos digitales, SaaS y tecnologías generativas.
