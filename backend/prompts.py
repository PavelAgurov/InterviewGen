"""
    LLM Prompts
"""

GENERATE_INTERVIEW_QUESTIONS_PROMPT = """
I want you to act as an interviewer. 
Generate me {question_count} the interview questions for the {job_title} position.
Your questions should cover different aspects of work.

{profile_note}

Only reply with English. Answer in XML format.

<generated_questions>
    <topic name="topic">
        <question_item>
            <question>question here</question>
            <explanation>explain why the question is relevant to the provided candidate's profile</explanation>
        </question_item>
        
    </topic>
</generated_questions>
"""
