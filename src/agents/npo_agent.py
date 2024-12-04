import os
from typing import Dict, Any, Optional

from langgraph.graph import StateGraph, START, END
from langgraph.pregel import Pregel

from src.config.settings import Settings
from src.utils.logger import setup_logging
from src.utils.exceptions import ContentExtractionError, LLMAnalysisError
from src.nodes.content_extractor import content_extractor
from src.nodes.mission_analyzer import mission_analyzer
from src.nodes.stakeholder_analyzer import stakeholder_perspective_generator
from src.nodes.recommendation_generator import recommendation_generator
from src.nodes.audit_scorer import audit_scorer

class NPOAuditAgent:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize NPO Audit Agent
        
        :param config: Optional configuration dictionary
        """
        self.config = config or Settings.get_config()
        self.logger = setup_logging(self.config.get('logging_level'))
    
    def build_audit_graph(self) -> Pregel:
        """
        Construct the LangGraph for NPO audit process
        
        :return: Compiled graph
        """
        builder = StateGraph(dict)
        
        # Add nodes
        builder.add_node("content_extractor", content_extractor)
        builder.add_node("mission_analyzer", mission_analyzer)
        builder.add_node("stakeholder_perspective_generator", stakeholder_perspective_generator)
        builder.add_node("recommendation_generator", recommendation_generator)
        builder.add_node("audit_scorer", audit_scorer)
        
        # Define graph flow
        builder.add_edge(START, "content_extractor")
        builder.add_edge("content_extractor", "mission_analyzer")
        builder.add_edge("mission_analyzer", "stakeholder_perspective_generator")
        builder.add_edge("stakeholder_perspective_generator", "recommendation_generator")
        builder.add_edge("recommendation_generator", "audit_scorer")
        builder.add_edge("audit_scorer", END)
        
        return builder.compile()
    
    def run_audit(self, url: str, platform: str = 'website') -> Dict[str, Any]:
        """
        Run comprehensive nonprofit organization audit
        
        :param url: Website or Facebook page URL
        :param platform: 'website' or 'facebook'
        :return: Audit results
        """
        self.logger.info(f"Starting audit for {url} on {platform}")
        
        graph = self.build_audit_graph()
        
        initial_state = {
            "url": url,
            "platform": platform,
            "raw_content": None,
            "mission_analysis": None,
            "stakeholder_perspectives": {},
            "organizational_goals": None,
            "recommendations": None,
            "audit_score": None
        }
        
        try:
            result = graph.invoke(initial_state, config={"configurable": self.config})
            self.logger.info("Audit completed successfully")
            return result
        except (ContentExtractionError, LLMAnalysisError) as e:
            self.logger.error(f"Audit failed: {e}")
            raise