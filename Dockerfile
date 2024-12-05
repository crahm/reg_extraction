FROM python:3.12

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_lg
CMD [ "python", "./extract_requirements.py"]
