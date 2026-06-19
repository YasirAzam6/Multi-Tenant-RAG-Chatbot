from fastapi import APIRouter, Depends, HTTPException
import logging
from api.dependencies.tenant import get_tenant
from api.schemas.rag import RAGChatRequest, RAGChatResponse, ContextChunk
from core.tenant_manager import TenantContext
from graph.rag_graph import build_graph

# Setup logger for this route
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/rag", tags=["rag"])

_GRAPH = None

def get_graph():
    global _GRAPH
    if _GRAPH is None:
        _GRAPH = build_graph()
    return _GRAPH

@router.post("/chat", response_model=RAGChatResponse)
async def chat(req: RAGChatRequest, tenant: TenantContext = Depends(get_tenant)):
    try:
        state = {"query": req.query, "tenant_id": tenant.tenant_id}
        config = {"configurable": {"thread_id": req.thread_id or f"thread_{tenant.tenant_id}"}}
        result = get_graph().invoke(state, config=config)
        
        # bot answers with its "bot_name" passed in query
        answer = result.get("answer") or ""
        bot_name = (tenant.config or {}).get("bot_name")

        if bot_name:
            # prefix the answer with bot name
            answer = f"{bot_name}: {answer}"

        ctx_out = None
        if req.include_context:
            docs = result.get("re_ranked_docs") or result.get("retrieved_docs") or []
            ctx_out = [ContextChunk(content=d.page_content, metadata=d.metadata or {}) for d in docs]

        return RAGChatResponse(
            tenant_id=tenant.tenant_id,
            router=result.get("router"),
            answer=answer,
            context=ctx_out,
        )
        
    except Exception as e:
        # 1. This prints the EXACT Python error to your Vercel logs
        logger.error(f"Fatal error in RAG graph: {str(e)}", exc_info=True)
        
        # 2. This returns a properly formatted JSON error to the frontend 
        # so you don't get the "Unexpected token 'I'" crash
        raise HTTPException(status_code=500, detail=f"LLM/Graph Error: {str(e)}")