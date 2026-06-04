# Document Generator Service

**Archivo**: `app/services/document_generator.py`

## Proposito

Toma el contenido generado (por Gemini o fallback) y produce un archivo `.docx` formateado.

## Como funciona

1. Busca `base_documento.py` en `data/skills/`
2. Si existe, lo importa dinamicamente (`importlib.util.spec_from_file_location`) y usa sus funciones para crear el documento con formato APA 7
3. Si no existe, usa `python-docx` directamente con formato basico

## Formato con base_documento.py

`base_documento.py` es una skill **oculta** (no aparece en `list_skills()`) que proporciona:

- Configuracion de pagina: tamanio carta (21.59x27.94 cm), margenes APA (2.54 top/bottom, 3.0 left, 2.54 right)
- Estilos: Normal (Arial 12, justificado, interlineado 1.5, sangria 1.25cm), Heading 2 y 3 con estilos APA
- Caratula institucional con logo, facultad, carrera, titulo, autor, tutor
  - Campos vacios muestran `(llenar campo)` como placeholder
  - Sin espacios excesivos en el margen superior (solo 1 salto de linea)
- Tabla de contenidos (TOC) automatica con campo `TOC \o "1-3"` (actualizable con clic derecho en Word)
- Numeracion de pagina automatica
- Formato APA para referencias bibliograficas
- Tablas con bordes estilo APA (`add_table_with_data()`)

## Formato sin base_documento.py

- Titulo centrado en negrita
- Autor y tutor centrados
- Contenido en Arial 12pt

## Renderizado de contenido

El contenido Markdown generado por Gemini se parsea linea por linea:

| Elemento Markdown | Accion en .docx |
|---|---|
| `# Titulo` | Heading 2 (estilo APA) |
| `## Subtitulo` | Heading 3 (estilo APA) |
| `- item` | Lista con viñetas |
| `1. item` | Lista numerada |
| `**texto**` | Negrita |
| `*texto*` | Cursiva |
| `| tabla |` | Tabla con bordes APA |
| Parrafo normal | Justificado, sangria 1.25cm |

El documento generado incluye:
1. **Caratula** con datos institucionales
2. **Tabla de Contenidos** (campo TOC, actualizable en Word)
3. **Contenido** estructurado segun la skill seleccionada
4. **Encabezados** con numeracion de pagina

No se agrega ningun titulo generico (como "CONTENIDO GENERADO") antes del contenido.

## Salida

Los documentos se guardan en `data/output/` con el formato `{titulo}_{primeros_50_caracteres}.docx`.

## Dependencias

- `python-docx` (python-docx)
- `base_documento.py` (skill oculta, formato APA 7)
- `importlib` (carga dinamica del modulo base)
