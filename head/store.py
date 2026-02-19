from head.utility.yt_transcription import Transcription
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class VectorStore:
    def __init__(self, url):
        self.url = url
        self.chunks = Transcription(self.url).transcript()

        if isinstance(self.chunks, str):
            self.error = self.chunks
            self.retriever = None
        else:
            self.error = None

            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            self.vector_store = FAISS.from_documents(self.chunks, embeddings)

            self.retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )

    def my_invoke(self, question):

        if self.error:
            return self.error

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

        prompt = PromptTemplate(
            template="""
You are a helpful assistant.
Answer ONLY using the provided transcript context.
Explain like a beginner.
Respond in bullet points.
If the context is insufficient, say "I don't know based on the given context."

Context:
{context}

Question:
{question}
""",
            input_variables=["context", "question"]
        )

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        parallel_chain = RunnableParallel({
            "context": self.retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        })

        parser = StrOutputParser()

        main_chain = parallel_chain | prompt | llm | parser

        return main_chain.invoke(question)
