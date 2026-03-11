# Clarity Studio 💎

Clarity Studio es una herramienta web profesional impulsada por IA para el procesamiento de logos. Permite redimensionar imágenes y eliminar fondos automáticamente para crear transparencias perfectas (PNG).

## 🚀 Características
- **Eliminación de fondo con IA**: Utiliza el motor `rembg` para detectar y remover fondos de logos con alta precisión.
- **Redimensionamiento inteligente**: Ajusta alto y ancho manteniendo la relación de aspecto si se desea.
- **Interfaz Premium**: Diseño moderno con Glassmorphism, animaciones y modo oscuro.
- **Privacidad**: Procesamiento local rápido y seguro.

## 🛠️ Tecnologías
- **Backend**: Python 3.x, Flask
- **Procesamiento de imagen**: Pillow (PIL), rembg (ONNX Runtime)
- **Frontend**: HTML5, Vanilla CSS, JavaScript

## 📦 Instalación y Ejecución Local

Si acabas de clonar este repositorio, sigue estos pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/clarity-studio.git
   cd clarity-studio
   ```

2. **Crear un entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Mac/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```

5. **Abrir en el navegador:**
   Accede a `http://127.0.0.1:5000`

## 🌐 Despliegue en Render.com

Para poner Clarity Studio online:

1. **Crea una cuenta** en [Render.com](https://render.com/).
2. **Crea un nuevo "Web Service"** y conecta tu repositorio de GitHub.
3. Configura los siguientes campos:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. En la pestaña **Environment**, asegúrate de que el puerto se asigne automáticamente (Render lo hace por defecto).

> [!IMPORTANT]
> Debido a que la IA utiliza modelos de procesamiento, el primer arranque puede tardar un poco mientras se configuran las dependencias.

---
Desarrollado con ❤️ para Clarity Studio.
