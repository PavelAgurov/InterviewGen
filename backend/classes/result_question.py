"""
    Result question
"""
# pylint: disable=C0301,C0103,C0303,C0411,W1203

from dataclasses import dataclass

@dataclass
class ResultQuestion:
    """
        Result question
    """
    question    : str
    explanation : str
    
