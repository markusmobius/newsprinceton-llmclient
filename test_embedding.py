import asyncio
from  LlmClient.LlmLib import Embedding, LlmFactory

async def main():
    factory=LlmFactory()
    client=await factory.create_client()
    #embedding
    texts=["Hello lila super super super wunderland story","JFK was the much older brother of RFK (Robert) and the President."]
    for text in texts:
        output=await client.Embed(Embedding(text),tags=["example"])
        if output.error!=None:
            print("ERROR:")    
            print(output.error)
        else:
            print("RESPONSE:")    
            print(len(output.answer.Embedding))
        print(output.answer.RuntimeData)
    await client.Close()
    
if __name__ == "__main__":
    asyncio.run(main())
