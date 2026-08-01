import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class BudgetConfig(BaseModel):
    low_max: int = int(os.getenv("BUDGET_LOW_MAX", 500))
    medium_max: int = int(os.getenv("BUDGET_MEDIUM_MAX", 1500))
    
    def get_budget_band(self, cost_for_two: int) -> str:
        """Categorize cost for two into budget bands."""
        if cost_for_two <= self.low_max:
            return "low"
        elif cost_for_two <= self.medium_max:
            return "medium"
        else:
            return "high"

class Config(BaseModel):
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai").lower()
    budget: BudgetConfig = BudgetConfig()

settings = Config()
