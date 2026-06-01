# Skills

## Que son

Las Skills son archivos (`.md`, `.py`, `.txt`) que definen **la estructura y las reglas** para generar un documento. Funcionan como plantillas o instructivos que la IA sigue al generar contenido.

Cada skill contiene:
- **Nombre**: Titulo descriptivo
- **Descripcion**: Para que sirve
- **Contenido**: La estructura del documento en Markdown o Python

## Como funcionan

1. El usuario selecciona una skill
2. El sistema envia la skill completa a Gemini como parte del prompt
3. Gemini genera contenido siguiendo la estructura definida en la skill
4. El contenido generado se pasa a `document_generator.py` que produce el `.docx`

## Tipos de skills

### Markdown (.md) - Recomendado
Definen la estructura del documento con encabezados, viñetas y ejemplos.

```markdown
# Nombre de Skill

## Descripcion
...

## Contenido
# {titulo}

## 1. Introduccion

## 2. Desarrollo

## 3. Conclusiones
```

### Python (.py)
Contienen codigo Python que puede extender o personalizar la generacion.

```python
"""
Nombre

Descripcion
"""

def procesar(datos):
    # Logica personalizada
    return resultado
```

### Texto (.txt)
Texto plano sin formato.

## Skills precargadas

| Skill | Tipo | Proposito |
|---|---|---|
| `EstructuraIntegrador` | .md | Tesis UNIFRANZ (formato APA 7 completo) |
| `humano` | .md | Estilo de escritura humana anti-deteccion IA |
| `Skill-Controladores` | .md | Documentos tecnicos de microcontroladores |
| `base_documento` | .py | Modulo de formato APA 7 para document_generator |

## Crear una skills

Desde la interfaz:
1. Click en "+ nueva skill" en la barra lateral
2. Llenar nombre, descripcion, tipo y contenido
3. Click en "crear skill"

O desde la API:
```bash
curl -X POST http://localhost:8000/api/skills \
  -H "Content-Type: application/json" \
  -d '{"name": "Mi Skill", "content": "# Estructura...", "type": "md"}'
```

O directamente creando un archivo en `data/skills/`.
