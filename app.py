import streamlit as st

import llm_agent
from global_config import GlobalConfig


def build_ui():
    st.write('''
    # Slides Wizard
    
    *Create your next presentation using AI*
    ''')

    name = st.text_input(
        f'''**Type in your name**''',
        value='John Doe'
    )

    topic = st.text_area(
        f'''**Describe the topic of the presentation. 
        Avoid mentioning the count of slides.**''',
        value='''Make a presentation about AI. Talk about its pros, cons, and future prospects. '''
        '''Add examples of some real-life use cases in engineering and medicine.'''
    )

    audience = st.text_input(
        f'''**Briefly describe your target audience**''',
        value='I am a teacher and want to present these slides to college students'
    )

    if st.button('Generate slides'):
        progress_text = 'Generating your presentation slides...give it a moment'
        progress_bar = st.progress(0, text=progress_text)

        name_txt = name.strip()
        topic_txt = topic.strip()
        audience_txt = audience.strip()

        process_inputs(name_txt, topic_txt, audience_txt, progress_bar)


def process_inputs(name: str, topic: str, audience: str, progress_bar):
    name_length = len(name)
    topic_length = len(topic)
    audience_length = len(audience)
    print(f'Input lengths:: name: {name_length}, topic: {topic_length}, audience: {audience_length}')

    if name_length > 0 and topic_length > 10 and audience_length > 5:
        print(
            f'Name: {name}\n'
            f'Topic: {topic}\n'
            f'Audience: {audience}'
        )
        print('=' * 20)

        target_length = min(topic_length, GlobalConfig.LLM_MODEL_MAX_INPUT_LENGTH)

        try:
            slides_content = llm_agent.generate_slides_content(name, topic[:target_length], audience)

            print('=' * 20)
            print(f'Slides content:\n{slides_content}')
            print('=' * 20)
            st.write(f'''Slides content:\n{slides_content}''')
            progress_bar.progress(100, text='Done!')
        except ValueError as ve:
            st.error(f'Unfortunately, an error occurred: {ve}! '
                     f'Please change the text, try again later, or report it, sharing your inputs.')

        # image = generate_image_from_text(summary)
        # progress_bar.progress(100, text='Done!')
        #
        # st.image(image, caption=summary)
        # st.info('Tip: Right-click on the image to save it')
    else:
        st.error('Not enough information provided! Please be little more descriptive :)')


def main():
    build_ui()


if __name__ == '__main__':
    main()
