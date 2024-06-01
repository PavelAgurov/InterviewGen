"""
    Utils for streamlit
"""
# pylint: disable=C0301,C0103,C0303,C0411,W1203

import streamlit as st
import streamlit.components.v1 as components

# https://discuss.streamlit.io/t/prevent-st-text-input-from-triggering-callback-when-losing-focus/37103/3

def streamlit_hack_disable_textarea_submit():
    """Do not submit TextArea component when lost focus"""
    components.html(
            """
        <script>
        const doc = window.parent.document;

        const textareas = doc.querySelectorAll('textarea');
        textareas.forEach(textarea => {
            textarea.addEventListener('focusout', function(event) {
                event.stopPropagation();
                event.preventDefault();
            });
        });

        const inputs = doc.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('focusout', function(event) {
                event.stopPropagation();
                event.preventDefault();
            });
        });
        
        </script>""",
            height=0,
            width=0,
        )

def streamlit_hack_remove_top_space():
    """Remove top space of streamlit windos"""
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

    # https://discuss.streamlit.io/t/how-to-keep-the-pages-menu-expanded-in-multipage-apps/40775/3
    st.markdown("""
        <style>
            div[data-testid='stSidebarNav'] ul {
                max-height:none;
                padding-top: 2rem;
            }
        </style>
        """, unsafe_allow_html=True)


def hide_footer():
    """Hide footer"""
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    
# https://github.com/streamlit/streamlit/issues/3587
def update_multiselect_style():
    """Update multiselect style"""
    st.markdown(
        """
        <style>
            .stMultiSelect [data-baseweb="tag"] {
                height: fit-content;
            }
            .stMultiSelect [data-baseweb="tag"] span[title] {
                white-space: normal; max-width: 100%; overflow-wrap: anywhere;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# https://github.com/streamlit/streamlit/issues/3587
def update_selectbox_style():
    """Update selectbox style"""
    st.markdown(
        """
        <style>
            .stSelectbox [data-baseweb="select"] div[aria-selected="true"] {
                white-space: normal; overflow-wrap: anywhere;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
__MD_SPECIAL_CHARS = "`*_{}[]()#+.!:"

def escape_markdown(text : str) -> str:
    """
        Escape markdown special characters
    """
    for char in __MD_SPECIAL_CHARS:
        text = text.replace(char, "\\"+char)
    return text

def get_param_from_url(param_name : str, default_value : any) -> any:
    """Get param from URL"""
    return type(default_value)(st.query_params.get(param_name, default_value))

# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
__STREAMLIT_NUMBERS_DICT = {
    0 : ":zero:",
    1 : ":one:",
    2 : ":two:",
    3 : ":three:",
    4 : ":four:",
    5 : ":five:",
    6 : ":six:",
    7 : ":seven:",
    8 : ":eight:",
    9 : ":nine:",
}

def get_streamlit_number(index : int, details_count : int) -> str:
    """Get streamlit number as icons"""

    if details_count < 10:
        string_index = str(index)
    else:
        string_index = str(index).zfill(details_count)

    string_result = ""
    for char in string_index:
        string_result += __STREAMLIT_NUMBERS_DICT[int(char)]

    return string_result
    

def add_numeration(details : list[str]) -> list[str]:
    """Add numeration to the list of details"""
    return [f"{get_streamlit_number(index+1, len(details))} {detail}" for index, detail in enumerate(details)]

def show_page_header(page_title : str, description : str, details : list[str] = None):
    """Show page header"""
    st.set_page_config(page_title= page_title, layout="wide", initial_sidebar_state="expanded")
    streamlit_hack_remove_top_space()
    update_selectbox_style()
    update_multiselect_style()
    st.markdown(f"# {page_title}")
    
    if details and len(details) > 0:
        with st.expander(f":point_right: {description}"):
            st.markdown("\n\n".join(add_numeration(details)))
    else:
        st.markdown(f":point_right: {description}")
