from langchain_chroma import Chroma


class ChromaStore:

    def __init__(self,embedding,persist_directory="./chroma_db",collection_name="rag_collection",):

        self.collection_name = collection_name
        
        self.store = Chroma(
            collection_name=self.collection_name,
            embedding_function=embedding,
            persist_directory=persist_directory,
        )
        
        
        

    def add_documents(self, docs):
        # self.db = Chroma.from_documents(docs,embedding=self.embedding,persist_directory=self.persist_directory)
        self.store.add_documents(
            docs
        )
        
        
    def similarity_search(self,query,k=5):
        return self.store.similarity_search(query,k=k)
        
    def similarity_search_with_score(self,query,k=5):
        return self.store.similarity_search_with_score(query,k=k,)
    

    def max_marginal_relevance_search(self,query,k=5,):
        return self.store.max_marginal_relevance_search(query,k=k,)
    
    
    def as_retriever(self,k=5,):
        return self.store.as_retriever( search_kwargs={ "k": k})