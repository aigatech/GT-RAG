from openai import OpenAI
from .config import settings

client = OpenAI(
    api_key=settings.NIM_API_KEY,
    base_url="https://integrate.api.nvidia.com/v1"
)

def generate_embedding(text):
    response = client.embeddings.create(
        input=[text],
        model="nvidia/nv-embed-v1",
        encoding_format="float",
        extra_body={"input_type": "document", "truncate": "NONE"}
    )
    return response.data[0].embedding
