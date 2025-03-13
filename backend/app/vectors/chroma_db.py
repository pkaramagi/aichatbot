from typing import Any, Dict, List
import chromadb
from app.vectors.base import VectorDB

class ChromaDB(VectorDB):
    def __init__(self, collection_name: str, embedding_dim, persist_dir:str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim
        self._create_collection()

    @property
    def _doc(self) -> Dict[str, Any]:
        return {
            "id": None,
            "text": "",
            "embedding": []
        }    
    
    def _create_collection(self) -> None:
      
        collection = self.client.get_or_create_collection(self.collection_name)
        if collection is not None:
            print(f"Collection '{self.collection_name} is ready for use.")

    def save_vectors(self, vectors: List[Dict[str, Any]]):
        collection = self.client.get_collection(self.collection_name)
        ids = []
        texts = []
        embeddings = []
        

        for vector in vectors:
            document_id = vector.get("id")
            if not document_id:
                raise ValueError("Vector Must have an 'id' field" )
            
            ids.append(document_id)
            texts.append(vector.get("text",""))
            embeddings.append(vector.get("embedding",[]))
            
        
        
        collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
           
        )
        print(f"Saved {len(vectors)} vectors to collection '{self.collection_name}'")

    def search_vectors(self, query_vector:List[float], top_k:int = 3):

        collection = self.client.get_collection(self.collection_name)
        print(f"Total records in collection '{self.collection_name}': {collection.count()}")

        results = collection.query(
            query_embeddings=[query_vector],
            n_results= top_k,
        )
        if results and "metadatas" in results and results["metadatas"]:
            return results
        return None
    
    
    def remove_collection(self):
        collection = self.client.get_collection(self.collection_name)
        collection.delete(ids=None)
        print(f"Collection {self.collection_name} has been reset")
        