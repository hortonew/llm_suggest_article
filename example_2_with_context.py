# pip install keyring langchain openai unstructured chromadb tiktoken
# type: ignore
import os

import keyring
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator

# Store API key with:
# python -c 'import keyring; keyring.set_password("openai_api_key", "openai", "sk-...")'
os.environ["OPENAI_API_KEY"] = keyring.get_password(service_name="openai_api_key", username="openai")

# Create an in-memory vector store with our context
dir_loader = DirectoryLoader("data/")
loaders = [dir_loader]
index = VectorstoreIndexCreator().from_loaders(loaders)

# Use our context when querying GPT-4.  At most consider 10 of the documents.  If <= 10, use every document found.
chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-4"),
    retriever=index.vectorstore.as_retriever(
        search_kwargs={"k": min(len(index.vectorstore.get('documents', [])), 10)}
    )
)

# Query / Response
query = "What are some of the most fun programming languages to learn if I like Python?"
result = chain({"question": query, "chat_history": []})
print(result["answer"])
