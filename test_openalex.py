import asyncio
from LlmClient.LlmLib import LlmFactory
from LlmClient.Models import Chat

async def process_chat(chat : Chat, client, name: str):
    output=await client.Ask(chat,tags=["example", name])
    print(f"--- Output for {name} ---")
    if output.error!=None:
      print("ERROR:", output.error)
    else:
      print("RESPONSE:", output.answer.ChatAnswer if output.answer else "None")
    print("\n")

async def main():
    factory=LlmFactory()
    client=await factory.create_client()
    
    prompt = "List all paper in economics on risk preferences from January 2026 in the American Economic Review."
    
    # Run WITHOUT the academic tool
    chat_without_tool = Chat()
    chat_without_tool.AddUserMessage(prompt)

    # Run WITH the academic tool
    chat_with_tool = Chat(tools=["openalex"])
    chat_with_tool.AddSystemMessage("Use the openalex tool to find the academic papers requested.")
    chat_with_tool.AddUserMessage(prompt)
    
    # Execute both sequentially
    await process_chat(chat_without_tool, client, "NO_TOOL")
    await process_chat(chat_with_tool, client, "WITH_OPENALEX")

    await client.Close()
    
if __name__ == "__main__":
    asyncio.run(main())