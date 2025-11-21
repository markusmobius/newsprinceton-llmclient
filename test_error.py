import asyncio
from  LlmClient.LlmLib import LlmFactory
from LlmClient.Models import Chat
 
async def process_chat(chat : Chat, client):
    output=await client.Ask(chat,tags=["example"])
    await client.Close()
    return output
 
async def loop(chats: list[Chat]):
    factory=LlmFactory()
    tasks = [process_chat(chat,await factory.create_client()) for chat in chats]
    outputs = await asyncio.gather(*tasks)
    for i,output in enumerate(outputs):
      print(f"Task {i}")
      print("chat:")
      print(chats[i].getJSON())
      if output.error!=None:
        print("ERROR:")    
        print(output.error)
      else:
        print("RESPONSE:")    
        print(output.answer)
      print("________________________________________________________")
      print("")
 
 
 
#define the chats
#response for this request is just a text
chats=[]
for i in range(1):
 
  #simple numeric answer
  numeric_schema={
    "type": "object",
    "properties": {
        "answer": {
          "type": "number",
          "description": "The numerical answer to the question."
        }
    },
    "required": ["answer"],
    "additionalProperties": False
  }
  chat = Chat(responseSchema=numeric_schema)
  chat.AddSystemMessage("You are a helpful assistant.")
  message = f"What is {i}+2? Return as JSON." + " "*17000
  chat.AddUserMessage(message)
  chats.append(chat)
 
asyncio.run(loop(chats))
 