import json
from jsonschema import Draft202012Validator, SchemaError
from typing import Any
import base64
import magic
import mimetypes

class MessageFragments:
    def __init__(self):
        self.content=[]
    
    def AddText(self, text :str):
        self.content.append({"type": "input_text", "text": text})
    
    def AddImage(self, image :bytes):
        mimeType = magic.from_buffer(image, mime=True)
        self.content.append({"type": "input_image", "image_url": "data:"+mimeType+";base64," + base64.b64encode(image).decode("utf-8")})

    def AddFile(self, doc :bytes):
        mimeType = magic.from_buffer(doc, mime=True)
        self.content.append({"type": "input_file", "filename":f"file.{mimetypes.guess_extension(mimeType)}", "file_data": "data:"+mimeType+";base64," + base64.b64encode(doc).decode("utf-8")})


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


    def AddSystemMessage(self, message :str):
        self.query["messages"].append({"role": "system", "content": message})

    def AddSystemMessageList(self,fragments: MessageFragments):
        self.query["messages"].append({"role": "system", "content": fragments.content})    

    def AddAssistantMessage(self, message :str):
        self.query["messages"].append({"role": "assistant", "content": message})

    def AddAssistantMessageList(self,fragments: MessageFragments):
        self.query["messages"].append({"role": "assistant", "content": fragments.content})    

    def AddUserMessage(self, message :str):
        self.query["messages"].append({"role": "user", "content": message})

    def AddUserMessageList(self,fragments: MessageFragments):
        self.query["messages"].append({"role": "user", "content": fragments.content})    


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

