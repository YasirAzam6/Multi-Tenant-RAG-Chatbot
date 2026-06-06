from fastapi import APIRouter, Depends
from api.dependencies.tenant import get_tenant
from api.schemas.rag import RAGChatRequest, RAGChatResponse, ContextChunk
from core.tenant_manager import TenantContext
from graph.rag_graph import build_graph
import traceback

router = APIRouter(prefix="/v1/rag", tags=["rag"])

_GRAPH = build_graph()  # build once

@router.post("/chat", response_model=RAGChatResponse)
async def chat(req: RAGChatRequest, tenant: TenantContext = Depends(get_tenant)):
    state = {"query": req.query, "tenant_id": tenant.tenant_id}
    config = {"configurable": {"thread_id": req.thread_id or f"thread_{tenant.tenant_id}"}}

    try:
        # Changed to ainvoke() to prevent blocking FastAPI's async loop
        result = await _GRAPH.ainvoke(state, config=config)
        
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
        # THE TRICK: Catch the crash and send the error to the chat UI
        error_trace = traceback.format_exc()
        return RAGChatResponse(
            tenant_id=tenant.tenant_id,
            router="ERROR",
            answer=f"🚨 CRASH DETECTED 🚨\n\n{error_trace}",
            context=[]
        )