from app.services.document_retrieval import DocumentRetriever


def test_document_retriever():
    retriever = DocumentRetriever(
        docs_path="C:\\code_gen_backend\\backend2\\data\\faiss_index\\documentation_chunks.json",
        index_path="C:\\code_gen_backend\\backend2\\data\\faiss_index\\documentation.index",
    )

    snippets = []
    for element in ["CSV parsing"]:
        retrieved_snippets = retriever.retrieve(element, k=2)
        snippets.extend(retrieved_snippets)
    print(snippets)
        