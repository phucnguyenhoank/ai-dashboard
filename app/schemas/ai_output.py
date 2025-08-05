from pydantic import BaseModel

class AIOutput(BaseModel):
    model_name: str  # Name of the AI model (e.g., "gpt-3")
    output: str      # Output from the AI model

class AIOutputCreate(AIOutput):
    id: int          # Unique ID for the output (e.g., from a database)