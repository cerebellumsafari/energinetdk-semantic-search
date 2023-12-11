import os
from decouple import config


_current_file = os.path.realpath(__file__)
_current_folder = os.path.split(_current_file)[0]

# Folders
SOURCE_FOLDER = os.path.realpath(os.path.join(_current_folder, '..'))
DATA_FOLDER = os.path.join(SOURCE_FOLDER, '..', 'var')
NLTK_FOLDER = os.path.join(DATA_FOLDER, 'nltk')

# Azure OpenAI
OPENAI_ENDPOINT = config('OPENAI_ENDPOINT', default=None)
OPENAI_KEY = config('OPENAI_KEY', default=None)
OPENAI_DEPLOYMENT_NAME = config('OPENAI_DEPLOYMENT_NAME', default=None)
OPENAI_API_VERSION = config('OPENAI_API_VERSION', default='2023-07-01-preview')

# Pinecone vector database
PINECONE_API_KEY = config('PINECONE_API_KEY', default=None)
PINECONE_ENVIRONMENT = config('PINECONE_ENVIRONMENT', default=None)
PINECONE_INDEX = config('PINECONE_INDEX', default='energinetdk-index')
