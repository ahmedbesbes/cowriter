from functools import lru_cache
import json
from pathlib import Path
from rich.console import Console
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain, LLMChain
from langchain.callbacks import StreamingStdOutCallbackHandler

console = Console()


@lru_cache(maxsize=None)
def get_chain(model_name, temperature, is_listicle, use_streaming=False):
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                Path(
                    "src/prompts/listicle_writer.prompt"
                    if is_listicle
                    else "src/prompts/article_writer.prompt"
                ).read_text()
            ),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )

    callbacks = [StreamingStdOutCallbackHandler()] if use_streaming else None

    if model_name == "gpt3.5":
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=temperature,
            streaming=use_streaming,
            callbacks=callbacks,
        )
    elif model_name == "gpt4":
        llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=temperature,
            streaming=use_streaming,
            callbacks=callbacks,
        )

    memory = ConversationBufferWindowMemory(
        k=1 if is_listicle else 5,
        return_messages=True,
    )

    chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=chat_prompt,
    )
    return chain


def generate_sections_from_introduction(introduction: str):
    llm = ChatOpenAI(temperature=0.8)
    prompt = PromptTemplate(
        template=Path("src/prompts/section_extractor.prompt").read_text(),
        input_variables=["introduction"],
    )
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
    )
    sections = chain.run(introduction)
    sections = json.loads(sections)
    sections = sections["sections"]
    return sections


def generate_topic_from_listicle_sections(listicle_sections: list):
    topics = [section["section_topic"] for section in listicle_sections]
    llm = ChatOpenAI(temperature=0.8)
    items = "- " + "\n- ".join(topics)
    prompt = PromptTemplate(
        template=Path("src/prompts/guess_topic.prompt").read_text(),
        input_variables=["items"],
    )
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
    )
    topic = chain.run(items)
    return topic
