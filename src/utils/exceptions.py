class NPOAuditError(Exception):
    """Base exception for NPO Audit errors"""
    pass

class ContentExtractionError(NPOAuditError):
    """Raised when content extraction fails"""
    pass

class LLMAnalysisError(NPOAuditError):
    """Raised when LLM-based analysis encounters an error"""
    pass