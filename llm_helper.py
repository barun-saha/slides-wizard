from langchain import HuggingFaceHub, PromptTemplate

from global_config import GlobalConfig


prompt = None


def get_llm() -> HuggingFaceHub:
    llm = HuggingFaceHub(
        repo_id=GlobalConfig.LLM_MODEL_NAME,
        task='text-generation',
        huggingfacehub_api_token=GlobalConfig.HUGGINGFACEHUB_API_TOKEN,
        model_kwargs={
            'temperature': GlobalConfig.LLM_MODEL_TEMPERATURE,
            'min_length': GlobalConfig.LLM_MODEL_MIN_OUTPUT_LENGTH,
            'max_length': GlobalConfig.LLM_MODEL_MAX_OUTPUT_LENGTH,
            'max_new_tokens': GlobalConfig.LLM_MODEL_MAX_OUTPUT_LENGTH,
            'num_return_sequences': 1
        }
    )
    print(llm)

    return llm


def generate_slides_content(name: str, topic: str, audience: str) -> str:
    """
    Generate the outline/contents of slides for a presentation on a given topic.

    :return: The content
    """

    global prompt

    if not prompt:
        with open(GlobalConfig.SLIDES_TEMPLATE_FILE, 'r') as in_file:
            template_txt = in_file.read().strip()

        prompt = PromptTemplate.from_template(template_txt)

    formatted_prompt = prompt.format(topic=topic, audience=audience)
    # print(formatted_prompt)

    llm = get_llm()
    slides_content = llm(formatted_prompt, verbose=True)

    return slides_content


def text_to_json(content: str) -> str:
    """
    Convert input text into structured JSON representation.

    :param content: Input text
    :return: JSON string
    """

    # f-string is not used in order to prevent interpreting the brackets
    text = '''
    Context:


    '''
    text += content
    text += '''


    Convert the above text into structured JSON output. The JSON structure should be something like this:
    {
        "presentation_title": "...",
        "slides": [
            {
                "slide_number": "...",
                "slide_heading": "...",
                "slide_contents": [
                    "...",
                    "...",
                ],
            },
            {
                ...
            },
        ]
    }
    '''

    llm = get_llm()
    output = llm(text, verbose=True)
    output = output.strip()

    first_index = max(0, output.find('{'))
    last_index = min(output.rfind('}'), len(output))
    output = output[first_index: last_index + 1]

    return output
