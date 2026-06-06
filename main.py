import sys
import uvicorn
from core.server import app 
from core.logging_config import setup_logging
from core.tenant_manager import tenant_manager
from graph.rag_graph import build_graph

def run_cli():
    tenant = tenant_manager.load_tenant(tenant_id="tenant_1")
    
    print("Tenant Configuration:", tenant.config)
    print("System Prompt:", tenant.config.get("system_prompt"))
    print("Style Prompt:", tenant.config.get("style_prompt"))

    my_graph = build_graph()
    print("RAG Graph built successfully.")
    
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

# Vercel ignores everything below this line, which prevents the 500 crash!
if __name__ == "__main__":
    setup_logging() 
    
    if "--cli" in sys.argv:
        run_cli()
    else:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000
        )