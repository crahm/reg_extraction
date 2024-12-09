# Regulation Extraction

This project processes a text file, splits it into chunks 
and simulates using a Large Language Model (LLM) to 
summarise each chunk.

The text example uses a 
[regulatory document](https://www.fca.org.uk/publication/consultation/cp24-24.pdf) 
from the Financial Conduct Authority (FCA).

The code in `extract_requirements.py` uses `LangChain` to load the document and split it into chunks.
To create the summary for each chunk,
`Langchain`'s `FakeListLLM` is a useful tool for simulating the use of an LLM.
It will produce outputs from a given list.

The possible `FakeListLLM` outputs are generated through the TextRank algorithm in a `spaCy` implementation.
TextRank ranks the phrases in a spacy document and is a well-known method for extractive summarisation.
The summary is produced by taking a number of top-ranked phrases, 
concatenating them and using them as the only output choice for `FakeListLLM`.

The summaries are written to `extracted_requirements.json` 
together with 
- the number of the section within the document
- the original text
- the length of the original text
- the length of the summary text
- the ratio of the lengths of summary and original text

The length ratio varies naturally with the document 
splitting method, the size of the resulting chunks, 
and the number of top-ranked phrases taken into account.

A number of configuration parameters can be adjusted in `settings.toml`,
in particular 
- input and output paths
- splitting parameters
- spacy model and desired number of top-ranked phrases

## Code execution

The project contains a `docker-compose.yml` and `Dockerfile` which allow for easy code execution.
Just run 

```bash
docker-compose up
```

from within the project folder.
The specified python version is 3.12.
Once the container is built, the execution took 
around 25 seconds on my computer with the given 
parameter settings.


## File Content

The project contains the following files:
- README.md: Project description
- extract_requirements.py: main executable
- requirements.txt: package list
- Datafiles:
  - regulations.txt: input file
  - extracted_requirements.json: output file
- Container setup
  - docker-compose.yml
  - Dockerfile
- Dynaconf configuration files
  - config.py  
  - settings.toml
  - .secrets.toml