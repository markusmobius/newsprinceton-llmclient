from LlmClient.LlmLib import Chat, Llm
import json

truefacts=[
    "Illustra's printing business in China made record sales.",
    "Illustra's nuclear power division in Japan saw a 20% decline in sales.",
    "Illustra's appliance division in Florida introduced a successful line of washers."
]
recalled="Illustra introduced some washers"

#define the chats
chats=[]

recall_schema={
  "type": "object",
  "properties": {
    "matching_fact": {
      "type": "number"
    },
    "rating": {
      "type": "number",
      "enum": [0,1,2,3,4,5,6,7,8,9,10]
    },
    "reasoning":{
      "type": "string"
    }
  },
  "required": ["matching_fact","rating","reasoning"],
  "additionalProperties": False
}

chat = Chat(responseSchema=recall_schema) 

chat.AddSystemMessage("You are a helpful assistant.")
chat.AddUserMessage(f"A participant in an experiment attempted to recall some facts of a fictitious company that we showed to them. Here are the facts as a JSON list {json.dumps(truefacts)}. Here is what they recalled:\"{recalled}\". We ask you to match the recalled response to the best-matching fact using the index in the JSON array of facts. We also ask you to rate the answer on a scale from 0 to 10 where 0 is a very bad match and 10 is a great match. Also explain your reasoning. Provide these three outputs - the JSON index, the rating and the reasoning in a JSON array using the schema ['matching_fact':'fact_index','rating':'your_rating','reasoning':'your reasoning for the rating']")
chats.append(chat)

#execute them
llm = Llm()
responses=llm.execute_chats(chats,["example"])

for i,response in enumerate(responses):
    print(f"Task {i}")
    if response["error"]!=None:
        print("ERROR:")
        print(response["error"])
    else:
        print("RESPONSE:")
        answer= json.loads(response["answer"])  # we ask the LLM to answer in JSON
        print(answer)