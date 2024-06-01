"""
    Core module
"""
# pylint: disable=C0301,C0103,C0303,C0411,W1203

import logging
from typing import Any
from backend.llm_core import LLMCore 

from backend.classes.result_output import ResultOuput

logger : logging.Logger = logging.getLogger()

class Core:
    """
        Core class for back-end
    """

    llm_backend = None

    def __init__(self, all_settings : dict[str, Any]):
        logger.info("Core init")
        self.llm_backend = LLMCore(all_settings)

    def generate_interview_questions(self, job_title : str, profile : str, question_count : int) -> ResultOuput:
        """
            Generate interview questions
        """
        try:
            logger.info("Generate interview questions...")
            return self.llm_backend.generate_interview_questions(job_title, profile, question_count)
        except Exception as error: # pylint: disable=broad-except
            error_str = f"Error generating interview questions ({error})"
            return ResultOuput([], error_str, 0)
