# Interfaz de usuario

## Layout

```
+--------------------------------------------------+
| docgent          [❤️ Doname]     [status]          |  <- Header
+----------------------------+---------------------+
|                            | Sidebar (derecha)    |
|   Workspace principal      |                      |
|                            | [−] recursos         |
|   [DOCGENT] sistema listo  |   ~ archivos    3   |
|   [ARCHIVO] subido: x.md   |   # skills      4   |
|   [SKILL] creada: y        |   + documentos  1   |
|   [DOC] preview / descarga |                      |
|                            | [+] skills           |
|                            | [+] acciones         |
|                            | [+] carátula         |
|                            | [+] gemini keys      |
|                            | [+] demo             |
|                            |                      |
|                            | [GIF animado]        |
|                            |  (hover: cambiar)    |
|                            |                      |
|                            | docgent v1           |
+----------------------------+---------------------+
| [ > Escribe... ] [~>]                             |  <- Input
|   (●) Documentos  (●) Skill  (●) Generar          |  <- Botones
+--------------------------------------------------+
```

## Componentes

### Header
- Barra superior fina con logo `docgent`, boton `❤️ Doname` y estado `listo`

### Sidebar (derecha)
Todas las secciones son **acordeón retráctil**: click en el header para expandir/contraer.
- `[−]` = sección abierta, `[+]` = sección cerrada
- Solo una sección abierta a la vez (la anterior se cierra automáticamente)
- **recursos**: abierto por defecto. Contadores de archivos, skills y documentos generados
- **skills**: cerrado por defecto. Lista clicable de skills disponibles (max 8)
- **acciones**: cerrado por defecto. Accesos directos a crear skill, subir archivo, API keys
- **caratula**: cerrado por defecto. 3 campos (titulo, autor, tutor) que se guardan en `sessionStorage`
- **gemini keys**: cerrado por defecto. Estado de las keys configuradas
- **demo**: cerrado por defecto. Enlace "Documento .docx prueba"
- **GIF decorativo**: al final, debajo de las secciones. Al pasar el mouse aparece "cambiar gif" — permite pegar un enlace de Giphy (se guarda en localStorage)

### Workspace (centro)
- Area principal donde aparecen las entradas del sistema
- Cada entrada tiene un tag de color (DOCGENT, ARCHIVO, SKILL, DOCUMENTO, ERROR, AYUDA, TU, INFO)
- Las entradas son tipo "chat" o "log" cronologico
- El contenido se renderiza como Markdown (con soporte para tablas, listas, bold, etc.)

### Input (abajo)
- Campo de texto donde se escriben mensajes para el agente IA
- Boton `~>` para enviar
- Soporta Enter para enviar, Shift+Enter para nueva linea
- Debajo: **3 botones circulares**:
  - **Documentos** (azul): subir archivos
  - **Skill** (purpura): seleccionar skill
  - **Generar** (verde): genera documento directo con busqueda web, sin preguntas

## Comandos

El agente IA entiende lenguaje natural, no comandos fijos. Ejemplos de lo que puede hacer:

| Accion | Ejemplo |
|---|---|
| Crear skill | "crea una skill para informe de laboratorio" |
| Subir archivo | "necesito subir un archivo" |
| Generar documento | "genera un documento con la skill EstructuraIntegrador" |
| Listar skills | "que skills tengo?" |
| Seleccionar skill | "quiero ver la skill Humano" |
