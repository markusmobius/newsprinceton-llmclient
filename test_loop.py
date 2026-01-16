import asyncio
from  LlmClient.LlmLib import LlmFactory
from LlmClient.Models import Chat


async def loop(chats: list[Chat]):
    factory=LlmFactory()
    client=await factory.create_client()
    for chat in chats:
      output=await client.Ask(chat,tags=["example"])
      print("chat:")
      print(chat.getJSON())
      if output.error!=None:
        print("ERROR:")    
        print(output.error)
      else:
        print("RESPONSE:")    
        print(output.answer)
      print("________________________________________________________")
      print("")
    await client.Close()


#define the chats
#response for this request is just a text
chats=[]

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
start=200
for i in range(10):
  chat = Chat(responseSchema=yesno_schema) 
  chat.AddSystemMessage("You are a helpful assistant.")
  chat.AddUserMessage(f"Is the square root of {start+i} a rational number? Return as JSON.")
  chats.append(chat)

asyncio.run(loop(chats))

