import json
from jsonschema import Draft202012Validator, SchemaError
from typing import Any

class Chat:
    def __init__(self, responseSchema: Any, model : str = "gpt-5-mini_2025-08-07"):
        #check that we have valid JSON schema
        if responseSchema!=None:
            try:
                Draft202012Validator.check_schema(responseSchema)
            except SchemaError as e:
                raise Exception(f"JSON schema is invalid: {e.message}")
        self.query = {
                "model": model,
                "messages": [],
                "ResponseSchema": json.dumps(responseSchema)
            }


    def AddSystemMessage(self, message):
        self.query["messages"].append({"role": "system", "content": message})

    def AddAssistantMessage(self, message):
        self.query["messages"].append({"role": "assistant", "content": message})

    def AddUserMessage(self, message):
        self.query["messages"].append({"role": "user", "content": message})

    def to_dict(self):
        return self.query
    
    def getJSON(self):
        """Returns the JSON string representation of the query."""
        return json.dumps(self.query, indent=4)


class Embedding:
    def __init__(self, text: str, model : str = "text-embedding-3-large_1"):
        self.embedding = {
                "model": model,
                "text" : text
            }


    def to_dict(self):
        """Returns the JSON representation of the embedding."""
        return self.embedding

    def getJSON(self):
        """Returns the JSON string representation of the embedding."""
        return json.dumps(self.embedding, indent=4)

