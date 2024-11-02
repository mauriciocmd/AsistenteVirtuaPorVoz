import spacy

# Cargar el modelo de lenguaje en español de spaCy
nlp = spacy.load("es_core_news_sm")

intenciones = {
    "buscar": ["buscar", "investigar", "consultar"],
    "crear_documento": ["crear documento", "nuevo documento", "escribir documento"],
    "leer_documento": ["leer documento", "abrir documento", "mostrar documento"],
    "navegar_internet": ["navegar", "abrir navegador", "buscar en internet"],
    "control_basico": ["subir volumen", "bajar volumen", "conectar wifi", "desconectar wifi"]
}

def reconocer_intencion(comando):
    doc = nlp(comando)
    for token in doc:
        for intencion, palabras in intenciones.items():
            if token.lemma_ in palabras:
                return intencion
    return "desconocida"

