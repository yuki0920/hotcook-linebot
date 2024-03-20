import logging
import sys

from vector_store import initialize_vectorstore
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings

load_dotenv()

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def add_document():
    # load document
    file_path = sys.argv[1]
    loader = UnstructuredPDFLoader(file_path)
    raw_docs = loader.load()
    logger.info("Loaded %d documents", len(raw_docs))

    # split documents
    text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    docs = text_splitter.split_documents(raw_docs)
    logger.info("Split %d documents", len(docs))

    # add documents to vectorstore
    vectorstore = initialize_vectorstore()
    vectorstore.add_documents(docs)

if __name__ == "__main__":
    add_document()
