# Skill: Estructura de Documento Técnico (Microcontroladores)

## Descripción
Define la estructura de contenido específica para documentos técnicos de proyectos de microcontroladores/sistemas embebidos. Se aplica sobre el formato base APA 7 definido en `Skill.md`.

## Estructura del Documento (Orden Exacto)
El documento debe generarse siguiendo estrictamente esta secuencia de secciones. Utilizar `Heading 2` para cada título principal.

### 1. Título
- Título completo del proyecto.

### 2. Planteamiento del problema
- Descripción clara y concisa de la problemática que aborda el proyecto.

### 3. Importancia del Proyecto
- Justificación técnica, social y/o económica del trabajo.

### 4. Solución al problema
- Propuesta concreta y explicación de cómo resuelve la problemática planteada.

### 5. Cómo enfrentará técnicamente la solución
- Descripción del stack tecnológico, microcontroladores, sensores, actuadores, telemetría, lenguajes y metodologías a utilizar.

### 6. Diagrama de explicación del proyecto propuesto
- Sección reservada para el diagrama de bloques o arquitectura del sistema.
- Placeholder: "Espacio reservado para insertar diagrama de arquitectura."

### 7. Conclusiones
- Un concepto de lo que se trata todo el documento, no exceder más de 44 palabras en una estrofa.

## Tabla de Contenido (Índice Funcional)
El documento debe incluir un índice generado como campo dinámico de Word (`TOC Field`). Este campo se actualiza automáticamente en Word al hacer clic derecho → "Actualizar campos".

### Implementación en Python (`python-docx`)
Insertar el campo XML después de la carátula o página de título y antes del contenido principal:

```python
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

# ... después del título/resumen y antes del contenido ...

doc.add_page_break()

# ==================== TABLA DE CONTENIDO ====================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("TABLA DE CONTENIDO")
run.font.name = 'Arial'
run.font.size = Pt(14)
run.bold = True
run.font.color.rgb = RGBColor(0, 0, 0)
p.paragraph_format.space_before = Pt(12)
p.paragraph_format.space_after = Pt(24)

# Insertar campo TOC funcional (niveles 1-3, hipervínculos, estilos)
p = doc.add_paragraph()
run = p.add_run()
fld_char_begin = parse_xml(
    f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>'
)
run._r.append(fld_char_begin)

run2 = p.add_run()
instr_text = parse_xml(
    f'<w:instrText {nsdecls("w")} xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText>'
)
run2._r.append(instr_text)

run3 = p.add_run()
fld_char_separate = parse_xml(
    f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>'
)
run3._r.append(fld_char_separate)

run4 = p.add_run()
run4.text = 'Haga clic derecho y seleccione "Actualizar campos" para generar la tabla de contenido.'
run4.font.name = 'Arial'
run4.font.size = Pt(10)
run4.font.italic = True

run5 = p.add_run()
fld_char_end = parse_xml(
    f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>'
)
run5._r.append(fld_char_end)

doc.add_page_break()
```

### Parámetros del campo TOC:
- `\\o "1-3"`: Incluye niveles de esquema 1, 2 y 3.
- `\\h`: Crea hipervínculos clickeables a cada sección.
- `\\z`: Oculta los números de página y caracteres de tabulación en vista web.
- `\\u`: Usa estilos de párrafo (Heading 1, Heading 2, Heading 3) para construir el índice.

### Requisito para que funcione:
Todos los títulos del documento deben usar los estilos de Word `doc.add_heading(text, level=2)` o `level=3`. No usar párrafos con formato manual para títulos, ya que el campo TOC solo detecta los estilos de encabezado nativos.
