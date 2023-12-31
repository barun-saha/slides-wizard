from dataclasses import dataclass
from dotenv import load_dotenv
import os


load_dotenv()


@dataclass(frozen=True)
class GlobalConfig:
    HUGGINGFACEHUB_API_TOKEN: str = os.getenv('HUGGINGFACEHUB_API_TOKEN')

    LLM_MODEL_NAME = 'tiiuae/falcon-7b-instruct'
    # LLM_MODEL_NAME = 'h2oai/h2ogpt-gm-oasst1-en-2048-falcon-7b-v2'
    # LLM_MODEL_NAME = 'garage-bAInd/Platypus2-70B-instruct'
    LLM_MODEL_TEMPERATURE: float = 0.5
    LLM_MODEL_MIN_OUTPUT_LENGTH: int = 50
    LLM_MODEL_MAX_OUTPUT_LENGTH: int = 2000
    LLM_MODEL_MAX_INPUT_LENGTH: int = 1000

    PRELOAD_DATA_FILE = 'examples/example_02.json'
    SLIDES_TEMPLATE_FILE = 'langchain_templates/template_07.txt'

