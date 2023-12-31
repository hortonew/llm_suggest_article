# type: ignore
import os
import warnings

import keyring
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator

from hn_articles import fetch_or_load_articles

warnings.simplefilter(action='ignore', category=UserWarning)

# Store secret with: python -c  'import keyring; keyring.set_password("openai_api_key", "openai", "sk-...")'
os.environ["OPENAI_API_KEY"] = keyring.get_password("openai_api_key", "openai")

# Load context
dir_loader = DirectoryLoader("data/")
loaders = [dir_loader]
index = VectorstoreIndexCreator().from_loaders(loaders)
total_documents_with_context = len(index.vectorstore.get('documents', []))
print(f"Total documents with context loaded: {total_documents_with_context}")
chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-4"),
    retriever=index.vectorstore.as_retriever(
        search_kwargs={"k": min(total_documents_with_context, 10)}
    ),
)

# Load articles to curate
print("Fetching articles")
articles = fetch_or_load_articles()
print(f"Total articles from HN loaded: {len(articles)}\n\n")

# Curate
query = (
    "Based on this list of hacker news articles and what you know about me, "
    "which of these are the best articles to read based on my interests?  "
    "Please only provide a bulleted list back without expanding on why they are relevant to me.  "
    "If you can somehow give a percentage 0-100% based on how well they fit my interests, please provide that too. "
    "Don't suggest anything that isn't a 75% or higher, but if there are no suggestions, provide the top 3 even if"
    "below 75%. "
    f"{articles}"
)
result = chain({"question": query, "chat_history": []})
print("Suggestions: ")
print(result["answer"])
