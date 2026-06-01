# Componentes UI

Los estilos estan en `app/static/css/style.css` y la logica en `app/static/js/app.js`.

## Variables CSS (tema oscuro)

| Variable | Valor | Uso |
|---|---|---|
| `--bg` | `#000` | Fondo general |
| `--surface` | `#0a0a0a` | Superficies (header, sidebar, input-area) |
| `--surface2` | `#111` | Superficie secundaria (hover, modals) |
| `--surface3` | `#1a1a1a` | Superficie terciaria (tooltips) |
| `--border` | `#222` | Bordes |
| `--text` | `#e0e0e0` | Texto principal |
| `--text2` | `#888` | Texto secundario |
| `--text3` | `#555` | Texto terciario / placeholder |
| `--accent` | `#22c55e` | Verde acento (boton send, links, hover) |
| `--accent2` | `#16a34a` | Verde acento hover |
| `--blue` | `#3b82f6` | Archivos / documentos |
| `--purple` | `#a855f7` | Skills |
| `--orange` | `#f97316` | Documentos generados |
| `--green` | `var(--accent)` | Boton Generar |
| `--danger` | `#ef4444` | Errores |
| `--warn` | `#f59e0b` | Advertencias |

## Layout general

```
.app (flex column, 100vh)
├── .header (48px, fixed height)
│   ├── .logo "docgent"
│   ├── .header-actions
│   │   └── .donate-btn "❤️ Doname"
│   └── .status (dot verde + "listo")
├── .body (flex row, flex: 1)
│   ├── .main (flex column, flex:1)
│   │   ├── .workspace (flex:1, scroll)
│   │   │   └── .entry (mensajes)
│   │   └── .input-area (fixed bottom)
│   │       ├── .input-row
│   │       │   ├── .input-wrap > textarea
│   │       │   └── .btn-send
│   │       └── .input-actions
│   │           ├── .circle-btn (Documentos - azul)
│   │           ├── .circle-btn (Skill - purpura)
│   │           └── .circle-btn.generate-btn (Generar - verde)
│   └── .sidebar (280px, right side)
│       ├── caratula (titulo, autor, tutor)
│       ├── demo (Documento .docx prueba)
│       ├── recursos (counters)
│       ├── skills (quick list)
│       ├── acciones (nueva skill, subir archivo, api keys)
│       └── gemini key status
```

## Circle Buttons (input-actions)

Tres circulos retractiles debajo del input:

| Boton | Clase | Color punto | Accion |
|---|---|---|---|
| Documentos | `.circle-btn` | `--blue` | Subir archivos |
| Skill | `.circle-btn` | `--purple` | Seleccionar skill |
| Generar | `.circle-btn.generate-btn` | `--accent` (verde) | Genera documento directo con busqueda web |

### Estados

| Estado | Clase CSS | Apariencia | Comportamiento |
|---|---|---|---|
| Contraido | `.circle-btn` | Circulo de 36px, borde `--border`, fondo `--surface2`, punto de color | Tooltip en hover |
| Hover | `.circle-btn:hover` | Borde `--accent`, punto se vuelve verde | Tooltip visible |
| Expandido | `.circle-btn.expanded` | Rectangulo `auto` con padding, radio 8px, gap 8px | Label visible, sin tooltip |
| Drag-over | `.circle-btn.drag-over` | Borde `--accent`, fondo `--accent`, punto negro | Solo en boton Documentos |

El boton **Generar** (`.generate-btn`) tiene borde verde siempre, y al expandirse ejecuta directamente la generacion del documento.

### Tooltip

- Posicion: `left: calc(100% + 10px)`, centrado vertical
- Fondo: `--surface3`, borde `--border`
- Visibilidad: `opacity: 1` en hover del `.circle-btn`
- Oculto: cuando `.circle-btn` tiene clase `.expanded`

### Auto-collapse

- Al expandirse, se colapsa solo despues de **5 segundos**
- Si se hace clic antes, se ejecuta la accion y se cancela el timeout
- Al expandir uno, se colapsan los otros automaticamente

## Boton Send

- 42x42px, borde redondeado 8px
- Fondo: `--accent`, hover: `--accent2`
- Texto: `~>` en negro

## Input textarea

- Fondo: `--surface2`, borde `--border`
- Focus: borde `--accent`
- Placeholder: `--text3`
- Auto-resize: min 44px, max 120px
- Enter envia, Shift+Enter nueva linea

## Entries / Mensajes (workspace)

### Tipos de entrada

| Clase | Color borde izquierdo | tag |
|---|---|---|
| `.entry.system` | `--text3` | DOCGENT / TU |
| `.entry.file` | `--blue` | ARCHIVO |
| `.entry.skill` | `--purple` | SKILL |
| `.entry.doc` | `--orange` | DOC |
| `.entry.error` | `--danger` | ERROR |

