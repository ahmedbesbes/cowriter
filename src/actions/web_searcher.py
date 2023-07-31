from argparse import ArgumentParser
from rich.console import Console
from duckduckgo_search import DDGS
from newspaper import Article


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


def extract_full_text(url):
    article = Article(url)
    try:
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        console.log(str(e))
        return ""


def fetch_article_data(pages):
    for page in pages:
        url = page["href"]
        full_text = extract_full_text(url)
        page["full_text"] = full_text
    return pages


# only for demos

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
        "--query",
        default="tutorial python decorators",
        type=str,
    )
    args = argument_parser.parse_args()
    console = Console()
    web_pages = search_webpages(query=args.query)
    article_data = fetch_article_data(web_pages)
    console.print_json(data=article_data)
