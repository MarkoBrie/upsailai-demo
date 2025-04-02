from dotenv import load_dotenv, find_dotenv

load_dotenv()

import os

settings = {**os.environ}

# Find the .env file
dotenv_path = find_dotenv()

# Load the .env file
#load_dotenv(dotenv_path)

print(f"1. working in file /discord/app/core/config.py)")
print(f"Loading environment variables from: {dotenv_path}")

# Print the path to the .env file
#print(f"Loading environment variables from: {dotenv_path}")
# Access specific environment variables
#openai_api_key = settings.get("OPENAI_API_KEY2")
#db_path = settings.get("DB_PATH")
#doc_store_path = settings.get("DOC_STORE_PATH")

# Print the values
#print(f"OPENAI_API_KEY: {openai_api_key}")
#print(f"DB_PATH: {db_path}")
#print(f"DOC_STORE_PATH: {doc_store_path}")