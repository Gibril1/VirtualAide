import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from config.chromadb import ChromaDb

# Init ChromaDB
chroma_config = ChromaDb()

# Init GPT Model
llm = ChatOpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    model='gpt-3.5-turbo-1106',
    temperature=0.4
)

db = Chroma(
    client=chroma_config.client,
    collection_name="ceo_project_collection",
    embedding_function=OpenAIEmbeddings()
)

class ChatBotService:
    def create_rag_chain(self):
        retriever = db.as_retriever(search_type="similarity",search_kwargs={"k":1})
        template_str = """You are helpful Virtual Executive assistant. You have been provided with a context which holds conversations about team mates in a software engineering company. You are supposed to help them plan the task they have by taking updates from them and answering questions.
        Context:    {context}
        Question: {question}

        Helpful Answer:
                """
        prompt = PromptTemplate.from_template(template_str)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs[1:2])

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        return rag_chain
    
    def invoke_llm(self, prompt:str):
        chain = self.create_rag_chain()

        response = chain.invoke(prompt)

        return response