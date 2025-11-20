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
chat.AddUserMessage("What's the best way to train a swan?")
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
chat.AddUserMessage("What is 2+2? Return as JSON.")
chats.append(chat)

chat = Chat(responseSchema=numeric_schema) 
chat.AddSystemMessage("You are a helpful assistant.")
chat.AddUserMessage("What is the square root of 121? Return as JSON.")
chats.append(chat)

chat = Chat(responseSchema=numeric_schema) 
chat.AddSystemMessage("You are a helpful assistant.")
chat.AddUserMessage("How many letters are in the word 'Rhythm'? Return as JSON.")
chats.append(chat)

chat = Chat(responseSchema=numeric_schema) 
chat.AddSystemMessage("You are a helpful assistant.")
chat.AddUserMessage("When was Barack Obama born? Return as JSON.")
chats.append(chat)

#summarize scheme
string_schema={
    "type": "object",
    "properties": {
        "answer": {
          "type": "string"
        }
    },
    "required": ["answer"],
    "additionalProperties": False
}
chat = Chat(responseSchema=string_schema) 
chat.AddSystemMessage("You are a helpful assistant.")
chat.AddUserMessage("Summarize this text in one sentence of not more than 15 words: Jimmy Kimmel broke his silence on Tuesday night in an emotional return to ABC’s airwaves, addressing the controversy that temporarily sidelined his late-night show amid a still-swirling storm of political and corporate standoffs. 'This show is not important,' Mr. Kimmel said in his opening monologue. 'What’s important is that we get to live in a country that allows us to have a show like this.' ABC and Disney executives pulled 'Jimmy Kimmel Live!' off the air last week after an uproar over the host's comments about the suspected shooter of right-wing activist Charlie Kirk. On Tuesday night, Mr. Kimmel, choking up, said it 'was never my intention' to make light of the murder of a young man.? Return as JSON.")
chats.append(chat)

chat = Chat(responseSchema=string_schema) 
chat.AddSystemMessage("You are a helpful assistant.")
chat.AddUserMessage("Summarize this text: Abstractive summarization methods generate new text that did not exist in the original text. This has been applied mainly for text. Abstractive methods build an internal semantic representation of the original content (often called a language model), and then use this representation to create a summary that is closer to what a human might express. Abstraction may transform the extracted content by paraphrasing sections of the source document, to condense a text more strongly than extraction. Such transformation, however, is computationally much more challenging than extraction, involving both natural language processing and often a deep understanding of the domain of the original text in cases where the original document relates to a special field of knowledge. 'Paraphrasing' is even more difficult to apply to images and videos, which is why most summarization systems are extractive. Return as JSON.")
chats.append(chat)

chat = Chat(responseSchema=string_schema)
chat.AddSystemMessage("You are a helpful assistant.")
chat.AddUserMessage("Who is older - god or the universe? Return as JSON.")
chats.append(chat)

chat = Chat(responseSchema=string_schema) 
chat.AddSystemMessage("You are a helpful assistant.")
chat.AddUserMessage("Who invented the tetanus vaccine some time ago? Return as JSON.")
chats.append(chat)

asyncio.run(loop(chats))

