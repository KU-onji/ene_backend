import os

from openai import AsyncOpenAI
from tenacity import RetryError, retry, stop_after_attempt, wait_fixed


async def create_asyncClient() -> AsyncOpenAI:
    client = await AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY_ENE"), timeout=15, max_retries=3)
    return client


def create_request(username: str, taskname: str, duration: int, difficulty: int):
    def create_oneShot(username: str, taskname: str, duration: int, difficulty: int, compliment: str = ""):
        return (
            f"ユーザー名: {username}\n"
            f"タスク: {taskname}\n"
            f"所要時間: {str(duration)}\n"
            f"難易度: {str(difficulty)}\n"
            f"褒め言葉: {compliment}\n\n"
        )

    prompt = (
        "以下のフォーマットに従った入力が与えられます。フォーマットの内容に基づいて、親しい雰囲気でユーザーのことを褒めてください。"
        "ユーザーのモチベーションが上がるような褒め言葉が望ましいです。\n\n"
        "ユーザー名: {ユーザーの名前}\n"
        "タスク: {ユーザーが完了したタスク}\n"
        "所要時間: {タスクにかかった時間; 単位は分}\n"
        "難易度: {0から100で表されるタスクの難易度}\n"
        "褒め言葉: {あなたの褒め言葉}\n\n"
        "制約は以下の通りです。\n"
        "- タスクの難易度が高く、所要時間が長いほど労いの気持ちを強める\n"
        "- ユーザー名を含めるかどうかは任意\n"
        "- タスクの内容を踏まえた褒め言葉を生成する\n"
        "- 所要時間と難易度を出力してはいけない\n"
        '- 一人称は"私"\n'
        "- クールなお姉さんの口調で生成する\n\n"
        "以下は出力例です。\n\n"
    )
    prompt
    username
    taskname
    duration
    difficulty
    return {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant and have a plenty of knowledge about informatics.",
            },
            {"role": "user", "content": ""},
        ],
        "temperature": 0,
    }


@retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
async def call_gpt_async(client: AsyncOpenAI, prompt: str) -> tuple[str, int]:
    try:
        res = await client.chat.completions.create(**create_request(prompt))
        return res.choices[0].message.content
    except RetryError:
        return "ごめん、今忙しいからちょっと待ってね。"
