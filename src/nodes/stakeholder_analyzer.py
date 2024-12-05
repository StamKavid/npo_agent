from typing import Dict, Any
import logging

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

from src.utils.exceptions import LLMAnalysisError

def stakeholder_perspective_generator(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate stakeholder perspectives based on mission analysis
    
    :param state: Current state of the audit process
    :param config: Configuration dictionary
    :return: Updated state with stakeholder perspectives
    """
    logger = logging.getLogger(__name__)
    logger.info("Generating stakeholder perspectives")
    
    if not state.get('mission_analysis'):
        logger.warning("No mission analysis available")
        state['stakeholder_perspectives'] = {"Error": "No mission analysis available"}
        return state
    
    try:
        llm = ChatOpenAI(
            temperature=0.2,
            base_url=config.get('configurable', {}).get('local_llm_base_url', "http://localhost:1234/v1"),
            api_key="not-needed",
            model_name="local_model"
        )
        
        perspective_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
            You are an expert in nonprofit stakeholder analysis. 
            Based on the organization's mission and characteristics, 
            identify the most relevant stakeholders and their potential perspectives.
            
            For each stakeholder:
            - Describe their potential interests
            - Highlight their expectations
            - Note potential points of engagement or concern
            
            Provide at least 3 distinct stakeholder perspectives.
            """),
            HumanMessage(content=f"Analyze stakeholder perspectives for this mission:\n{state['mission_analysis']}")
        ])
        
        response = llm.invoke(perspective_prompt.format_messages())
        
        # More robust parsing of stakeholder perspectives
        perspectives = {}
        for perspective in response.content.split('\n'):
            if ':' in perspective:
                stakeholder, details = perspective.split(':', 1)
                perspectives[stakeholder.strip()] = details.strip()
        
        state['stakeholder_perspectives'] = perspectives
    except Exception as e:
        logger.error(f"Stakeholder perspective generation error: {e}")
        raise LLMAnalysisError(f"Error generating stakeholder perspectives: {str(e)}")
    
    return state