from ddgs import DDGS

# Mapa de terminos tecnico-cientificos españoles -> ingles
_TERM_MAP = {
    "sistema operativo": "operating system",
    "distribuciones": "distributions",
    "distribucion": "distribution",
    "software libre": "free software open source",
    "codigo abierto": "open source",
    "inteligencia artificial": "artificial intelligence",
    "aprendizaje automatico": "machine learning",
    "redes neuronales": "neural networks",
    "base de datos": "database",
    "desarrollo web": "web development",
    "aplicaciones moviles": "mobile applications",
    "computacion en la nube": "cloud computing",
    "seguridad informatica": "cybersecurity",
    "arquitectura de computadores": "computer architecture",
    "lenguaje de programacion": "programming language",
    "framework": "framework",
    "microcontrolador": "microcontroller",
    "internet de las cosas": "internet of things",
    "analisis de datos": "data analysis",
    "visualizacion de datos": "data visualization",
    "ingenieria de software": "software engineering",
    "metodologia agil": "agile methodology",
    "caracteristicas": "features",
    "principales": "top",
    "usos": "uses",
    "tipos": "types",
    "que es": "what is",
    "como funciona": "how it works",
}


def _spanish_to_english(query: str) -> str:
    result = query.lower()
    for es, en in _TERM_MAP.items():
        result = result.replace(es, en)
    if result == query.lower():
        return query
    return result


def _simplify_query(query: str) -> str:
    stopwords = {
        "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del",
        "en", "por", "para", "con", "sin", "y", "e", "o", "u", "a", "que",
        "es", "como", "sobre", "entre", "cuales", "cual", "sus", "tu", "mi",
        "se", "le", "lo", "al", "del", "mas", "más", "pero", "tambien",
        "muy", "este", "esta", "esto", "esa", "eso", "ese",
    }
    words = query.split()
    simplified = [w for w in words if w.lower() not in stopwords and len(w) > 2]
    if not simplified:
        simplified = [w for w in words if len(w) > 2]
    if not simplified:
        return query
    return " ".join(simplified[:6])


def search_web(query: str, max_results: int = 5) -> list[dict]:
    queries_to_try = [query]

    simplified = _simplify_query(query)
    if simplified != query:
        queries_to_try.append(simplified)

    english = _spanish_to_english(query)
    if english not in queries_to_try and english != query:
        queries_to_try.append(english)

    simplified_en = _simplify_query(english)
    if simplified_en not in queries_to_try and simplified_en != english:
        queries_to_try.append(simplified_en)

    seen_urls = set()
    all_results = []

    for q in queries_to_try:
        try:
            with DDGS() as ddgs:
                results = ddgs.text(q, max_results=max_results)
                for r in results:
                    url = r.get("href", "")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        all_results.append({
                            "title": r.get("title", ""),
                            "href": url,
                            "body": r.get("body", ""),
                        })
        except Exception:
            continue
        if len(all_results) >= max_results:
            break

    return all_results[:max_results]


def search_web_formatted(query: str, max_results: int = 5) -> str:
    results = search_web(query, max_results)
    if not results:
        return "No se encontraron resultados en internet para esta consulta."
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. **{r['title']}**")
        lines.append(f"   {r['body'][:300]}")
        if r['href']:
            lines.append(f"   Fuente: {r['href']}")
        lines.append("")
    return "\n".join(lines).strip()
