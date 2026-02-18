from head.utility.yt_transcription import Transcription
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class vector_store:
    def __init__(self, url):
        self.url = url
        self.chunks = Transcription(self.url).transcript()

    def my_invoke(self, question):
        self.question = question

        # Handle transcript errors
        if isinstance(self.chunks, str):
            return self.chunks  # return the error string like "No captions available..."

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        vector_store = FAISS.from_documents(self.chunks, embeddings)
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

        prompt = PromptTemplate(
            template="""
                You are a helpful assistant.
                Answer ONLY using the provided transcript context, as if you are explaining to a beginner in the field.
                Respond in bullet points.
                If the context is insufficient, say "I don't know based on the given context."

                Context:
                {context}

                Question:
                {question}
            """,
            input_variables=['context', 'question']
        )

        # format retrieved docs into plain text
        def format_docs(retrieved_docs):
            return "\n\n".join(doc.page_content for doc in retrieved_docs)

        parallel_chain = RunnableParallel({
            'context': retriever | RunnableLambda(format_docs),
            'question': RunnablePassthrough()
        })

        # final_prompt = prompt.invoke({"question": question})
        parser = StrOutputParser()
        main_chain = parallel_chain | prompt | llm | parser

        # FIX: pass dictionary to invoke()
        result = main_chain.invoke(self.question)
        return result
