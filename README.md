# Energinet.dk Semantic Search Engine

A simple demo project to show how to implement a semantic search engine using
a vector store. The project contains a simple web crawler that fetches all
HTML- and PDF-files from Energinet.dk and stores them in a Pinecone database.


## Requirements

- Python (tested with 3.11)
- Poetry (to manage dependencies)
- Azure OpenAI embedding model (to generate vector embeddings)
- Pinecone (to store the vector embeddings)


## Installation

1. Clone the repository
2. Install dependencies
   - Using Poetry: `poetry install`
   - Using Pip: `pip install -r requirements.txt`


## Usage

CD to the correct directory:

    $ cd src/

Start the crawler using the following command:

    $ poetry run python -m energinetdk crawl

Index crawled data into Pinecone vector store:

    $ poetry run python -m energinetdk index

Start the GUI:

    $ poetry run streamlit run gui.py


## Environment variables

The following environment variables are used:


| Name                      | Description                  |
|---------------------------|------------------------------|
| OPENAI_ENDPOINT           | Azure OpenAI Endpoint URL    |
| OPENAI_KEY                | Azure OpenAI Access token    |
| DEPLOYMENT_NAME           | Azure OpenAI Deployment name |
| API_VERSION               | Azure OpenAI API version     |
| PINECONE_API_KEY          | Pinecone API key             |
| PINECONE_INDEX            | Pinecone index name          |
| PINECONE_ENVIRONMENT      | Pinecone environment         |
