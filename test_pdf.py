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


#define menu itesm response schema
menu_schema={
                  "type": "object",
                  "properties": {
                    "menu_items": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "name": {
                            "type": "string",
                            "description": "The name of the menu item."
                          },
                          "description": {
                            "type": "string",
                            "description": "A brief explanation of the menu item's ingredients and style."
                          },
                          "price": {
                            "type": "number",
                            "description": "The cost of the menu item."
                          }
                        },
                        "required": [
                          "name",
                          "description",
                          "price"
                        ],
                        "additionalProperties": false
                      }
                    }
                  },
                  "required": [
                    "menu_items"
                  ],
                  "additionalProperties": false
}

def get_file_bytes(url):
    with urllib.request.urlopen(url) as response:
        return response.read()

#define the chats
chats=[]
descriptions=[]

# Chat 1: Is this a cat? (With cat image)
menu_url = "https://www.llmserver.econlabs.org/assets/menutest.pdf"
menu_bytes = get_file_bytes(menu_url)
chat_menu = Chat(responseSchema=menu_schema)
chat_menu.AddSystemMessage("You are a helpful assistant who reads restaurant menus.")
fragment_menu = MessageFragments()
fragment_menu.AddText("Extract the entrees from this PDF menu as a JSON object.")
fragment_menu.AddFile(menu_bytes)
chat_menu.AddUserMessageList(fragment_menu)
chats.append(chat_menu)
descriptions.append(f"Menu items on this menu: {menu_url}")


if __name__ == "__main__":
    asyncio.run(loop(chats,descriptions))