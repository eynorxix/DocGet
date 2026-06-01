# Comandos de la interfaz

## Comandos por texto

Escribe en el input y presiona Enter:

| Comando | Accion |
|---|---|
| `subir archivo` | Abre el selector de archivos para subir |
| `nueva skill` o `crear skill` | Abre el modal para crear una skill |
| `skills` o `listar skills` | Muestra las skills disponibles en el workspace |
| `generar` o `documento` | Abre el modal para generar un .docx |
| `ayuda` o `help` | Muestra la lista de comandos |
| `[nombre de skill]` | Selecciona una skill por su nombre (coincidencia parcial) |

## Acciones por click

### Sidebar (derecha)
- **Skills**: Click en cualquier skill para seleccionarla
- **"+ nueva skill"**: Abre modal de creacion
- **"+ subir archivo"**: Abre selector de archivos

### Botones en entradas
- **"generar documento"**: Aparece al seleccionar una skill, abre el modal de generacion
- **"descargar .docx"**: Aparece cuando un documento se genera, descarga el archivo

## Modal de crear skill

Campos:
- **Nombre** (requerido): Identificador de la skill
- **Descripcion**: Para que sirve
- **Tipo**: md, py o txt
- **Contenido** (requerido): Estructura del documento en Markdown o Python

## Modal de generar documento

Antes de abrir este modal, debe haber una skill seleccionada.

Campos:
- **Skill**: Muestra la skill seleccionada (solo lectura)
- **Titulo** (requerido): Titulo del documento
- **Autor**: Nombre del autor
- **Tutor**: Nombre del tutor
- **Instrucciones adicionales**: Texto libre para que la IA personalice el contenido
