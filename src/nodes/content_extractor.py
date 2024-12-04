from typing import Dict, Any
import logging

from src.utils.exceptions import ContentExtractionError

def content_extractor(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract content from website or Facebook page
    
    :param state: Current state of the audit process
    :param config: Configuration dictionary
    :return: Updated state with extracted content
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Extracting content from {state['url']} on {state['platform']}")
    
    try:
        if state['platform'] == 'website':
            from firecrawl import FirecrawlApp
            
            api_key = config.get('configurable', {}).get('firecrawl_api_key')
            if not api_key:
                raise ContentExtractionError("Firecrawl API key is required")
            
            app = FirecrawlApp(api_key=api_key)
            scrape_result = app.scrape_url(state['url'], params={'formats': ['markdown']})
            
            state['raw_content'] = scrape_result.get('markdown', '')
        
        elif state['platform'] == 'facebook':
            # TODO: Implement Facebook page scraping
            state['raw_content'] = "Facebook scraping not yet implemented"
    except Exception as e:
        logger.error(f"Content extraction error: {e}")
        raise ContentExtractionError(f"Error extracting content: {str(e)}")
    
    return state