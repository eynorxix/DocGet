# Vercel vs Render para DocGent

## Vercel (NO recomendado para el backend)

Vercel es excelente para frontend (Next.js, React), pero tiene limitaciones para este proyecto:

| Problema | Detalle |
|---|---|
| Sin sistema de archivos | No se pueden guardar archivos subidos ni .docx generados |
| Timeout de 10s | La generacion de documentos puede tomar mas tiempo |
| No corre Python bien | Solo funciones serverless, no un servidor persistente |

**Vercel solo sirve** si separas el frontend (HTML estatico) del backend (API en otro lado).

## Render (recomendado)

Render es mejor opcion porque:
- Corre Python como servicio persistente
- Tiene sistema de archivos
- Sin timeout restrictivo
- Plan free funcional

## Alternativa hibrida

Si quieres usar Vercel para algo:
- Frontend en Vercel (HTML/JS puro)
- Backend Python en Render
- Frontend llama a la API de Render

## Conectarse desde otros agentes

Cualquier agente de IA o aplicacion externa puede conectarse al backend (donde sea que este hosteado) via HTTP:

```
[Agente Externo] --HTTP POST--> [DocGent API en Render]
                                   |
                                   v
                               .docx listo
```

El agente solo necesita hacer un `curl` o `fetch` a los endpoints de la API.
