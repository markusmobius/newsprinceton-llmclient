import asyncio
import urllib.request
from LlmClient.LlmLib import LlmFactory
from LlmClient.Models import Chat, MessageFragments

async def process_chat(chat : Chat, client):
    output=await client.Ask(chat,tags=["example"])
    await client.Close()
    return output 

async def loop(chats: list[Chat],descriptions: list[str]):
    factory=LlmFactory()
    tasks = [process_chat(chat,await factory.create_client()) for chat in chats]
    outputs = await asyncio.gather(*tasks)
    for i,output in enumerate(outputs):
      print(f"Task {i}")
      print(f"description: {descriptions[i]}")
      if output.error!=None:
        print("ERROR:")    
        print(output.error)
      else:
        print("RESPONSE:")    
        print(output.answer)
      print("________________________________________________________")
      print("")


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

def get_image_bytes(url):
    with urllib.request.urlopen(url) as response:
        return response.read()

#define the chats
chats=[]
descriptions=[]

# Chat 1: Is this a cat? (With cat image)
cat_url = "https://www.llmserver.econlabs.org/assets/cat.png"
cat_image_bytes = get_image_bytes(cat_url)
fragment_cat = MessageFragments()
fragment_cat.AddText("Is this a cat?")
fragment_cat.AddImage(cat_image_bytes, "image/png")
chat_cat = Chat(responseSchema=yesno_schema)
chat_cat.AddSystemMessage("You are a helpful assistant capable of  image recognition.")
chat_cat.AddUserMessageList(fragment_cat)
chats.append(chat_cat)
descriptions.append(f"Is there a cat in this cat image: {cat_url}")

# Chat 2: Is this a cat? (With not-a-cat image)
cat_url = "https://www.llmserver.econlabs.org/assets/notacat.png"
cat_image_bytes = get_image_bytes(cat_url)
fragment_cat = MessageFragments()
fragment_cat.AddText("Is this a cat?")
fragment_cat.AddImage(cat_image_bytes, "image/png")
chat_cat = Chat(responseSchema=yesno_schema)
chat_cat.AddSystemMessage("You are a helpful assistant capable of  image recognition.")
chat_cat.AddUserMessageList(fragment_cat)
chats.append(chat_cat)
descriptions.append(f"Is there a cat in this not-a-cat image: {cat_url}")


if __name__ == "__main__":
    asyncio.run(loop(chats,descriptions))