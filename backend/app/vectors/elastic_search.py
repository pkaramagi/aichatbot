from typing import Any, Dict, List
from elasticsearch import Elasticsearch
from app.vectors.base import VectorDB


class ElasticSearchDB(VectorDB):
    def __init__(self, index_name:str, embedding_dim:int, host:str ="http://localhost", port:int= 9200,):
        self.client:Elasticsearch = Elasticsearch(
            [f"{host}:{port}"] 
        )
        self.index_name = index_name
        self.embedding_dim = embedding_dim
        self._create_index()
        
    @property
    def _mapping(self) -> Dict[str, Any]:
        return  {
            "mapping":{
                "properties":{
                    "id": {"type":"keyword"},
                    "text": {"type":"text"},
                    "embedding":{"type":"dense_vector","dims":self.embedding_dim}
                }
            }
        }
    
    @property
    def _doc(self) -> Dict[str, Any]:
        return {
            "id": None,
            "text": "",
            "embedding": []
        }
    
    @property 
    def _querybody(self, size, query_embedding) -> Dict[str, Any]:
        return {
            "size": size,
            "query": {
                "script_score":{
                    "query": {"match_all":{}},
                    "script":{
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": query_embedding}
                    }
                }
            }
        }


    def _create_index(self) -> None:
        
        if not self.client.indices.exists(index=self.index_name):
            self.client.indices.create(index=self.index_name, body=self._mapping)
            print(f"index '{self.index_name}' created successfully.")
        


    def save_vectors(self, vectors:List[Dict[str, Any]]):
        for vector in vectors:
            document_id = vector.get("id")
            if not document_id:
                raise ValueError("Vector Must have an 'id field")
            
            doc = self._doc.copy()
            doc['id'] = document_id
            doc['text'] = vector.get("text","")
            doc['embedding'] = vector.get("embedding", [])
            
           
            self.client.index(index=self.index_name, id=document_id, body=doc)
            print(f"Saved Vector {document_id}")
    
    def search_vectors(self, query_vector:List[float], top_k:int = 3):

        search_results = self.client.search(
            index=self.index_name,
            body = self._querybody(top_k,query_vector)
        )

        if search_results["hits"]["hits"]:
            return search_results
        
        return None

    