### Estructura

```html
<div class="entry system">
  <div class="entry-header">
    <span class="entry-tag">DOCGENT</span>
    <span class="entry-title">titulo opcional</span>
    <span class="entry-time">ahora</span>
  </div>
  <div class="entry-body markdown-body">
    <p>contenido renderizado como markdown</p>
  </div>
</div>
```

## Modals

| Modal | ID | Proposito |
|---|---|---|
| Nueva skill | `#modalOverlay` | Crear skill (nombre, descripcion, tipo, contenido + drag & drop) |
| Editar skill | `#editSkillOverlay` | Editar / eliminar skill existente |
| API Keys | `#apiKeysOverlay` | Gestion de hasta 4 keys Gemini (input password + persistencia) |
| Seleccionar skill | `#skillSelectOverlay` | Lista visual de skills |
| Generar doc | `#genModal` | Titulo, autor, tutor, instrucciones adicionales |
| Bienvenida | `#welcomeOverlay` | Pantalla de bienvenida al cargar la app |
| Donacion | `#donateOverlay` | QR de criptomonedas para donar (Bitcoin, Polygon, BNB) |
| Vista Previa | `#previewOverlay` | Preview del .docx generado (parrafos + tablas) |

Todos los modals comparten:
- Overlay: `position: fixed`, fondo `rgba(0,0,0,.85)`
- Content: `max-width: 540px`, borde `--border`, fondo `--surface2`
- Boton primary: fondo `--accent`, texto negro
- Boton ghost: transparente, borde `--border`

## Lightbox

- ID: `#lightbox`
- Visor de imagenes a pantalla completa
- Se activa al hacer click en los QR de donacion
- Auto-cierra a los 30 segundos
- Click en cualquier lado o boton X para cerrar

## Caratula (sidebar)

Seccion en el sidebar con 3 campos de texto:
- Titulo del documento
- Autor
- Tutor

Los datos se guardan en `sessionStorage` y se envian como header `X-Caratula` en cada peticion de chat.

## Documento Demo (sidebar)

Seccion "demo" con enlace "▶ Documento .docx prueba". Al hacer clic:
1. Llama a `POST /api/documents/generate-demo`
2. Genera un documento con: caratula UNIFRANZ, tabla de contenidos, encabezados nivel 2 y 3, tablas (6x4), listas con viñetas, listas numeradas, **negritas**, *cursivas*, formato mixto, referencias APA, numeracion de pagina
3. Muestra botones "descargar .docx" y "visualizar" como cualquier documento generado

## Donate Button (header)

- Texto: `❤️ Doname`
- Abre `#donateOverlay` con QR de 3 criptomonedas
- Cada QR se puede ampliar en el lightbox

## Animaciones

- Entrada de mensajes: `fadeIn` (0.2s, translateY 4px → 0)
- Dot verde del header: `pulse` (opacity 1 ↔ 0.3, 2s infinite)
- Transiciones suaves en hover de botones, sidebar items, modals (0.12s-0.15s)

## Responsive (max-width: 800px)

- `.body` cambia a columna
- `.sidebar` pasa abajo, 120px max-height, horizontal scroll
- Sidebar groups en fila con flex-wrap

## Sidebar Accordion

Todas las secciones del sidebar (excepto la version) son acordeón retráctil:

- Click en el `<h3>` de cualquier sección la expande/contrae
- Icono `+` cuando cerrado, `−` cuando abierto
- Solo una sección abierta a la vez (la anterior se cierra automáticamente)
- Sección **recursos** abierta por defecto; las demás cerradas
- Función `toggleSection(h3)` en `app.js`
- Variable global `activeSection` rastrea la sección abierta actual

```css
.collapse-content{max-height:0;overflow:hidden;transition:max-height .25s ease}
.collapse-content.open{max-height:400px}
```

## GIF Decorativo

- Sección `.sidebar-gif` al final del sidebar, debajo de todas las secciones
- Muestra un GIF animado de Giphy
- Hover muestra overlay "cambiar gif"
- Al hacer clik, `changeGif()` pide un enlace de Giphy (sugiere `giphy.com/search/anime`)
- El GIF seleccionado se guarda en `localStorage` (clave `sidebar_gif_url`)
- Se restaura automáticamente al cargar la app via `loadGif()`
- En responsive (<800px) se oculta

## Sidebar

- 280px fijo, borde izquierdo
- Grupos: recursos, skills, acciones, caratula, gemini keys, demo, gif
- Items clickables tienen clase `.clickable`
- Skill seleccionada tiene clase `.active` (fondo `--surface2`, color `--accent`)

## Scrollbar

Color personalizado `#99606E` (rosa) en todo el sistema para mejor visibilidad en modales y paneles:
