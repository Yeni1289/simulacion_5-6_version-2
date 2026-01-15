import os
import json
import base64
from pathlib import Path
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

try:
    from nbformat import read as nb_read
    from nbformat import NO_CONVERT
except ImportError:
    nb_read = None
    NO_CONVERT = 4

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_NOTES_DIR = BASE_DIR / 'templates' / 'notebooks'
STATIC_NOTES_DIR = BASE_DIR / 'static' / 'notebooks'

# Crear directorios si no existen
TEMPLATES_NOTES_DIR.mkdir(parents=True, exist_ok=True)
STATIC_NOTES_DIR.mkdir(parents=True, exist_ok=True)


def loader_view(request):
    """Pantalla inicial para cargar datasets"""
    # Intentar obtener la última ruta usada de la sesión
    last_path = request.session.get('last_dataset_path', '')
    
    # Asegurar que el CSRF cookie esté configurado
    from django.middleware.csrf import get_token
    get_token(request)
    
    # Usar versión simple sin CSS complejo
    return render(request, 'loader_simple.html', {'last_path': last_path})


def browse_notebooks(request):
    """Vista para navegar notebooks ya cargados"""
    notebooks = []
    
    # Buscar todos los JSON procesados
    if TEMPLATES_NOTES_DIR.exists():
        for json_file in TEMPLATES_NOTES_DIR.glob('*.json'):
            slug = json_file.stem
            
            # Buscar thumbnail
            thumb_dir = STATIC_NOTES_DIR / slug
            thumbnail = None
            if thumb_dir.exists():
                for ext in ['.png', '.jpg', '.jpeg', '.svg']:
                    thumb_files = list(thumb_dir.glob(f'*{ext}'))
                    if thumb_files:
                        thumbnail = f'/static/notebooks/{slug}/{thumb_files[0].name}'
                        break
            
            # Leer preview del JSON
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    preview = data[0].get('content', '')[:200] if data else ''
            except:
                preview = ''
            
            notebooks.append({
                'slug': slug,
                'title': slug.replace('_', ' ').replace('-', ' '),
                'thumbnail': thumbnail,
                'preview': preview
            })
    
    return render(request, 'browse.html', {'notebooks': notebooks})


