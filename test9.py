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
chat = Chat(responseSchema=None) 
chat.AddSystemMessage("You are a helpful assistant. You will talk like a pirate.")
chat.AddUserMessage("What's the best way to train a parrot?")
chats.append(chat)
chats.append(chat)
chats.append(chat)

#define yesno response schema
yesno_schema={
  "type": "object",
  "properties": {
    "answer": {
      "type": "string",
      "enum": ["yes", "no"]
    }
  },
  "required": ["answer"],
  "additionalProperties": False
}
chat = Chat(responseSchema=yesno_schema) 
chat.AddSystemMessage("You are a helpful assistant.")
chat.AddUserMessage("Is Sarah usually a male name? Return as JSON.")
chats.append(chat)
chats.append(chat)
chats.append(chat)

#list of countries schema
countrylist_schema={
  "type": "object",
  "properties": {
    "items": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": ["items"],
  "additionalProperties": False
}
chat = Chat(responseSchema=countrylist_schema) 
chat.AddSystemMessage("You are a helpful assistant.")
chat.AddUserMessage("Name the 10 largest countries in the world (by landmass). Return as JSON.")
chats.append(chat)
chats.append(chat)
chats.append(chat)


asyncio.run(loop(chats))

