import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.vectorstores.chroma import Chroma
from config.chromadb import ChromaDb
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate

chroma = ChromaDb()
llm = ChatOpenAI(
    model='gpt-3.5-turbo',
    temperature=0.3
)

db = Chroma(
    collection_name="ceo_project_collection",
    client=chroma.client,
    embedding_function=OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))
)
class LangChainService:
    def create_chain(self):
        template = """
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Use three sentences maximum and keep the answer as concise as possible.
        Always politely request if they would like to know more or anything else they want to know.

        {context}

        Question: {question}

        Helpful Answer:
        """

        prompt = PromptTemplate(template)
        retriever = db.as_retriever()

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)


        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        return rag_chain
    
    def chat_with_bot(self, prompt:str):
        chain = self.create_chain()

        response = chain.invoke(prompt)

        return response