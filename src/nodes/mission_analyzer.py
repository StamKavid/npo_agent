from typing import Dict, Any
import logging

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

from src.utils.exceptions import LLMAnalysisError

def mission_analyzer(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the organization's mission and core characteristics
    
    :param state: Current state of the audit process
    :param config: Configuration dictionary
    :return: Updated state with mission analysis
    """
    logger = logging.getLogger(__name__)
    logger.info("Analyzing organization mission")
    
    if not state.get('raw_content'):
        logger.warning("No content available for mission analysis")
        state['mission_analysis'] = "No content available for analysis"
        return state
    
    try:
        llm = ChatOpenAI(
            temperature=0.2,
            base_url=config.get('configurable', {}).get('local_llm_base_url', "http://localhost:1234/v1"),
            api_key="not-needed",
            model_name="local_model"
        )
        
        mission_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
            You are an expert nonprofit organizational analyst. 
            Extract and analyze the core mission, primary goals, 
            and key characteristics of the organization from the given content.
            
            Focus on:
            - Mission statement
            - Primary objectives
            - Target beneficiaries
            - Unique value proposition
            """),
            HumanMessage(content=f"Analyze the following organizational content:\n{state['raw_content']}")
        ])
        
        response = llm.invoke(mission_prompt.format_messages())
        state['mission_analysis'] = response.content
    except Exception as e:
        logger.error(f"Mission analysis error: {e}")
        raise LLMAnalysisError(f"Error in mission analysis: {str(e)}")
    
    return state