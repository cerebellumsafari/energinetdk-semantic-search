import nltk
import openai
from typing import List, Optional
from functools import lru_cache
from nltk.corpus import stopwords
from openai import AzureOpenAI

from .config import (
    OPENAI_ENDPOINT,
    OPENAI_KEY,
    OPENAI_DEPLOYMENT_NAME,
    OPENAI_API_VERSION,
    NLTK_FOLDER,
)


openai_client = AzureOpenAI(
    azure_endpoint=OPENAI_ENDPOINT,
    azure_deployment=OPENAI_DEPLOYMENT_NAME,
    api_version=OPENAI_API_VERSION,
    api_key=OPENAI_KEY,
)


@lru_cache
def get_stopwords(language: str = 'danish') -> List[str]:
    """
    Initiate NLTK and download stopwords and tokenizer
    if not already downloaded.

    :param language: The language to get stopwords for.
    :return: The stopwords.
    """
    if NLTK_FOLDER not in nltk.data.path:
        nltk.data.path.append(NLTK_FOLDER)

    nltk.download('punkt', download_dir=NLTK_FOLDER)
    nltk.download('stopwords', download_dir=NLTK_FOLDER)

    return stopwords.words(language)


def create_embeddings(s: str, lang: str = 'danish') -> Optional[List[float]]:
    """
    Create embeddings from a string.

    :param s: The string to create embeddings from.
    :param lang: The language of the string.
    :return: The embeddings.
    """
    stopwords_ = get_stopwords(lang)

    tokens = nltk.word_tokenize(s, language=lang)
    tokens_no_punct = (word for word in tokens if word.isalnum())
    tokens_no_stopwords = (t for t in tokens_no_punct if t not in stopwords_)
    tokens_lower = (t.lower() for t in tokens_no_stopwords)

    model_input = ' '.join(tokens_lower)

    if model_input == '':
        # Empty string after preprocessing means no input is worth embedding
        return None

    try:
        response = openai_client.embeddings.create(
            model='text-embedding-ada-002',
            input=[model_input],
        )
    except openai.APIError as e:
        raise ValueError('%s (INPUT: "%s")' % (str(e), model_input))

    return response.data[0].embedding
