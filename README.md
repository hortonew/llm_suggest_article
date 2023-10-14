# llm_suggest_article

What articles are worth reading, given what's relevant to me?

## Dependencies

```sh
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Store your OpenAI API Key in your system keychain for retrieval later
python -c 'import keyring; keyring.set_password("openai_api_key", "openai", "<your openai api key>")'

# Example
# python -c 'import keyring; keyring.set_password("openai_api_key", "openai", "sk-a1b2c3d4e5")'
```

## Quickstart

Suggest articles from Hacker News, based on my interests

```sh
python suggest_hn_article.py
```
