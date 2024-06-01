"""
    LLM Core
"""
# pylint: disable=C0301,C0103,C0303,C0411,W1203

import logging
from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.callbacks import get_openai_callback

from backend import prompts
from backend import xml_utils
from backend.llm_base_core import LLMBaseCore

from backend.classes.result_output import ResultOuput
from backend.classes.result_topic import ResultTopic
from backend.classes.result_question import ResultQuestion

logger : logging.Logger = logging.getLogger()

class LLMCore(LLMBaseCore):
    """
        LLM Core
    """
    chain_generate = None

    def __init__(self, all_settings : dict[str, Any]):
        LLMBaseCore.__init__(self, all_settings)

        # Init LLM
        model_name = all_settings.get('BASE_MODEL_NAME')
        max_tokens = all_settings.get('MAX_TOKENS')
        logger.info(f"LLM index model name: {model_name}")
        logger.info(f"LLM index max tokens: {max_tokens}")

        llm = self.create_llm(max_tokens, model_name)

        # Init chains
        generate_prompt = ChatPromptTemplate.from_template(prompts.GENERATE_INTERVIEW_QUESTIONS_PROMPT)
        self.chain_generate  = generate_prompt | llm | StrOutputParser()

    def generate_interview_questions(self, job_title : str, profile : str, question_count : int) -> ResultOuput:
        """
            Generate inverview questions
        """
        
        profile_note = ""
        if profile:
            profile = profile.replace("&", " and ")
            profile_note = f"When you build question, first take into account the candidate's profile to be more concrete. <profile>{profile}</profile>"

        with get_openai_callback() as cb:
            result_xml = self.chain_generate.invoke({
                "job_title" : job_title,
                "profile_note" : profile_note,
                "question_count" : question_count,
            })
        tokens_used = cb.total_tokens
       
        result_xml = self.extract_llm_xml_string(result_xml)
        logger.debug(f"LLM generated questions: {result_xml}")
        logger.debug(f"LLM used tokens: {tokens_used}")
        
        result_topics : list[ResultTopic] = []
        try:
            x = xml_utils.get_as_xml(result_xml)
        except Exception as error: # pylint: disable=broad-except
            logger.error(error)
        for topic_element in x.findall('topic'):
            topic_name = topic_element.attrib['name']
            topic_item : ResultTopic = ResultTopic(topic_name, list[ResultQuestion]())
            for question_element in topic_element.findall('question_item'):
                question_text = question_element.find('question').text.strip()
                explanation   = question_element.find('explanation').text.strip()
                topic_item.questions.append(ResultQuestion(question_text, explanation))
            result_topics.append(topic_item)
            
        return ResultOuput(result_topics, "", tokens_used)
    
