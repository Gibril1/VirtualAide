import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.vectorstores.chroma import Chroma
from config.chromadb import ChromaDb
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import RetrievalQA

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

retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":1})

class LangChainService:
    def create_chain(self):
        prompt = ChatPromptTemplate.from_template(""" You are helpful Virtual Executive assistant. You have been provided with a context which holds conversations about team mates in a software engineering company. You are supposed to help them plan the task they have by taking updates from them and answering questions
                                                  
        Context: {context}
        Question: {input}
    """)
        
        chain = create_stuff_documents_chain(
            llm=llm,
            prompt=prompt
        )

        
        
        retrieval_chain = create_retrieval_chain(retriever, chain)

        return retrieval_chain
    
    def chat_with_bot(self, prompt:str):
        chain = self.create_chain()
        response = chain.invoke({
            "input": prompt
        })

        return response['context'][0].page_content


    
    
