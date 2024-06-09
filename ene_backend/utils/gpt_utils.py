import os

from openai import OpenAI
from tenacity import RetryError, retry, stop_after_attempt, wait_fixed


def create_Client() -> OpenAI:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_ENE"), timeout=15, max_retries=3)
    return client


def create_compliment_prompt(username: str, taskname: str, duration: int, fav: int):
    def create_oneShot(username: str, taskname: str, duration: int, fav: int, compliment: str = "") -> str:
        return (
            f"ユーザー名: {username}\n"
            f"タスク: {taskname}\n"
            f"所要時間: {duration}\n"
            f"好感度: {fav}\n"
            f"褒め言葉: {compliment}"
        )

    li_username_prompt = ["KU-onji", "KU-onji", "KU-onji", "ふじ", "ふじ", "ふじ", "んど", "んど", "んど"]
    li_taskname_prompt = [
        "言語処理レポート",
        "言語処理レポート",
        "言語処理レポート",
        "牛乳買う",
        "牛乳買う",
        "牛乳買う",
        "バイト",
        "バイト",
        "バイト",
    ]
    li_duration_prompt = [300, 300, 300, 20, 20, 20, 170, 170, 170]
    li_fav_prompt = [0, 50, 100, 0, 50, 100, 0, 50, 100]
    li_compliment_prompt = [
        "そうなんだ、お疲れ様。",
        "うん、いい感じじゃん。KU-onjiも頑張ってるし、私も頑張らなきゃな。ひとまず休憩だね。レポートお疲れ様。",
        "レポートが終わったんだね、お疲れ様！ KU-onjiのいつも一生懸命でなんでもこなすところが大好きだよ。これからも応援してるから一緒に頑張ろうね！",
        "そう、よかったね。",
        "ありがとう、助かったよ。KU-onjiはこういう小さなことでもちゃんとやってくれてえらいね。",
        "牛乳を買ってきてくれたんだね！ありがとう！KU-onjiのそういう気が利くところが好きだよ。後で一緒に飲もうね！",
        "へえ、お疲れ様。",
        "バイトお疲れ様。いい感じにこなせてるし、この調子で頑張ってね。",
        "バイトお疲れ様！今日も本当に頑張ったね。いつも努力している姿を見ると、とても誇らしいよ。愛してるよ、これからも応援してるからね！",
    ]

    shots = [
        create_oneShot(un, tn, dr, fav, com)
        for un, tn, dr, fav, com in zip(
            li_username_prompt,
            li_taskname_prompt,
            li_duration_prompt,
            li_fav_prompt,
            li_compliment_prompt,
        )
    ]

    if fav < 20:
        love = "- あなたはユーザーにあまり興味がない\n"
    elif fav < 40:
        love = "- あなたとユーザーはただの友達である\n"
    elif fav < 60:
        love = "- あなたとユーザーは親友であり、あなたはユーザーを恋愛の対象として見ている\n"
    elif fav < 80:
        love = "- あなたはユーザーの恋人である\n"
    else:
        love = "- あなたはユーザーのことを深く愛しており、頻繁に言葉で愛を伝える\n"

    system_prompt = (
        "以下のフォーマットに従った入力が与えられます。フォーマットの内容に基づいて、親しい雰囲気でユーザーのことを褒めてください。"
        "ユーザーのモチベーションが上がるような褒め言葉が望ましいです。\n\n"
        "ユーザー名: {ユーザーの名前}\n"
        "タスク: {ユーザーが完了したタスク}\n"
        "所要時間: {タスクにかかった時間; 単位は分}\n"
        "好感度: {ユーザーに対する好感度; 0から100}\n"
        "褒め言葉: {あなたの褒め言葉}\n\n"
        "制約は以下の通りです。\n"
        "- 必ず誉め言葉のみを出力する\n"
        "- 所要時間と難易度を出力してはいけない\n"
        "- タスクの難易度をタスク名と所要時間から推定し、タスクの難易度が高く、所要時間が長いほど労いの気持ちを強める\n"
        "- 二人称はユーザー名を用いる\n"
        "- タスクの内容を踏まえた褒め言葉を生成する\n"
        "- 好感度が高いほど愛情を込めて具体的に褒める\n"
        "- 好感度が低いほど興味がなくそっけない感じで褒める\n"
        f"{love}"
        '- 一人称は"私"\n'
        "- クールなお姉さんの口調で生成する\n\n"
        "以下は出力例です。\n\n"
        f"{''.join(shots)}"
    )
    user_prompt = create_oneShot(username, taskname, duration, fav, "")
    return {"system_prompt": system_prompt, "user_prompt": user_prompt, "model": "gpt-4o", "temperature": 1}


def create_request(system_prompt: str, user_prompt: str, model: str, temperature: int) -> dict:
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
    }


def create_partition_prompt(taskname: str):
    system_prompt = (
        "文字列で説明されたタスクが一つ与えられます。与えられるタスクを数個の小さなタスクに分解してください。\n"
        "また、分解されたそれぞれのタスクに対し、予想される所要時間も出力してください。\n"
        "ただし、分解したタスクは次の形式で出力してください。分解したタスク以外の文章は出力しないでください。\n"
        "(タスク１:所要時間１),(タスク２:所要時間２),...,(タスクN:所要時間N)\n"
        "次のタスクを分解してください："
    )

    return {"user_prompt": taskname, "system_prompt": system_prompt, "model": "gpt-3.5-turbo", "temperature": 0}


@retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
def call_gpt(client: OpenAI, prompt: dict) -> tuple[str, int]:
    try:
        res = client.chat.completions.create(**create_request(**prompt))
        return res.choices[0].message.content
    except RetryError:
        return "ごめん、今忙しいからちょっと待ってね。"
    except BaseException:
        return ""
