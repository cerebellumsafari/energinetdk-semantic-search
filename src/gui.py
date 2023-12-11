import pinecone
import streamlit as st

from energinetdk.embeddings import create_embeddings
from energinetdk.config import (
    PINECONE_API_KEY,
    PINECONE_ENVIRONMENT,
    PINECONE_INDEX,
)


pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENVIRONMENT,
)

index = pinecone.Index(PINECONE_INDEX)


# -- Streamlit app ------------------------------------------------------------


st.set_page_config(
    page_title='Energinet.dk Semantic Search',
    page_icon=":bird:",
)

st.header('Energinet.dk Semantic Search')

query_response = None

with st.form('search'):
    search_string = st.text_area('Enter question or search string:')

    if st.form_submit_button('Search'):
        search_embedding = create_embeddings(search_string)
        query_response = index.query(
            top_k=50,
            include_values=True,
            include_metadata=True,
            vector=search_embedding,
        )


if query_response is not None:
    if not query_response['matches']:
        st.subheader('No results found')

    for match in query_response['matches']:
        metadata = match['metadata']
        source_link = f'Source URL: [{metadata["source_url"]}]({metadata["source_url"]})'
        if metadata['type'] == 'website-link':
            st.subheader(metadata["title"])
            st.markdown(source_link, unsafe_allow_html=True)
        elif metadata['type'] == 'pdf-page':
            file_link = f'[{metadata["file_url"]}]({metadata["file_url"]})'
            st.subheader(f'PDF: {metadata["title"]} (page {int(metadata["page_number"])})')
            st.markdown(file_link, unsafe_allow_html=True)
            st.markdown(source_link, unsafe_allow_html=True)
        st.divider()
