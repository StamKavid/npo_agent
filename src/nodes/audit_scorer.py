from typing import Dict, Any
import logging

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

from src.utils.exceptions import LLMAnalysisError

def audit_scorer(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Score the comprehensiveness and potential impact of the audit
    
    :param state: Current state of the audit process
    :param config: Configuration dictionary
    :return: Updated state with audit score
    """
    logger = logging.getLogger(__name__)
    logger.info("Scoring audit report")
    
    if not state.get('recommendations'):
        logger.warning("No recommendations available for scoring")
        state['audit_score'] = {"Error": {"score": 0, "explanation": "No recommendations to score"}}
        return state
    
    try:
        llm = ChatOpenAI(
            temperature=0.2,
            base_url=config.get('configurable', {}).get('local_llm_base_url', "http://localhost:1234/v1"),
            api_key="not-needed",
            model_name="local_model"
        )
        
        scoring_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
            Evaluate the nonprofit audit report across these dimensions:
            
            1. Comprehensiveness (How thoroughly the report covers organizational aspects)
            2. Actionability (Practicality of recommendations)
            3. Strategic Alignment (How well recommendations match the mission)
            4. Potential Impact (Likelihood of recommendations driving positive change)
            
            Provide a score from 1-10 for each dimension, with a brief justification.
            """),
            HumanMessage(content=f"""
            Mission Analysis: {state.get('mission_analysis', 'N/A')}
            
            Recommendations: 
            {chr(10).join(f"{k}: {chr(10).join(v)}" for k, v in state.get('recommendations', {}).items())}
            """)
        ])
        
        response = llm.invoke(scoring_prompt.format_messages())
        
        # More robust parsing of scoring results
        audit_score = {}
        for line in response.content.split('\n'):
            if ':' in line:
                dimension, score_info = line.split(':', 1)
                try:
                    score, explanation = score_info.split('(', 1)
                    audit_score[dimension.strip()] = {
                        'score': int(score.strip()),
                        'explanation': explanation.strip().rstrip(')')
                    }
                except ValueError:
                    # Fallback if parsing fails
                    audit_score[dimension.strip()] = {
                        'score': 0,
                        'explanation': 'Unable to parse score'
                    }
        
        state['audit_score'] = audit_score
    except Exception as e:
        logger.error(f"Audit scoring error: {e}")
        raise LLMAnalysisError(f"Error scoring audit: {str(e)}")
    
    return state