try:
    from agents.marketing_agent import MarketingAgent
    from agents.finance_agent import FinanceAgent
except ImportError:
    from marketing_agent import MarketingAgent
    from finance_agent import FinanceAgent

class Orchestrator:
    def __init__(self):
        self.marketing_agent = MarketingAgent()
        self.finance_agent = FinanceAgent()

    def handle_request(self, request_type, data):
        """
        Routes the task to the appropriate agent.
        """
        print(f"[Orchestrator] Routing task: {request_type}")
        
        if request_type == "marketing":
            return self.marketing_agent.run(data)
        elif request_type == "finance":
            return self.finance_agent.analyze(data)
        
        return {"error": "Unknown request type"}

if __name__ == "__main__":
    # Test run
    orch = Orchestrator()
    print(orch.handle_request("marketing", "Hackathon Launch"))
