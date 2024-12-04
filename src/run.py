import dotenv
import argparse
import warnings
warnings.filterwarnings("ignore")

from src.agents.npo_agent import NPOAuditAgent
# Load environment variables
dotenv.load_dotenv()

def parse_arguments():
    """
    Parse command-line arguments for the NPO audit script.
    
    Returns:
        str: The URL to be audited
    """
    parser = argparse.ArgumentParser(description="NPO Audit Tool")
    parser.add_argument("url", help="The URL of the non-profit organization to audit")
    
    args = parser.parse_args()
    return args.url

def main():
    # Parse the URL from command-line arguments
    url = parse_arguments()
    
    # Initialize the NPO Audit Agent
    agent = NPOAuditAgent()
    
    # Run an audit on the specified URL
    audit_result = agent.run_audit(url)
    
    # Print detailed audit results
    print("Audit Completed Successfully!")
    print("\nMission Analysis:")
    print(audit_result.get('mission_analysis', 'N/A'))
    
    print("\nStakeholder Perspectives:")
    for stakeholder, perspective in audit_result.get('stakeholder_perspectives', {}).items():
        print(f"{stakeholder}: {perspective}")
    
    print("\nRecommendations:")
    for stakeholder, recs in audit_result.get('recommendations', {}).items():
        print(f"{stakeholder}:")
        for rec in recs:
            print(f"  - {rec}")
    
    print("\nAudit Score:")
    for dimension, score_info in audit_result.get('audit_score', {}).items():
        print(f"{dimension}: {score_info['score']}/10 - {score_info['explanation']}")

if __name__ == "__main__":
    main()