import gensim.downloader as api
from gensim.corpora import WikiCorpus
import os
import urllib.request
import bz2

WIKI_DUMP_URL = "https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2"
WIKI_DUMP_FILENAME = "enwiki-latest-pages-articles.xml.bz2"


def download_wiki_dump(output_path):
    """
    Download the Wikipedia dump file.

    :param output_path: Path to save the downloaded file
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_path = os.path.join(output_path, WIKI_DUMP_FILENAME)

    if not os.path.exists(file_path):
        print(f"Downloading Wikipedia dump from {WIKI_DUMP_URL}")
        print("This may take a while...")
        urllib.request.urlretrieve(WIKI_DUMP_URL, file_path)
        print("Download complete.")
    else:
        print(f"Wikipedia dump file already exists at {file_path}")


def download_wiki_corpus(output_path, num_articles=10000):
    """
    Download and process Wikipedia articles.

    :param output_path: Path to save the processed corpus
    :param num_articles: Number of articles to process (default: 10000)
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    dump_path = os.path.join(output_path, WIKI_DUMP_FILENAME)

    if not os.path.exists(dump_path):
        download_wiki_dump(output_path)

    # Process the Wikipedia dump
    wiki = WikiCorpus(dump_path, dictionary={})

    with open(os.path.join(output_path, "wiki_corpus.txt"), "w", encoding="utf-8") as output:
        for i, text in enumerate(wiki.get_texts()):
            if i >= num_articles:
                break
            output.write(" ".join(text) + "\n")
            if i % 1000 == 0:
                print(f"Processed {i} articles")


def load_wiki_corpus(file_path):
    """
    Load the processed Wikipedia corpus.

    :param file_path: Path to the processed corpus file
    :return: List of tokenized sentences
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip().split() for line in f]


if __name__ == "__main__":
    download_wiki_corpus("../data")
