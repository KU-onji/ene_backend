import os

from openai import AsyncOpenAI
from tenacity import RetryError, retry, stop_after_attempt, wait_fixed


async def create_asyncClient() -> AsyncOpenAI:
    client = await AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY_ENE"), timeout=15, max_retries=3)
    return client


def create_request(prompt):
    return {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant and have a plenty of knowledge about informatics.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
    }


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def call_gpt_async(client: AsyncOpenAI, prompt: str) -> tuple[str, int]:
    try:
        res = await client.chat.completions.create(**create_request(prompt))
        return res.choices[0].message.content
    except RetryError:
        return "ごめん、今忙しいからちょっと待ってね。"