@csrf_exempt
@require_http_methods(["POST"])
def scan_folder(request):
    """API para escanear carpeta y encontrar notebooks"""
    try:
        folder_path = request.POST.get('folder_path', '')
        
        print(f"📁 Ruta recibida: {folder_path}")
        print(f"🔍 ¿Existe? {os.path.exists(folder_path)}")
        
        if not folder_path:
            return JsonResponse({
                'success': False,
                'error': 'No se proporcionó una ruta'
            })
            
        if not os.path.exists(folder_path):
            return JsonResponse({
                'success': False,
                'error': f'La carpeta no existe: {folder_path}'
            })
        
        # Guardar en sesión
        request.session['last_dataset_path'] = folder_path
        
        # Buscar archivos .ipynb
        notebooks = []
        folder = Path(folder_path)
        
        print(f"🔎 Buscando en: {folder}")
        
        for nb_file in folder.glob('*.ipynb'):
            if '.ipynb_checkpoints' in str(nb_file):
                continue
            
            print(f"  ✓ Encontrado: {nb_file.name}")
            notebooks.append({
                'name': nb_file.name,
                'path': str(nb_file),
                'size': nb_file.stat().st_size,
                'slug': nb_file.stem
            })
        
        print(f"📊 Total notebooks: {len(notebooks)}")
        
        return JsonResponse({
            'success': True,
            'notebooks': notebooks,
            'folder': str(folder)
        })
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@csrf_exempt
@require_http_methods(["POST"])
def process_notebook(request):
    """API para procesar un notebook y extraer contenido importante"""
    try:
        nb_path = request.POST.get('notebook_path', '')
        
        if not nb_path or not os.path.exists(nb_path):
            return JsonResponse({
                'success': False,
                'error': 'Notebook no encontrado'
            })
        
        if not nb_read:
            return JsonResponse({
                'success': False,
                'error': 'nbformat no está instalado'
            })
        
        # Leer notebook
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nb_read(f, as_version=NO_CONVERT)
        
        slug = Path(nb_path).stem
        static_dir = STATIC_NOTES_DIR / slug
        static_dir.mkdir(parents=True, exist_ok=True)
        
        # Extraer solo contenido importante
        items = []
        img_counter = 0
        
        for cell in nb.cells:
            # Markdown (solo títulos y párrafos importantes)
            if cell.cell_type == 'markdown':
                content = ''.join(cell.source) if isinstance(cell.source, list) else cell.source
                if content.strip():
                    # Filtrar markdown muy básico
                    if len(content) > 20 or content.startswith('#'):
                        items.append({
                            'type': 'markdown',
                            'content': content
                        })
            
            # Code cells - solo outputs importantes
            elif cell.cell_type == 'code' and hasattr(cell, 'outputs'):
                for output in cell.outputs:
                    # Imágenes (PRIORIDAD)
                    if hasattr(output, 'data'):
                        if 'image/png' in output.data:
                            img_counter += 1
                            img_filename = f'viz_{img_counter}.png'
                            img_path = static_dir / img_filename
                            
                            img_data = base64.b64decode(output.data['image/png'])
                            img_path.write_bytes(img_data)
                            
                            items.append({
                                'type': 'image',
                                'content': f'/static/notebooks/{slug}/{img_filename}',
                                'index': img_counter
                            })
                        
                        # Tablas HTML (datos importantes)
                        elif 'text/html' in output.data:
                            html_content = ''.join(output.data['text/html']) if isinstance(output.data['text/html'], list) else output.data['text/html']
                            if 'table' in html_content.lower() or 'dataframe' in html_content.lower():
                                items.append({
                                    'type': 'table',
                                    'content': html_content
                                })
                    
                    # Texto de salida (solo si es resultado importante)
                    elif hasattr(output, 'text'):
                        text = ''.join(output.text) if isinstance(output.text, list) else output.text
                        # Filtrar outputs triviales
                        if text.strip() and len(text) < 5000:
                            # Solo si parece resultado importante
                            if any(keyword in text.lower() for keyword in ['accuracy', 'score', 'result', 'mean', 'std', 'count', ':']):
                                items.append({
                                    'type': 'output',
                                    'content': text
                                })
        
        # Guardar JSON
        json_path = TEMPLATES_NOTES_DIR / f'{slug}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        
        return JsonResponse({
            'success': True,
            'slug': slug,
            'items_count': len(items),
            'images_count': img_counter
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def notebook_detail(request, slug):
    """Vista detallada del notebook procesado"""
    json_path = TEMPLATES_NOTES_DIR / f'{slug}.json'
    
    if not json_path.exists():
        from django.http import Http404
        raise Http404('Notebook no encontrado')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)
    
    # Extraer estadísticas y listas separadas
    images = [item for item in items if item['type'] == 'image']
    tables = [item for item in items if item['type'] == 'table']
    outputs = [item for item in items if item['type'] == 'output']
    
    stats = {
        'total': len(items),
        'images': len(images),
        'tables': len(tables),
        'outputs': len(outputs),
        'total_cells': len(items),
        'code_cells': sum(1 for item in items if item.get('type') == 'code')
    }
    
    # Extraer título del primer markdown
    title = slug.replace('_', ' ').replace('-', ' ').title()
    description = ''
    
    for item in items:
        if item['type'] == 'markdown':
            content = item['content']
            if content.startswith('#'):
                title = content.lstrip('#').strip()
            else:
                description = content[:300]
            break
    
    # Detectar si es el notebook de Regresión Logística
    if '05_Regrecion_Loguistica' in slug or 'regresion' in slug.lower():
        return render(request, 'regresion_logistica_interactive.html')
    
    # Detectar si es el notebook de Visualización de DataSet
    if '06_Visualizacion_DtaSet' in slug or 'visualizacion' in slug.lower():
        return render(request, 'visualizacion_dataset_interactive.html')
    
    # Detectar si es el notebook de División del DataSet
    if '07_Divicion_del_DataSet' in slug or 'divicion' in slug.lower() or 'division' in slug.lower():
        return render(request, 'division_dataset_interactive.html')
    
    # Detectar si es el notebook de Preparación del DataSet
    if '08_Preparacion_del_DataSet' in slug or 'preparacion' in slug.lower():
        return render(request, 'preparacion_dataset_interactive.html')
    
    # Detectar si es el notebook de Transformadores y Pipelines Personalizados
    if '09_Creacion-de-Transformadores-y-Pipeline-Personalizados' in slug or 'transformadores' in slug.lower() or 'pipelines' in slug.lower() or 'creacion' in slug.lower():
        return render(request, 'pipelines_transformadores_interactive.html')
    
    # Detectar si es el notebook de Evaluación de Resultados
    if '10_Evalucion-de-Resultados' in slug or 'evaluacion' in slug.lower() or 'evalucion' in slug.lower():
        return render(request, 'evaluacion_resultados_interactive.html')
    
    return render(request, 'notebook_detail_interactive.html', {
        'slug': slug,
        'title': title,
        'description': description,
        'items': items,
        'stats': stats,
        'images': images,
        'tables': tables,
        'outputs': outputs
    })
