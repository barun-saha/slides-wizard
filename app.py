import json

import streamlit as st

import llm_helper
from global_config import GlobalConfig


UI_BUTTONS = [
    'Generate slides content',
    'Generate JSON',
    'Make the slides'
]


def build_ui():
    """
    Display the input elements for content generation. Only covers the first step.
    """

    st.title('Slides Wizard')
    st.subheader('*:blue[Create your next slide deck using AI]*')
    st.divider()

    st.header('Step 1: Generate your content')
    st.caption('Let\'s start by generating some contents for your slides')

    # name = st.text_input(
    #     f'''**Type in your name**''',
    #     value='John Doe'
    # )

    try:
        with open(GlobalConfig.PRELOAD_DATA_FILE, 'r') as in_file:
            preload_data = json.loads(in_file.read())
    except (FileExistsError, FileNotFoundError):
        preload_data = {'topic': '', 'audience': ''}

    topic = st.text_area(
        f'''**Describe the topic of the presentation. 
        Avoid mentioning the count of slides.**''',
        value=preload_data['topic']
    )

    audience = st.text_input(
        f'''**Briefly describe your target audience**''',
        value=preload_data['audience']
    )

    # Button with callback function
    st.button(UI_BUTTONS[0], on_click=button_clicked, args=[0])

    if st.session_state.clicked[0]:
        progress_text = 'Generating your presentation slides...give it a moment'
        progress_bar = st.progress(0, text=progress_text)

        # name_txt = name.strip()
        topic_txt = topic.strip()
        audience_txt = audience.strip()

        process_topic_inputs('', topic_txt, audience_txt, progress_bar)


def process_topic_inputs(name: str, topic: str, audience: str, progress_bar):
    """
    Process the inputs to generate contents for the slides.

    :param name: Name of the speaker
    :param topic: The presentation topic
    :param audience: Target audience description
    :param progress_bar: Progress bar from the page
    :return:
    """

    # name_length = len(name)
    topic_length = len(topic)
    audience_length = len(audience)
    print(f'Input lengths:: topic: {topic_length}, audience: {audience_length}')

    if topic_length > 10 and audience_length > 5:
        print(
            f'Name: {name}\n'
            f'Topic: {topic}\n'
            f'Audience: {audience}'
        )
        print('=' * 20)

        target_length = min(topic_length, GlobalConfig.LLM_MODEL_MAX_INPUT_LENGTH)

        try:
            slides_content = llm_helper.generate_slides_content(name, topic[:target_length], audience)

            print('=' * 20)
            print(f'Slides content:\n{slides_content}')
            print('=' * 20)
            st.write(f'''Slides content:\n{slides_content}''')
            progress_bar.progress(100, text='Done!')

            # Move on to step 2
            st.divider()
            st.header('Step 2: Make it structured')
            st.caption('Let\'s now convert the above generated contents into JSON')

            # Streamlit multiple buttons work in a weird way!
            # Click on any button, the page just reloads!
            # Buttons are not "stateful"
            # https://blog.streamlit.io/10-most-common-explanations-on-the-streamlit-forum/#1-buttons-aren%E2%80%99t-stateful
            # Apparently, "nested button click" needs to be handled differently
            # https://playground.streamlit.app/?q=triple-button

            st.button(UI_BUTTONS[1], on_click=button_clicked, args=[1])

            if st.session_state.clicked[1]:
                progress_text = 'Converting...give it a moment'
                progress_bar = st.progress(0, text=progress_text)

                process_slides_contents(slides_content, progress_bar)
        except ValueError as ve:
            st.error(f'Unfortunately, an error occurred: {ve}! '
                     f'Please change the text, try again later, or report it, sharing your inputs.')

    else:
        st.error('Not enough information provided! Please be little more descriptive :)')


def process_slides_contents(text: str, progress_bar: st.progress):
    """
    Convert given content to JSON and display. Update the UI.

    :param text: The contents generated for the slides
    :param progress_bar: Progress bar for this step
    """

    print('JSON button clicked')
    json_str = llm_helper.text_to_json(text)
    print('=' * 20)
    print(f'JSON:\n{json_str}')
    print('=' * 20)
    st.code(json_str, language='json')

    progress_bar.progress(100, text='Done!')


def button_clicked(button):
    """
    Function to update the value in session state.
    """

    st.session_state.clicked[button] = True


def main():
    # Initialize the key in session state to manage the nested buttons states
    if 'clicked' not in st.session_state:
        st.session_state.clicked = {0: False, 1: False, 2: False}

    build_ui()


if __name__ == '__main__':
    main()
