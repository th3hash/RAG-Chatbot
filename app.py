# HackproofHacks AI Security Lab | @trickyhash | github.com/th3hash
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama

PDF_PATH = "handbook.pdf"
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "rag_chatbot"
OLLAMA_MODEL = "llama3.2"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def build_vector_store():
    if not Path(PDF_PATH).exists():
        raise FileNotFoundError(
            f"Could not find {PDF_PATH}. Put your PDF in the project root."
        )

    docs = PyPDFLoader(PDF_PATH).load()
    print(f"Loaded {len(docs)} pages.")

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    ).split_documents(docs)

    print(f"Created {len(chunks)} chunks.")
    print("Building/loading Chroma index...")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
    )

    return vectorstore


def answer_question(vectorstore, llm, question):
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
    retrieved_docs = retriever.invoke(question)

    context_parts = []
    for index, doc in enumerate(retrieved_docs, start=1):
        page = doc.metadata.get("page", "?")
        context_parts.append(
            f"[Chunk {index} | page {page}]\n{doc.page_content}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""You are a document-grounded assistant.

Answer the user's question using ONLY the provided context.
If the context does not contain enough information to answer,
say that the answer was not found in the provided document.
Do not invent facts.

CONTEXT:
{context}

QUESTION:
{question}
"""

    response = llm.invoke(prompt)

    print("\n" + "=" * 70)
    print("RETRIEVED CHUNKS")
    print("=" * 70)
    print(context)

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)
    print(response.content)
    print("=" * 70)


def main():
    vectorstore = build_vector_store()

    llm = ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0,
    )

    print("\nRAG chatbot ready.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        if not question:
            continue

        answer_question(vectorstore, llm, question)


if __name__ == "__main__":
    main()
