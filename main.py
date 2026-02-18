from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
            model="gpt-4o",  # or other OpenAI chat models like "gpt-3.5-turbo"
            temperature=0,  # Controls randomness of output (0-1)
            max_tokens=None, # Maximum number of tokens to generate
        )
from langchain.schema import HumanMessage, SystemMessage
messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="What is the capital of France?"),
        ]
response = llm.invoke(messages)
print(response.content)