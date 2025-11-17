from  LlmClient.LlmLib import Embedding, LlmFactory
import json

#define the embedding
embeddings = []
embeddings.append(Embedding("Hello lila super wunderland"))
embeddings.append(Embedding("JFK was the much older brother of RFK (Robert) and the President."))

factory=LlmFactory()
client=await factory.create_client()
llm =  Llm()
responses=llm.execute_embeddings(embeddings=embeddings,tags=["example"])

for i,response in enumerate(responses):
    print(f"Task {i}")
    print("embedding:")
    print(embeddings[i].getJSON())
    if response["error"]!=None:
        print("ERROR:")    
        print(response["error"])
    else:
        print("RESPONSE:")    
        print(len(response["answer"]))
        print(f"Usage: {json.dumps(response["usage"])}")
    print("________________________________________________________")
    print("")

