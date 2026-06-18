import os
import sys

# =========================================================================
# VERCEL FIX: MUST BE AT THE ABSOLUTE TOP BEFORE ANY OTHER APP IMPORTS
# =========================================================================
if os.environ.get("VERCEL") == "1":
    # Force tiktoken (OpenAI) to use the writable /tmp directory
    os.environ["TIKTOKEN_CACHE_DIR"] = "/tmp/tiktoken"
    os.makedirs("/tmp/tiktoken", exist_ok=True)
    
    # Force any underlying HuggingFace libraries to use /tmp
    os.environ["HF_HOME"] = "/tmp/huggingface"
    os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface"
    os.makedirs("/tmp/huggingface", exist_ok=True)
# =========================================================================

from core.tenant_manager import tenant_manager

from core.logging_config import setup_logging

from graph.rag_graph import build_graph
from core.server import app 
import uvicorn



setup_logging()

def run_cli():

    tenant = tenant_manager.load_tenant(tenant_id="tenant_1")
 
    print("Tenant Configuration:", tenant.config)
    print("System Prompt:", tenant.config.get("system_prompt"))
    print("Style Prompt:", tenant.config.get("style_prompt"))

    my_graph = build_graph()
    print("RAG Graph built successfully.")
    # mermaid_code = my_graph.get_graph().draw_mermaid()
    # print(mermaid_code)
    while True:
        input_query = input("Enter your query (or 'exit' to quit): ")
        if input_query.lower() == 'exit':
            break
        else:
            state = {
                "query": input_query,
                "tenant_id" : "tenant_1"
            }
            config_var = {"configurable": {
                "thread_id" : "thread_11",
            }}

            result = my_graph.invoke(state, config=config_var)
            print("Answer:", result['answer'])

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    else:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000
        )

# ****************************************************

