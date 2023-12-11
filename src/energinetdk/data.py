import os
import json
import uuid
from typing import Dict, Iterator, Tuple, List, Optional

from .config import DATA_FOLDER
from .embeddings import create_embeddings
from .pdf import extract_title_from_pdf, extract_text_from_pdf


DATA_FILE = os.path.join(DATA_FOLDER, 'data.json')


def iter_raw_data() -> Iterator[Dict[str, str]]:
    """
    Iterate over raw JSON data saved during crawling.
    """
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
        for item in data:
            yield item


def iter_documents() -> Iterator[Tuple[str, Dict[str, str]]]:
    """
    Iterate over documents.
    """
    for item in iter_raw_data():
        if item.get('content'):
            # continue
            # HTML page
            yield item['content'], {
                'type': 'website-link',
                'title': item['title'] if item['title'] else item['source_url'],
                'source_url': item['source_url'],
            }
        elif item.get('filename'):
            # PDF file
            filepath = os.path.join(DATA_FOLDER, 'files', item['filename'])
            if not os.path.exists(filepath):
                continue
            title = extract_title_from_pdf(filepath)
            if title is None:
                title = item['file_url'].rsplit('/', 1)[-1]
            for page_number, text in extract_text_from_pdf(filepath):
                yield text, {
                    'type': 'pdf-page',
                    'title': title,
                    'source_url': item['source_url'],
                    'file_url': item['file_url'],
                    'page_number': page_number,
                }
        else:
            raise NotImplementedError('Should not have happened')


def get_or_create_embeddings(text: str) -> Optional[List[float]]:
    """
    Get or create embeddings for a text.
    """
    fileid = uuid.uuid5(uuid.NAMESPACE_URL, text)
    filename = f'{fileid}.json'
    folder = os.path.join(DATA_FOLDER, 'embeddings')
    filepath = os.path.join(folder, filename)

    os.makedirs(folder, exist_ok=True)

    if os.path.exists(filepath):
        print('Loading embeddings from disk')
        with open(filepath, 'r') as f:
            return json.load(f)

    print('Creating embeddings')

    embeddings = create_embeddings(text)

    if not embeddings:
        return None

    with open(filepath, 'w') as f:
        json.dump(embeddings, f)

    return embeddings
