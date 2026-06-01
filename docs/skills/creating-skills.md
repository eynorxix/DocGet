# Crear Skills

## Reglas generales

- El **nombre** se extrae de la primera linea del archivo
- La **descripcion** se extrae de la linea posterior a `## Descripcion`
- El **ID** es el nombre del archivo sin extension
- Archivos soportados: `.md`, `.py`, `.txt`

## Markdown (.md)

Estructura recomendada:

```markdown
# Nombre de la Skill

## Descripcion
Breve descripcion de que tipo de documentos genera esta skill.

## Contenido

Define aqui la estructura del documento usando Markdown.

# {titulo}

## 1. Introduccion
Contexto del proyecto...

## 2. Marco Teorico
### 2.1 Conceptos fundamentales
...

## 3. Conclusiones
...

## Referencias
```

Las variables como `{titulo}`, `{autor}` pueden usarse como placeholders.

## Python (.py)

Estructura recomendada:

```python
"""
Nombre de la Skill

Descripcion de la skill
"""

# Puedes definir funciones que el sistema pueda usar
Estructura del documento:
- 1. Introduccion
- 2. Desarrollo
- 3. Conclusiones
```

## Tips

1. **Skills atomicas**: Cada skill debe cubrir UN tipo de documento
2. **Reutilizacion**: Las skills se pueden combinar subiendo archivos de contexto
3. **Iteracion**: Edita la skill y regenera el documento para mejorarlo
4. **Colaboracion**: Comparte skills copiando los archivos `.md`
