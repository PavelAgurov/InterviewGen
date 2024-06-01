"""
    Base class for LLM Core
"""
# pylint: disable=C0301,C0103,C0303,C0411,W1203,C0412

import logging
import os

from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

logger : logging.Logger = logging.getLogger()

class LLMBaseCore:
    """
        Base class for LLM Core
    """

    openai_api_type : str
    openai_api_deployment : str
    all_settings : dict[str, any]

    def __init__(self, all_settings : dict[str, any]):
        """
            Constructor
        """

        # save settings
        self.all_settings = all_settings

        # Init cache
        set_llm_cache(SQLiteCache(database_path=".langchain_cache\cache.db"))

        # init env
        self.init_llm_environment(all_settings)

    def init_llm_environment(self, all_settings : dict[str, any]):
        """
            Init OpenAI or Azure environment
        """

        self.openai_api_type = 'openai'
        self.openai_api_deployment = None
        if not all_settings:
            return
 
        self.openai_api_type = all_settings.get('OPENAI_API_TYPE')

        if self.openai_api_type == 'openai':
            openai_settings = all_settings.get('open_api_openai')
            if openai_settings:
                os.environ["OPENAI_API_KEY"] = openai_settings.get('OPENAI_API_KEY')
                logger.info(f'Run with OpenAI from config file [{len(os.environ["OPENAI_API_KEY"])}]')
            else:
                logger.error('open_api_openai section is required')
            return

        if self.openai_api_type == 'azure':
            azure_settings = all_settings.get('open_api_azure')
            if azure_settings:
                os.environ["AZURE_OPENAI_API_KEY"] = azure_settings.get('AZURE_OPENAI_API_KEY')
                os.environ["OPENAI_API_TYPE"] = "azure"
                os.environ["OPENAI_API_VERSION"] = azure_settings.get('OPENAI_API_VERSION')
                os.environ["AZURE_OPENAI_ENDPOINT"] = azure_settings.get('AZURE_OPENAI_ENDPOINT')
                self.openai_api_deployment = azure_settings.get('OPENAI_API_DEPLOYMENT')
                logger.info('Run with Azure OpenAI config file')
            else:
                logger.error('open_api_azure section is required')
            return
        
        logger.error(f'init_llm_environment: unsupported OPENAI_API_TYPE: {self.openai_api_type}')

    def create_llm(self, max_tokens : int, model_name : str) -> ChatOpenAI:
        """
            Create LLM
        """

        if self.openai_api_type == 'openai':
            return ChatOpenAI(
                model_name     = model_name,
                max_tokens     = max_tokens,
                temperature    = 0,
                verbose        = False,
                model_kwargs={
                    "frequency_penalty": 0.0,
                    "presence_penalty" : 0.0,
                    "top_p" : 1.0
                }        
            )
        
        if self.openai_api_type == 'azure':
            return AzureChatOpenAI(
                azure_deployment   = self.openai_api_deployment,
                model_name     = model_name,
                max_tokens     = max_tokens,
                temperature    = 0,
                verbose        = False,
                model_kwargs={
                    "frequency_penalty": 0.0,
                    "presence_penalty" : 0.0,
                    "top_p" : 1.0
                }        
            )
        
        logger.error(f'create_llm: unsupported OPENAI_API_TYPE: {self.openai_api_type}')
        return None

    def extract_llm_xml_string(self, sql_xml : str) -> str:
        """
        Extract LLM generated XML string
        """
        sql_xml = sql_xml.strip()
            
        xml_begin = "```xml"
        if sql_xml.startswith(xml_begin):
            sql_xml = sql_xml[len(xml_begin):]

        xml_end = "```"
        if sql_xml.endswith(xml_end):
            sql_xml = sql_xml[:-len(xml_end)]
            
        sql_xml = sql_xml.strip()

        return sql_xml
    
   