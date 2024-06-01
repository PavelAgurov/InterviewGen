"""
    Main APP and UI
"""
# pylint: disable=C0301,C0103,C0303,C0411,W1203

import streamlit as st
import logging
import pandas as pd

from ui_utils.utils_streamlit import streamlit_hack_remove_top_space, show_page_header, hide_header_footer
from ui_utils.app_logger import init_streamlit_logger

from backend.core import Core
from backend.classes.result_topic import ResultTopic

all_settings = {s[0]:s[1] for s in st.secrets.items()}

init_streamlit_logger(all_settings.get("RUN_LOCAL", True))

# ------------------------------- Logger
logger : logging.Logger = logging.getLogger()

# ------------------------------- Session
if 'core' not in st.session_state:
    st.session_state.core = Core(all_settings)
if 'tokens_currently_used' not in st.session_state:
    st.session_state.tokens_currently_used = 0
if 'tokens_total_used' not in st.session_state:
    st.session_state.tokens_total_used = 0
if 'errors' not in st.session_state:
    st.session_state.errors = None
if 'result_topic_list' not in st.session_state:
    st.session_state.result_topic_list = []

# ------------------------------- UI
show_page_header(
    "Interview Generator",
    "With help of this application you can generate examples of question for interview.", 
    [
        "Select job title",
        "Enter profile details (if needed)",
        "Enter number of questions (1-40)",
        "Click button Generate"
    ]
)
streamlit_hack_remove_top_space()
hide_header_footer()

st.info(f'Used {st.session_state.tokens_currently_used} tokens. Total used {st.session_state.tokens_total_used} tokens.')

if st.session_state.errors:
    st.error(st.session_state.errors)
    st.session_state.errors = None

job_title = st.text_input("Job Title:", value="Delivery Manager") #"Senior Java Software Engineer")
profile = st.text_area("Profile details:", value="", placeholder ="Optional profile details to include in questions")

question_count = st.number_input("Number of Questions:", value=10, min_value=1, max_value=40, step=1)
button_generate = st.button("Generate")

result_topic_list : list[ResultTopic] = st.session_state.result_topic_list
question_list_container = st.container(border=True)
for topic_item in result_topic_list:
    question_list_container.markdown(f'**{topic_item.topic_name}**')
    question_df = pd.DataFrame([[q.question, q.explanation] for q in topic_item.questions], columns = ['Question', 'Explanation'])
    question_list_container.dataframe(question_df, hide_index=True, use_container_width=True)    

def update_used_tokens(currently_used = 0):
    """Update token counters"""
    st.session_state.tokens_currently_used = currently_used
    st.session_state.tokens_total_used += currently_used

update_used_tokens()

if button_generate:
    if not job_title:
        st.session_state.operation_errors = "Please enter a valid job title"
    else:
        with st.spinner("Generating questions..."):
            result_output = st.session_state.core.generate_interview_questions(job_title, profile, question_count)
            st.session_state.result_topic_list = result_output.topics
        tokens_used = result_output.tokens_used
        update_used_tokens(tokens_used)
    st.rerun()
