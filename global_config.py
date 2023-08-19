from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(frozen=True)
class GlobalConfig:
    HUGGINGFACEHUB_API_TOKEN: str = os.getenv('HUGGINGFACEHUB_API_TOKEN')

    # Flan-T5
    # LLM_MODEL_NAME: str = 'google/flan-t5-xxl'
    LLM_MODEL_NAME = 'tiiuae/falcon-7b-instruct'
    LLM_MODEL_TEMPERATURE: float = 0.5
    LLM_MODEL_MIN_OUTPUT_LENGTH: int = 200
    LLM_MODEL_MAX_OUTPUT_LENGTH: int = 2000
    LLM_MODEL_MAX_INPUT_LENGTH: int = 1000

    # # Stable Diffusion
    # DIFFUSION_MODEL_NAME: str = 'stabilityai/stable-diffusion-2-1'
    # DIFFUSION_NUM_INFERENCE_STEPS: int = 3
