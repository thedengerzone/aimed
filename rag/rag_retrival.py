#%%


docs = vector_store.similarity_search("Bodovanje nazočnosti na nastavi", k=2)
for doc in docs:
    print(f'Page {doc.metadata["page"]}: {doc.page_content[:300]}\n')