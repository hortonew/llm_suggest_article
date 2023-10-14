# type: ignore
import os
import warnings

import keyring
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Store API key with:
# python -c 'import keyring; keyring.set_password("openai_api_key", "openai", "sk-...")'
os.environ["OPENAI_API_KEY"] = keyring.get_password(service_name="openai_api_key", username="openai")
warnings.simplefilter(action='ignore', category=UserWarning)

chat = ChatOpenAI(model='gpt-4')
messages = [
    SystemMessage(content="You are a helpful assistant that knows a lot about programming languages."),
    HumanMessage(content="What are some of the most fun programming languages to learn if I like Python?")
]
print(chat(messages).content)
