import json
import time
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from duckduckgo_search import DDGS
from newspaper import Article
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from src import logger


def search_webpages(query: str, max_results=5):
    ddgs = DDGS()
    results = ddgs.text(query)
    pages = []
    count = 0
    for result in results:
        count += 1
        pages.append(result)
        if count > max_results:
            break
    return pages


def extract_article_text(url):
    article = Article(url)
    try:
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        logger.error(str(e))
        return ""


def fetch_(pages):
    for page in pages:
        url = page["href"]
        full_text = extract_article_text(url)
        page["full_text"] = full_text
    return pages


class WebAgent(object):
    def __init__(self, query, max_pages):
        self.query = query
        self.max_pages = max_pages
        self.documents = []
        self.console = Console()

    def load_articles(self):
        pages = search_webpages(self.query, self.max_pages)
        export = []
        for page in pages:
            url = page["href"]
            full_text = extract_article_text(url)
            document = Document(
                page_content=full_text,
                metadata=page,
            )
            self.documents.append(document)
            export.append(dict(document))

        logger.info(f"Loaded {len(self.documents)} documents")

        dt = datetime.now()
        unix_time = time.mktime(dt.timetuple())
        filename = f"documents/{unix_time}_{self.query}.json"
        with open(filename, "w") as f:
            json.dump(export, f)

    def split_articles(self):
        splitter = CharacterTextSplitter(
            separator=" ",
            chunk_size=1024,
            chunk_overlap=0,
        )
        chunks = []
        for document in self.documents:
            for chunk in splitter.split_text(document.page_content):
                chunks.append(
                    Document(
                        page_content=chunk,
                        metadata=document.metadata,
                    )
                )
        self.chunks = chunks
        logger.info(f"Splitted the documents into {len(self.chunks)} chunks")

    def setup_vector_db(self):
        vector_db = Chroma.from_documents(
            self.chunks,
            OpenAIEmbeddings(),
            persist_directory="db",
        )
        self.vector_db = vector_db
        logger.info("Vector DB initialized")

    def setup_llm(self):
        prompt_template = """Use the provided context only to write an answer about the topic below.
        If you don't know the answer, simply say "I don't know how to answer the question".
        Don't use the context as is. You need to rephrase it.
        Context: {context}
        Topic: {topic}
        Answer:
        """
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "topic"],
        )
        llm = ChatOpenAI(temperature=0)
        chain = LLMChain(llm=llm, prompt=PROMPT)
        self.chain = chain
        logger.info("LLM initialized")

    def setup(self):
        logger.info("WebAgent setup ... ⌛")
        self.load_articles()
        self.split_articles()
        self.setup_vector_db()
        self.setup_llm()
        logger.info("WebAgent setup done ✅")

    def run(self):
        while True:
            topic = Prompt.ask(":robot: Ask a question")
            docs = self.vector_db.similarity_search(topic, k=4)
            context = "\n $$$$$ \n".join([doc.page_content for doc in docs])

            self.console.rule(style="red bold")
            for i, doc in enumerate(docs):
                self.console.print(f"Document {i} :")
                self.console.print(doc.metadata)
                self.console.print(doc.page_content)
                self.console.rule(style="red bold")

            inputs = {
                "context": context,
                "topic": topic,
            }

            with self.console.status(
                "Thinking and generating the answer ...\n",
                spinner="aesthetic",
                speed=1.5,
                spinner_style="red",
            ):
                output = self.chain.run(**inputs)
                self.console.print("[bold red]Answer [bold red/]")
                self.console.print(output)


# only for demos

if __name__ == "__main__":
    console = Console()
    query = Prompt.ask("[red bold]Type in your search query[red bold/]")
    is_valid = False
    while not is_valid:
        max_pages = Prompt.ask(
            "[red bold]Maximum number of web pages to search (must be an int)[red bold/]",
            default="5",
        )
        try:
            max_pages = int(max_pages)
            is_valid = True
        except Exception as e:
            is_valid = False
    console.rule(style="bold red")
    web_agent = WebAgent(query=query, max_pages=max_pages)
    web_agent.setup()
    console.rule(style="bold red")
    web_agent.run()
