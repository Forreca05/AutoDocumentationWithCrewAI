from src.crew import CodeDocumentationCrew

if __name__ == "__main__":
    CodeDocumentationCrew().crew().kickoff(inputs={"url": "https://raw.githubusercontent.com/crewAIInc/crewAI/refs/heads/main/src/crewai/agent.py"})
