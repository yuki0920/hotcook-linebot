from logger import get_logger
from vector_store import initialize_vectorstore
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain

CHAT_UPDATE_INTERVAL_SEC = 1
OPENAI_API_TEMPERATURE = 0.5
# OPENAI_API_MODEL="gpt-3.5-turbo-0125"
OPENAI_API_MODEL="gpt-4-0125-preview"

logger = get_logger()

def call_gpt(recipe):
    llm = ChatOpenAI(
          model=OPENAI_API_MODEL,
          temperature=OPENAI_API_TEMPERATURE,
    )

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """あなたはレシピ探しが得意な優秀なシェフです。提供されたメニューに類似したホットクックメニューを探し、下記のフォーマットで回答してください。
        質問内容にメニューではなく食材名が含まれる場合は、その食材を含むメニューを複数探してください。
        回答には、口語体で回答してください。
        メニューを見つけられない場合は、「ごめんね、<メニュー or 食材>に関するレシピは見つからなかったよ。」と回答してください。

        フォーマット:
        [メニュー: <メニュー名>]
        人数: <人数>

        食材
        ・<食材1>: <量>
        ・<食材2>: <量>
        etc...

        作り方
        ・<作り方1>
        ・<作り方2>
        etc...
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
