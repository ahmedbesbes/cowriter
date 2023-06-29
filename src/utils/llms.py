from functools import lru_cache
from pathlib import Path
from rich.console import Console
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain.callbacks import StreamingStdOutCallbackHandler

console = Console()


@lru_cache(maxsize=None)
def get_chain(use_streaming=False):
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                Path("src/prompts/system.prompt").read_text()
            ),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )

    callbacks = [StreamingStdOutCallbackHandler()] if use_streaming else None

    llm = ChatOpenAI(
        temperature=0.8,
        streaming=use_streaming,
        callbacks=callbacks,
    )

    memory = ConversationBufferWindowMemory(
        k=5,
        return_messages=True,
    )

    chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=chat_prompt,
    )
    return chain
