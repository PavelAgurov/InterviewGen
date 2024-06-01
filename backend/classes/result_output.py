"""
    Result output
"""
# pylint: disable=C0301,C0103,C0303,C0411,W1203

from dataclasses import dataclass
from backend.classes.result_topic import ResultTopic

   
@dataclass
class ResultOuput:
    """
        Output of interview questions
    """
    topics      : list[ResultTopic]
    error       : str
    tokens_used : int
