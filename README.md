# 📊 Notebook Viewer - Visualización Interactiva de Jupyter Notebooks

Aplicación web moderna para visualizar notebooks de Jupyter de forma interactiva y estructurada. Diseñada para presentar análisis de datos de manera profesional sin el aspecto básico de HTML.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

## ✨ Características

- 🎨 **Interfaz Moderna**: Diseño elegante con animaciones y efectos visuales
- 📁 **Carga de Datasets**: Arrastra y suelta carpetas o ingresa rutas
- 🔍 **Exploración Inteligente**: Escaneo automático de notebooks
- 📊 **4 Vistas Organizadas**: 
  - Resumen General
  - Visualizaciones (gráficos e imágenes)
  - Datos (tablas y salidas)
  - Insights (conclusiones)
- 🌓 **Tema Oscuro/Claro**: Cambia entre modos según tu preferencia
- 🖼️ **Lightbox para Imágenes**: Amplía imágenes con zoom
- 📱 **Diseño Responsivo**: Funciona en desktop, tablet y móvil
- 🚀 **Rápido y Eficiente**: Sin necesidad de ejecutar kernels

## 🚀 Inicio Rápido

### Desarrollo Local

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Yeni1289/simulacion_5-6_version-2.git
   cd simulacion_5-6_version-2
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar base de datos**
   ```bash
   python manage.py migrate
   ```

4. **Iniciar servidor** (Windows)
   ```bash
   INICIAR.bat
   ```
   
   O manualmente:
   ```bash
   python manage.py runserver
   ```

5. **Abrir en navegador**
   ```
   http://localhost:8000
   ```

### 🚂 Deploy en Railway

1. **Fork este repositorio**

2. **Crear nuevo proyecto en Railway**
   - Ve a [Railway](https://railway.app)
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Selecciona tu fork

3. **Variables de entorno** (opcional)
   ```
   SECRET_KEY=tu-clave-secreta-aqui
   DEBUG=False
   ```

4. **Deploy automático** 
   - Railway detectará automáticamente la configuración
   - El proyecto se desplegará en pocos minutos

## 📋 Requisitos

- Python 3.12+
- Django 4.2+
- nbformat 5.9+
- markdown 3.4+
- gunicorn 21.2+
- whitenoise 6.6+

## 🎯 Uso

1. **Cargar Dataset**
   - Ingresa la ruta de tu carpeta de notebooks
   - O arrastra la carpeta directamente

2. **Explorar Notebooks**
   - Se mostrarán todos los archivos `.ipynb` encontrados
   - Click en "Abrir" para visualizar

3. **Navegar Contenido**
   - Usa la barra lateral para cambiar entre vistas
   - Click en imágenes para ampliar
   - Exporta contenido si es necesario

## 🏗️ Estructura del Proyecto

```
proyecto-simulacion-ml/
├── app/                    # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── viewer/                 # App principal
│   ├── views.py           # Lógica de vistas
│   └── urls.py            # Rutas
├── templates/             # Templates HTML
│   ├── loader.html        # Pantalla de carga
│   └── notebook_detail.html  # Visor de notebooks
├── static/                # Archivos estáticos
│   └── css/
│       └── app.css        # Estilos principales
├── datasets/              # Notebooks de ejemplo
├── requirements.txt       # Dependencias
├── Procfile              # Configuración Railway
├── railway.json          # Config Railway
└── runtime.txt           # Versión de Python
```

## 🛠️ Tecnologías

- **Backend**: Django 5.2.7
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Processing**: nbformat para parsear notebooks
- **Deployment**: Railway, Gunicorn, WhiteNoise
- **Database**: SQLite (desarrollo), PostgreSQL (producción)

## 🐛 Solución de Problemas

### No encuentra notebooks
- Verifica que la ruta sea correcta
- Los archivos deben estar en la carpeta raíz, no en subcarpetas
- Deben tener extensión `.ipynb`

### Error de sesiones
```bash
python manage.py migrate
```

### Imágenes no se muestran
- Las imágenes deben estar embebidas en base64 en el notebook
- O usar rutas relativas

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## 👥 Autor

**Yeni** - [GitHub](https://github.com/Yeni1289)

## 🙏 Agradecimientos

- Diseñado para el curso de Simulación
- Inspirado en Jupyter Notebook y Google Colab
- UI/UX moderno y minimalista

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub!
