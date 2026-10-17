from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

class EmbeddingModel:

    def __init__(self,model_name="BAAI/bge-small-en-v1.5"):

        if model_name.startswith("BAAI/") or model_name.startswith("sentence-transformers/"):
            self.model = HuggingFaceEmbeddings(
                model_name=model_name
            )
            
        elif model_name.startswith("text-embedding-"):
            api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY environment variable is required "
                    "for OpenAI embeddings."
                )

            self.model = OpenAIEmbeddings(
                model=model_name,
                api_key=api_key,
            )
            
            
        elif model_name.startswith("gemini-embedding"):

            api_key = os.getenv("GOOGLE_API_KEY")

            if not api_key:
                raise ValueError(
                    "GOOGLE_API_KEY environment variable is required "
                    "for Gemini embeddings."
                )

            self.model = GoogleGenerativeAIEmbeddings(
                model=model_name,
                google_api_key=api_key,
            )
            
        
        else:

            raise ValueError(
                f"Unsupported embedding model: '{model_name}'.\n"
                "Supported models/providers:\n"
                "- HuggingFace: BAAI/*, sentence-transformers/*\n"
                "- OpenAI: text-embedding-*\n"
                "- Gemini: gemini-embedding*\n"
                "- Cohere: embed-*"
            )
                

    def get(self):
        return self.model