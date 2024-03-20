import os

from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings

def initialize_vectorstore():
    index_name = os.environ["PINECONE_INDEX"]
    embeddings = OpenAIEmbeddings()
    return Pinecone.from_existing_index(index_name, embeddings)
