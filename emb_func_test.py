import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import torch

client = chromadb.PersistentClient(path="C:/Users/axnm/PycharmProjects/colors_emb/chroma_shit")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key="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",
                model_name="text-embedding-ada-002"
            )
collection = client.get_or_create_collection(name="colors_of_words", metadata={'hnsw:space':'ip'}, embedding_function=openai_ef)
collection = client.get_collection(name="colors_of_words", embedding_function=openai_ef)

# embedding from emb function:
banana_emb = openai_ef('banana')
banana_from_func = torch.tensor(data=banana_emb[0])
print(banana_from_func[:5])

cg = collection.get(
    ids=["3"],
    include=['documents','embeddings']
)
print(cg)
banana_from_base = torch.tensor(data=cg['embeddings'][0])
print(banana_from_base[:5])

ts = torch.sum( (banana_from_base - banana_from_func)**2 )
print(ts)