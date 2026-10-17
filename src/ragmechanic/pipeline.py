import time

from .ingestion.document_loader import DocumentLoader
from .ingestion.text_splitter import TextSplitter

from .embeddings.embedding import EmbeddingModel
from .vector_store.vector_store import VectorStore

from .retriever.retriever import Retriever
from .compression.compressor import Compressor

from .llm.manager import LLMManager
from .evaluation.evaluator import Evaluator

from .report.result import RAGResult

from .report.html_report import HTMLReport

from pathlib import Path

from .storage.database import Database
import uuid


PACKAGE_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PACKAGE_ROOT / "output"

DATABASE_DIR = OUTPUT_DIR / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

REPORT_DIR = OUTPUT_DIR / "report"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
report_path = REPORT_DIR / "rag_report.html"


class RAGPipeline:

    def __init__(
        self,
        docs,
        embedding_model,
        llm_provider,
        llm_model,
        vector_store="chroma",
        chunk_size=800,
        chunk_overlap=150,
        db_path=None,
        k=5,
    ):
        
        if db_path is None:
            db_path = DATABASE_DIR / "ragmechanic.db"
        
        self.k = k

        self.pipeline_id = uuid.uuid4().hex
        
        self.loader = DocumentLoader(docs)

        self.splitter = TextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        self.embedding = EmbeddingModel(
            embedding_model
        )

        self.db = VectorStore(
            embedding=embedding_model,
            vector_store=vector_store,
            collection_name=f"rag_{self.pipeline_id}",
        )

        self.llm = LLMManager(
            provider=llm_provider,
            model=llm_model,
        )

        self.documents = self.loader.load()

        self.chunks = self.splitter.split(
            self.documents
        )

        self.db.add_documents(self.chunks)

        self.retriever = Retriever(
            vector_store = self.db.store,
            k=self.k
        )

        self.compressor = Compressor(
            # retriever=self.db.as_retriever(),
            llm=self.llm.get_llm(),
        )

        self.evaluator = Evaluator(
            llm=self.llm.get_llm(),
            embeddings=self.embedding.get(),
        )
        
        self.report = HTMLReport(
            report_path
        )
        
        self.database = Database( db_path=db_path )
        

    def ask(
        self,
        question,
    ):

        print("--- Retrieving Documents ---")
        retrieval = self.retriever.retrieve(question)

        print("--- Compressing Documents ---")
        compression = self.compressor.compress(
            question,
            retrieval["documents"],
        )

        context = "\n\n".join(
            d.page_content
            for d in compression.compressed_documents
        )

        
        prompt = f"""
                You are a helpful AI assistant.
                Answer ONLY using the provided context.\n
                DOn't assume anything your own. \n
                If answer is not found, say: "Not found in documents."\n

                Context:
                {context}\n

                Question:
                {question}
                """
            

        start = time.perf_counter()

        print("--- Getting response from llm ---")
        response = self.llm.invoke(prompt)

        generation_latency = (
            time.perf_counter()
            - start
        )
        
        answer = response.content[0]['text']
        # return
        
        # print("--- Evaluating the respone ---")
        
        

        # evaluation = self.evaluator.evaluate(
        #     question=question,
        #     answer=answer,
        #     contexts=[
        #         d.page_content
        #         for d in compression.compressed_documents
        #     ],
        # )

        result = RAGResult(
            id=None,
            question=question,
            answer=answer,

            retrieved_documents=retrieval["documents"],

            compressed_documents=(
                compression.compressed_documents
            ),

            retrieval_latency=(
                retrieval["retrieval_latency"]
            ),

            compression_latency=(
                compression.compression_latency
            ),

            generation_latency=(
                generation_latency
            ),

            evaluation=None,
        )
        
        query_id = ( self.database.save_result( result ) ) 
        result.id = query_id
        
        self.report.add_result(result)

        return result
    
    
    
    
    def evaluate( self, query_id=None, metrics=None ):
        # ----------------------------------------- # Determine queries # -----------------------------------------  
        if query_id is not None: 
            query_ids = [ query_id ] 
        
        else: 
            query_ids = ( self.database .get_unevaluated_query_ids() ) 
        
        if not query_ids: 
            print( "No unevaluated queries found." ) 
            return 
        
        print( f"Evaluating {len(query_ids)} query(s)..." ) 
        
        # ----------------------------------------- # Evaluate each query # ----------------------------------------- 
        for current_id in query_ids: 
            result = ( self.database .get_query(current_id) ) 
            
            if result is None: 
                print( f"Query {current_id} not found." )
                continue 
            
            print( f"\nEvaluating Query {current_id}" ) 
            print( f"Question: {result.question}" ) 
            
            # ----------------------------------------- # Evaluation # ----------------------------------------- 
            contexts = [ doc.page_content for doc in result.compressed_documents ]
            
            print( f"Evaluation contexts: {len(contexts)}" )
            
            evaluation = ( self.evaluator.evaluate( 
                                question=result.question,
                                answer=result.answer, 
                                contexts=contexts, 
                                # metrics=metrics, 
                                ) )
            
            self.database.save_evaluation( query_id=current_id, evaluation=evaluation, ) 
            print( "Evaluation saved." )
            
            
        self.report = HTMLReport()
            
        for result in ( self.database.get_all_queries() ):
            self.report.add_result( result )
        print( "\nEvaluation completed." )
    
    
    
    
    def save_html(self, path= report_path): 
        self.report = HTMLReport( path ) 
        for result in ( self.database.get_all_queries() ): 
            self.report.add_result( result ) 
        return self.report.generate()