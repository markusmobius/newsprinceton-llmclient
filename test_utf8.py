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
        print(output.answer.ChatAnswer)
      print("________________________________________________________")
      print("")



#define the chats
#response for this request is just a text
chats=[]
chat = Chat(responseSchema=None) 
chat.AddSystemMessage("You are a helpful assistant.")
chat.AddUserMessage("How do you call shoelaces in Hungarian?")
chats.append(chat)

chat = Chat(responseSchema=None) 
chat.AddSystemMessage("You are a helpful assistant.")
chat.AddUserMessage("How do Austrians call their country?")
chats.append(chat)

asyncio.run(loop(chats))