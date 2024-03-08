from openai import OpenAI

def get_emb(text):
    client = OpenAI()
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

if __name__ == '__main__':
    emb = get_emb('foxy')
    print(type(emb))
    print(len(emb))
    print(emb[:5])