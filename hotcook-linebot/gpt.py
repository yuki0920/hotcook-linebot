import logging
import os

from vector_store import initialize_vectorstore
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain

CHAT_UPDATE_INTERVAL_SEC = 1
OPENAI_API_TEMPERATURE = 0.5
# OPENAI_API_MODEL="gpt-3.5-turbo-0125"
OPENAI_API_MODEL="gpt-4-0125-preview"

# ログ
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

logger.info("Starting the app")

def call_gpt(recipe):
    llm = ChatOpenAI(
          model=OPENAI_API_MODEL,
          temperature=OPENAI_API_TEMPERATURE,
    )

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """あなたは優秀なレシピを考えるシェフです。提供されたメニューに一番近いホットクックメニューを探し、下記のフォーマットで回答してください。メニューではなく食材名が含まれる場合は、その食材を含むメニューを複数探してください。
        ・メニュー名
        ・人数
        ・食材
            ・食材1: 量
            ・食材2: 量
            etc...
        ・作り方
        \n\n{context}"""),
        ("user", "{input}"),
    ]
    )

    document_chain = create_stuff_documents_chain(llm, prompt)

    vectorstore = initialize_vectorstore()
    retriever = vectorstore.as_retriever()

    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": recipe})
    answer = response["answer"]
    logger.info("Answer: %s", answer)

    return answer
