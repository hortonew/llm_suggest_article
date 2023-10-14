# type: ignore
import os
import warnings

import keyring
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator

# Store API key with:
# python -c 'import keyring; keyring.set_password("openai_api_key", "openai", "sk-...")'
os.environ["OPENAI_API_KEY"] = keyring.get_password(service_name="openai_api_key", username="openai")
warnings.simplefilter(action='ignore', category=UserWarning)

dir_loader = DirectoryLoader("data/")
loaders = [dir_loader]
index = VectorstoreIndexCreator().from_loaders(loaders)
number_of_documents_found = len(index.vectorstore.get()['documents'])
chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-4"),
    retriever=index.vectorstore.as_retriever(
        search_kwargs={"k": min(number_of_documents_found, 10)}
    )
)
query = "What are some of the most fun programming languages to learn if I like Python?"
result = chain({"question": query, "chat_history": []})
print(result["answer"])
