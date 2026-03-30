from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

# Initialize Azure AI Search client
search_endpoint = "YOUR_SEARCH_ENDPOINT"
search_key = "YOUR_SEARCH_KEY"
search_index_name = "YOUR_INDEX_NAME"

search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=search_index_name,
    credential=AzureKeyCredential(search_key)
)

# Initialize Azure OpenAI client
openai_client = AzureOpenAI(
    api_key="YOUR_OPENAI_KEY",
    api_version="2024-02-15-preview",
    azure_endpoint="YOUR_OPENAI_ENDPOINT"
)

def retrieve_documents(query: str, top_k: int = 3) -> list:
    """Retrieve relevant documents from Azure AI Search"""
    results = search_client.search(search_text=query, top=top_k)
    documents = [result["content"] for result in results]
    return documents

def generate_response(user_query: str, context_documents: list) -> str:
    """Generate response using Azure OpenAI with retrieved context"""
    context = "\n".join(context_documents)
    
    system_prompt = "You are a helpful IT helpdesk assistant. Use the provided context to answer questions."
    user_message = f"Context:\n{context}\n\nQuestion: {user_query}"
    
    response = openai_client.chat.completions.create(
        model="YOUR_DEPLOYMENT_NAME",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content

def rag_pipeline(query: str) -> str:
    """Simple RAG pipeline: retrieve + generate"""
    documents = retrieve_documents(query)
    response = generate_response(query, documents)
    return response

if __name__ == "__main__":
    user_query = "How do I reset my password?"
    answer = rag_pipeline(user_query)
    print(answer)