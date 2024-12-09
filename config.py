"""Configuration setup"""

from pathlib import Path
from dynaconf import Dynaconf, Validator


settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
    validators=[
        Validator("data.input_path", cast=Path),
        Validator("data.output_path", cast=Path),
        Validator("splitter.chunk_size", cast=int),
        Validator("splitter.chunk_overlap", cast=int),
        Validator("splitter.separator", cast=list[str]),
        Validator("model.top_n", cast=int),
        Validator("model.spacy_model", cast=str),
        Validator("model.prompt", cast=str),
    ],
)
