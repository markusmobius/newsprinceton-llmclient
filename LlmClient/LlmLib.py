import asyncio
import aiohttp
import requests
import json
from jsonschema import Draft202012Validator, SchemaError
import os
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

    def getRaw(self):
        """Returns the JSON representation of the query."""
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


    def getRaw(self):
        """Returns the JSON representation of the embedding."""
        return self.embedding

    def getJSON(self):
        """Returns the JSON string representation of the embedding."""
        return json.dumps(self.embedding, indent=4)


class Dto:
    def __init__(self, chat: Chat, tags: list[str], cache_only: bool = False):
         self.dto={
            "chat" : chat.getRaw(),
            "tags" : tags,
            "cache_only": cache_only
         }

    def getJSON(self):
        """Returns the JSON string representation of the dto object."""
        return json.dumps(self.dto, indent=4)

class EmbeddingDto:
    def __init__(self, embedding : Embedding, tags: list[str], cache_only: bool = False):
         self.dto={
            "embed" : embedding.getRaw(),
            "tags" : tags,
            "cache_only": cache_only
         }

    def getJSON(self):
        """Returns the JSON string representation of the dto object."""
        return json.dumps(self.dto, indent=4)


class DtoSet:
    def __init__(self, chats: list[Chat], tags: list[str]):
        self.dto={
            "chats" : [],
            "tags" : tags
        }
        for chat in chats:
            self.dto["chats"].append(chat.getRaw())

    def getJSON(self):
        """Returns the JSON string representation of the dto object."""
        return json.dumps(self.dto, indent=4)


class Llm:

    def __init__(self, batch_size: int = 10):
        self.api_endpoint = os.environ["llmserverurl"]+"/llm/run"
        self.api_endpointbackground = os.environ["llmserverurl"]+"/llm/runbackground"
        self.batch_size = batch_size
        self.total_tasks = 0
        self.completed_tasks = 0
        self.errors = 0
        self.results = []

    async def _send_task_to_api(self, session, task_data : Dto):
        headers = {"Authorization": f"Bearer {os.environ['llmcode']}", "Content-Type": "application/json"}
        try:
            async with session.post(self.api_endpoint,
                                    data=task_data.getJSON(),
                                    headers=headers) as response:
                response.raise_for_status()
                js = await response.json()
                if js.get("error"):
                    self.errors += 1
                else:
                    self.completed_tasks += 1
                return js
        except aiohttp.ClientError as e:
            self.errors += 1
            return {"answer": None, "error": str(e)}

    async def execute_tasks_async(self, tasks: list):
        """
        Launch all tasks immediately but never allow more than
        self.batch_size concurrent HTTP requests.
        """
        self.total_tasks = len(tasks)
        self.completed_tasks = 0
        self.errors = 0
        self.results = [None] * self.total_tasks

        sem = asyncio.Semaphore(self.batch_size)

        async def worker(idx, task_data, session):
            async with sem:
                result = await self._send_task_to_api(session, task_data)
                self.results[idx] = result
                print(
                    f"Status: {self.completed_tasks}/{self.total_tasks} tasks done "
                    f"[errors: {self.errors}].",
                    end="\r",
                    flush=True,
                )

        async with aiohttp.ClientSession() as session:
            # create and schedule all tasks at once
            coros = [worker(i, t, session) for i, t in enumerate(tasks)]
            await asyncio.gather(*coros)

        print()  # move to a new line after progress output
        return self.results

    def execute_chats(self, chats: list[Chat], tags: list[str], cache_only: bool = False):
        tasks : list[Dto] = []
        for chat in chats:
            dto = Dto(chat, tags, cache_only)
            tasks.append(dto)

        return asyncio.run(self.execute_tasks_async(tasks))

    def execute_embeddings(self, embeddings: list[Embedding], tags: list[str], cache_only: bool = False):
        tasks : list[EmbeddingDto] = []
        for embed in embeddings:
            dto = EmbeddingDto(embed, tags, cache_only)
            tasks.append(dto)

        return asyncio.run(self.execute_tasks_async(tasks))


    def execute_chats_background(self, chats: list[Chat], tags: list[str]):
        headers = {"Authorization": f"Bearer {os.environ['llmcode']}", "Content-Type": "application/json"}
        payload = DtoSet(chats, tags).getJSON()
        try:
            response = requests.post(self.api_endpointbackground, data=payload, headers=headers)
        except:
            print("error submitting the background job")

