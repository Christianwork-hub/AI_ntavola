import os
import shutil
from langchain_community.document_loaders import JSONLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- 1. CONFIGURAZIONE ---
DATA_PATH = "ricette_dataset.json"       # file JSON con ricette
VECTOR_DB_DIR = "./ricette_db"   # Cartella dove salvare il database vettoriale

# PULIZIA: rimuove database esistente per ricrearlo
if os.path.exists(VECTOR_DB_DIR):
    print(f"Rimozione database esistente: {VECTOR_DB_DIR}")
    shutil.rmtree(VECTOR_DB_DIR)
    print("Database rimosso. Verrà ricreato.\n")

# --- 2. INIZIALIZZAZIONE EMBEDDINGS ---
print("1. Inizializzazione del modello di Embedding...")
embedding_model_name = "BAAI/bge-small-en-v1.5"
embeddings = HuggingFaceBgeEmbeddings(model_name=embedding_model_name)

# --- 3. CARICAMENTO DATI ---
print("2. Caricamento dei dati dal JSON...\n")

def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["titolo"] = record.get("titolo", "Titolo sconosciuto")
    metadata["categoria"] = record.get("categoria", "Categoria sconosciuta")
    metadata["descrizione"] = record.get("descrizione", "Descrizione mancante")
    metadata["id"] = record.get("id", 0)
    return metadata


loader = JSONLoader(
    file_path=DATA_PATH,
    jq_schema=".[]",           
    content_key="procedimento", 
    metadata_func=metadata_func
)


docs = loader.load()
print(f"Documenti caricati: {len(docs)}\n")

# --- 4. CREAZIONE DATABASE VETTORIALE ---
print("3. Creazione del database vettoriale...")
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory=VECTOR_DB_DIR
)
print(f"Database creato in: {VECTOR_DB_DIR}\n")

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# --- 5. CONFIGURAZIONE LLM ---
print("4. Connessione all'LLM locale...")
llm = Ollama(
    model="llama3",
    base_url="http://localhost:11434",
    temperature=0.1
)

# --- 6. PROMPT PERSONALIZZATO BASATO SUL RAG  ---
template = """Sei un esperto chef. Rispondi SOLO sulla base del contesto fornito.

CONTESTO:
{context}

DOMANDA: {question}

ISTRUZIONI:
- Leggi attentamente il contesto sopra
- Identifica ingredienti, procedimento e dettagli
- La ricetta deve includere:
    - Nome del piatto originale
    - Lista ingredienti
    - Procedimento dettagliato
    - Piccolo consiglio su come sorprendere i commensali
- Rispondi in italiano, mantenendo lo stile italiano autentico
- Non inventare informazioni, usa solo il contesto fornito
- Non aggiungere ingredienti esterni non menzionati nel contesto
"""


prompt = ChatPromptTemplate.from_template(template)

# --- 7. FUNZIONE DI FORMATTAZIONE CONTESTO ---
def format_docs(docs):
    context_parts = []
    for i, doc in enumerate(docs, 1):
        titolo = doc.metadata.get("titolo", "NON TROVATO")
        context_part = f"""RICETTA {i}:
Titolo: {titolo}
Procedimento: {doc.page_content}
"""
        context_parts.append(context_part)
    return "\n".join(context_parts)

# --- 8. RAG CHAIN ---
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- 9. ESECUZIONE QUERY ---
print("=" * 60)
print("ESECUZIONE QUERY PER GENERAZIONE DI RICETTE")
print("=" * 60)

question = "Generami una ricetta con parmigiano,melanzane e pomodoro"
print(f"\nDOMANDA: {question}\n")
print("RISPOSTA:")
response = rag_chain.invoke(question)
print(response)

question = "Generami una ricetta con ricotta,pane,olio"
print(f"\nDOMANDA: {question}\n")
print("RISPOSTA:")
response = rag_chain.invoke(question)
print(response)

question = "Generami una ricetta con basilico e pomodoro "
print(f"\nDOMANDA: {question}\n")
print("RISPOSTA:")
response = rag_chain.invoke(question)
print(response)

print("\n" + "=" * 60)
print("RICETTA CREATA")
print("=" * 60)
