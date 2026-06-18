class RetrievalRouter:
    """
    Routes retrieval requests to the appropriate retriever based on tenant configuration.
    """
    
    def __init__(self, tenant):
        self.tenant = tenant
        cfg = tenant.config
        self.retriever_type = cfg.get("retriever", "vector")
        self.top_k = cfg.get("top_k", 5)

    def get_retriever(self):
        """
        Returns the appropriate retriever instance based on tenant configuration.
        Uses lazy loading to prevent Vercel memory locks (Errno 16).
        """
        if self.retriever_type == "vector":
            # Only imported if the tenant specifically needs vector retrieval
            from retrieval.vector_retriever import VectorRetriever
            return VectorRetriever(tenant=self.tenant, top_k=self.top_k)
            
        elif self.retriever_type == "bm25":
            # Only imported if the tenant specifically needs BM25
            from retrieval.bm25_retriever import BM25Retriever
            return BM25Retriever(tenant=self.tenant, top_k=self.top_k)
            
        elif self.retriever_type == "hybrid":
            # Heavy ML libraries (PyTorch/Transformers) are isolated here
            from retrieval.hybrid_retriever import HybridRetriever
            return HybridRetriever(tenant=self.tenant, top_k=self.top_k)
            
        else:
            # Default fallback
            from retrieval.vector_retriever import VectorRetriever
            return VectorRetriever(tenant=self.tenant, top_k=self.top_k)