from typing import Dict, Any
import logging

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

from src.utils.exceptions import LLMAnalysisError

def recommendation_generator(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate actionable recommendations based on stakeholder perspectives
    
    :param state: Current state of the audit process
    :param config: Configuration dictionary
    :return: Updated state with recommendations
    """
    logger = logging.getLogger(__name__)
    logger.info("Generating recommendations")
    
    if not state.get('stakeholder_perspectives'):
        logger.warning("No stakeholder perspectives available")
        state['recommendations'] = {"Error": ["No stakeholder perspectives to generate recommendations from"]}
        return state
    
    try:
        llm = ChatOpenAI(
            temperature=0.2,
            base_url=config.get('configurable', {}).get('local_llm_base_url', "http://localhost:1234/v1"),
            api_key="not-needed",
            model_name="local_model"
        )
        
        recommendation_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
            You are a strategic nonprofit consultant. 
            Generate targeted, actionable recommendations addressing 
            the perspectives of key stakeholders.
            
            For each stakeholder perspective:
            - Identify potential improvement areas
            - Suggest concrete, implementable strategies
            - Align recommendations with the organization's mission
            """),
            HumanMessage(content=f"""
            Mission Analysis: {state.get('mission_analysis', 'N/A')}
            
            Stakeholder Perspectives: 
            {chr(10).join(f"{k}: {v}" for k, v in state.get('stakeholder_perspectives', {}).items())}
            """)
        ])
        
        response = llm(recommendation_prompt.format_messages())
        
        # More robust parsing of recommendations
        recommendations = {}
        current_stakeholder = None
        for line in response.content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            if ':' in line and not line.startswith(' '):
                current_stakeholder = line.split(':')[0].strip()
                recommendations[current_stakeholder] = []
            elif current_stakeholder and line:
                recommendations[current_stakeholder].append(line)
        
        state['recommendations'] = recommendations
    except Exception as e:
        logger.error(f"Recommendation generation error: {e}")
        raise LLMAnalysisError(f"Error generating recommendations: {str(e)}")
    
    return state