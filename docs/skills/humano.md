# Skill: humano (Estilo de escritura humana)

**Archivo**: `data/skills/humano.md`

## Proposito

Guia para generar texto con estilo humano, dificil de detectar como IA por herramientas como Turnitin, GPTZero o Originality.ai.

## Principios

1. **Perplexity**: El texto no debe ser predecible. Usar frases inesperadas, variacion emocional, errores naturales.
2. **Burstiness**: Variar drasticamente la longitud de frases y parrafos. No mantener un ritmo uniforme.
3. **Conectores minimos**: Maximo 3 conectores por cada 10 parrafos. Evitar "asimismo", "por lo tanto", "cabe destacar".
4. **Profundidad tecnica real**: Incluir problemas encontrados, datos concretos, errores, debugging.

## Como se usa

Esta skill no define una estructura de documento, sino un **estilo de escritura**. Se combina con otras skills (como `EstructuraIntegrador`) para que el contenido generado suene mas humano.

## Ejemplo de transformacion

**Original (IA)**:
> "El modulo Bluetooth HC-05 permite la comunicacion inalambrica..."

**Transformado (humano)**:
> "El HC-05 fue un dolor de cabeza las primeras dos semanas. El datasheet dice que opera a 3.3V, pero el modulo que compre venia con un regulador integrado, entonces funcionaba a 5V igual."
