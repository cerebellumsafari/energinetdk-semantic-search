import os
import uuid
import click
import pinecone
from scrapy.crawler import CrawlerProcess

from .spider import EnerginetSpider
from .data import iter_documents, get_or_create_embeddings
from .config import (
    DATA_FOLDER,
    PINECONE_API_KEY,
    PINECONE_ENVIRONMENT,
    PINECONE_INDEX,
)


@click.command()
def run_crawl():
    """
    Run the crawler.
    """
    # Create the data folder if it doesn't exist
    os.makedirs(DATA_FOLDER, exist_ok=True)

    # The output file
    output_file = os.path.join(DATA_FOLDER, 'data.json')

    # Crawler settings
    process = CrawlerProcess(
        settings={
            'FEEDS': {
                output_file: {'format': 'json'},
            },
        }
    )

    # Run the crawler
    process.crawl(EnerginetSpider)
    process.start()


@click.command()
def index_data():
    """
    Index all documents into vector database.
    """
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT,
    )

    active_indexes = pinecone.list_indexes()

    if PINECONE_INDEX not in active_indexes:
        pinecone.create_index(
            name=PINECONE_INDEX,
            dimension=1536,
        )

    index = pinecone.Index(PINECONE_INDEX)

    for content, metadata in iter_documents():
        embeddings = get_or_create_embeddings(content)

        if not embeddings:
            continue

        upsert_response = index.upsert(
            vectors=[
                (
                    str(uuid.uuid5(uuid.NAMESPACE_URL, content)),
                    embeddings,
                    metadata,
                ),
            ],
        )

        assert upsert_response['upserted_count'] == 1

        print(metadata)
        print(content)
        print(embeddings)
        print('-' * 80)


@click.command()
def run_gui():
    """
    Index all documents into vector database.
    """
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT,
    )

    active_indexes = pinecone.list_indexes()

    if PINECONE_INDEX not in active_indexes:
        pinecone.create_index(
            name=PINECONE_INDEX,
            dimension=1536,
        )

    index = pinecone.Index(PINECONE_INDEX)

    for content, metadata in iter_documents():
        embeddings = get_or_create_embeddings(content)

        upsert_response = index.upsert(
            vectors=[
                (
                    str(uuid.uuid5(uuid.NAMESPACE_URL, content)),
                    embeddings,
                    metadata,
                ),
            ],
        )

        assert upsert_response['upserted_count'] == 1

        print(metadata)
        print(content)
        print(embeddings)
        print('-' * 80)


# -- Main ---------------------------------------------------------------------


@click.group()
def main():
    """
    Energinet.dk crawler CLI
    """
    pass


main.add_command(run_crawl, name='crawl')
main.add_command(index_data, name='index')
main.add_command(run_gui, name='gui')
