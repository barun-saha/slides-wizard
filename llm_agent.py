from langchain import HuggingFaceHub, PromptTemplate

from global_config import GlobalConfig


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

#
# so that the speaker can deliver an engaging talk to the target audience. You use facts in your slides. When necessary,
# you also look up online for further details

template = '''
You are an artificial intelligence assistant. 
You are experienced in creating slides for a presentation on any given topic.
Generate a slide deck based on the following information:


Topic: 
```{topic}```


Target audience:
```{audience}```


Generate an engaging title for the presentation and output it as the first line.
The next line should contain the speaker's name.
Add a title and number to each slide on a separate line.
Each slide should have a bulleted list of items to talk about.
'''


template2 = '''
Act like a professional speaker and expert in PowerPoint: Create the outline for a PowerPoint presentation on 
any given topic. Include main headings for each slide, detailed bullet points for each slide, 
ideas for photos for each slide and an impactful intro and closing slide.


Speaker's name:
```{name}```


Topic: 
```{topic}```


Target audience:
```{audience}```


Generate an engaging title for the presentation and output it in the first line.
The next line should contain the speaker's name.
Add a title and number to each slide on a separate line.
'''

# The contents of the slides should be in plain-text in the form of bulleted list items.

with open('langchain_templates/template_07.txt', 'r') as in_file:
    template_txt = in_file.read().strip()

# prompt = PromptTemplate.from_template(template)
prompt = PromptTemplate.from_template(template_txt)


def generate_slides_content(name: str, topic: str, audience: str) -> str:
    """
    Generate the contents of slides for a presentation on a given topic.

    :return: The summary
    """

    formatted_prompt = prompt.format(topic=topic, audience=audience)
    print(formatted_prompt)

    slides_content = llm(formatted_prompt)

    return slides_content
