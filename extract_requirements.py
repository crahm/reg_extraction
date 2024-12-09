"""main module"""

import json
import spacy
import pytextrank
from tqdm import tqdm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.language_models.fake import FakeListLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.documents.base import Document
from config import settings


def rank_phrases(spacy_doc: spacy.tokens.Doc, n: int = 30) -> str:
    """
    Take a spacy document, use text_rank to score phrases and return the
    n top-ranked phrases concatenated as a string.
    :param spacy_doc: spacy.tokens.doc.Doc: input document
    :param n: int top-n
    :return: str
    """
    try:
        # check that textrank has been added to the pipeline
        # before creating the document
        phrases = spacy_doc._.phrases
    except AttributeError:
        print(
            """
            Document was created with a spacy pipeline
            which does not contain textrank!
            """
        )
        raise

    ranked_chunks = [phrase.text for phrase in phrases]
    return " ".join(ranked_chunks[:n])


def simulate_llm_summary(prompt: PromptTemplate, document: spacy.tokens.Doc) -> str:
    """
    Use a fake LLM to create a summary
    :param prompt: PromptTemplate LLM instruction
    :param document: spacy.tokens.doc.Doc spacy document
    :return: str summary
    """
    llm = FakeListLLM(responses=[rank_phrases(document, n=settings.model["top_n"])])
    chain = prompt | llm
    summary = chain.invoke({"text": document.text})
    return summary


def load_documents() -> list[Document]:
    """
    loads text file, splits recursively into chunks
    and returns and list of langchain documents
    :return: list[Document]
    """
    text_loader = TextLoader(settings.data["input_path"])
    text = text_loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        separators=settings.splitter["separator"],
        chunk_size=settings.splitter["chunk_size"],
        chunk_overlap=settings.splitter["chunk_overlap"],
        length_function=len,
        is_separator_regex=False,
    )
    documents = text_splitter.split_documents(text)
    return documents


def main():
    """
    Executor function loading models and documents,
    iterating over each document, creating summaries
    and writing results to disc.
    :return:
    """
    prompt = PromptTemplate(
        template=settings.model["prompt"],
        input_variables=["text"],
    )
    nlp = spacy.load(settings.model["spacy_model"])
    nlp.add_pipe("textrank")
    documents = load_documents()
    output = []
    for i, document in tqdm(enumerate(documents)):
        doc = nlp(document.page_content)
        summary = simulate_llm_summary(prompt, doc)
        output.append(
            {
                "section_number": i,
                "text": document.page_content,
                "summary": summary,
                "text_len": len(document.page_content),
                "summary_len": len(summary),
                "len_ratio": len(summary) / len(document.page_content),
            }
        )

    with open(settings.data["output_path"], "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)


if __name__ == "__main__":
    main()
