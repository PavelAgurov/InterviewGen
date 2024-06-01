"""
    Result topic
"""
# pylint: disable=C0301,C0103,C0303,C0411,W1203

from dataclasses import dataclass
from backend.classes.result_question import ResultQuestion

   
@dataclass
class ResultTopic:
    """
        Topic with questions
    """
    topic_name : str
    questions : list[ResultQuestion]
