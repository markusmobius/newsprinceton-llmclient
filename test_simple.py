import asyncio
from  LlmClient.LlmLib import Embedding, LlmFactory
import json

async def main():
    factory=LlmFactory()
    client=await factory.create_client()
    output=await client.Embed(Embedding("Hello lila super wunderland"),tags=["example"])
    print(output)
    
if __name__ == "__main__":
    asyncio.run(main())
