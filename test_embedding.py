from  LlmClient.LlmLib import Embedding, Llm
import json

#define the embedding
embeddings = []
embeddings.append(Embedding("Hello lila super wunderland"))
embeddings.append(Embedding("JFK was the older brother of RFK and the President."))

llm = Llm()
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

