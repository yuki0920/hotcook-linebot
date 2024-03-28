from logger import get_logger
from vector_store import initialize_vectorstore
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain

OPENAI_API_TEMPERATURE = 0.1
# OPENAI_API_MODEL="gpt-3.5-turbo-0125"
OPENAI_API_MODEL="gpt-4-0125-preview"

logger = get_logger()

def call_gpt(recipe):
    llm = ChatOpenAI(
          model=OPENAI_API_MODEL,
          temperature=OPENAI_API_TEMPERATURE,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """あなたはレシピ探しが得意な優秀なシェフです。
        入力として与えられた素材やメニューを元にホットクックのレシピを探し、
        下記のフォーマットで回答してください。
        質問内容に素材やメニュー以外の情報が含まれている場合は、自然に返答した後に
        「素材やメニューを教えてくれたら、もっと具体的なレシピを探せるかもしれないよ。」と返答してください。
        回答には、口語体で回答してください。
        メニューを見つけられない場合は、「ごめんね、<メニュー or 食材>に関するレシピは見つからなかったよ。」と回答してください。

        入力例は適宜変換してください。
        例えば、カレーとカレーライスは同じメニューとして扱ってください。無水カレーもカレーとして扱ってください。

        入力例:
        メニューの場合の例: カレー、カレーライス、無水カレー
        素材の場合の例: 豚肉、牛肉、玉ねぎ

        フォーマット:
        【メニュー: <メニュー名>】
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
    ])

    document_chain = create_stuff_documents_chain(llm, prompt)

    vectorstore = initialize_vectorstore()
    retriever = vectorstore.as_retriever()

    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": recipe})
    answer = response["answer"]
    logger.info("Answer: %s", answer)

    return answer
