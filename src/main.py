#!/usr/bin/env python3
"""
Meeting Minutes AI
自動會議記錄工具 - Whisper 轉錄 + Claude 整理
"""

import os
import sys
import whisper
import anthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

PROMPT_TEMPLATE = """你是一位政府機關的專業會議記錄助手。請根據以下資訊，整理出一份正式的會議記錄。

【基本資料】
{meeting_info}

【逐字稿】
{transcript}

---

請依照以下格式輸出會議記錄：

一、會議名稱：（從基本資料填入）
二、會議主席：（從基本資料填入）
三、會議出席人員：（從基本資料填入）
四、本署出席人員：（從基本資料填入）
五、重點說明：
（根據逐字稿，以2至4句話摘要本次會議的核心討論事項與背景說明。文字精簡，不重複結論內容。）
六、意見整理：（僅在逐字稿中有明確的與會者意見交流、討論或爭議時才列出此段；若無實質意見交流，請直接省略此項，不要留空白標題）
（條列各方主要意見，每條以「（一）（二）...」編號）
七、會議結論與主席裁示：
（一）...
（二）...
（條列主席的決定與指示，每條以「（一）（二）...」編號，用詞正式，以「請」字開頭帶出執行要求）
八、擬辦：（以一段文字說明後續執行方向，開頭用「本案將依主席裁示辦理」，並說明具體行動）

注意事項：
- 文字風格參照政府公文，正式、精簡、不口語
- 不推論、不補寫、不升格任何未在逐字稿中出現的內容
- 人名、單位名稱、職稱以基本資料為準，不自行更改
"""

def transcribe_audio(audio_path: str, model_size: str = "base") -> str:
    """使用 Whisper 將音檔轉為文字"""
    print(f"📢 載入 Whisper 模型（{model_size}）...")
    model = whisper.load_model(model_size)
    
    print(f"🎙️ 開始轉錄：{audio_path}")
    result = model.transcribe(audio_path, language="zh")
    
    return result["text"]

def generate_minutes(transcript: str, meeting_info: str = "") -> str:
    """使用 Claude 將逐字稿整理成會議記錄"""
    if not ANTHROPIC_API_KEY:
        raise ValueError("請設定 ANTHROPIC_API_KEY 環境變數")
    
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    print("🤖 Claude 整理中...")
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": PROMPT_TEMPLATE.format(
                    transcript=transcript,
                    meeting_info=meeting_info if meeting_info else "（未提供，請依逐字稿內容判斷）"
                )
            }
        ]
    )
    
    return message.content[0].text

def save_output(content: str, output_path: str):
    """儲存會議記錄到檔案"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 會議記錄已儲存：{output_path}")

def main():
    if len(sys.argv) < 2:
        print("使用方式：python src/main.py <音檔路徑> [輸出路徑]")
        print("範例：python src/main.py meeting.m4a output/minutes.md")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output/minutes.md"
    info_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    if not os.path.exists(audio_path):
        print(f"❌ 找不到音檔：{audio_path}")
        sys.exit(1)
    
    # 讀取會議基本資料（選填）
    meeting_info = ""
    if info_path and os.path.exists(info_path):
        with open(info_path, "r", encoding="utf-8") as f:
            meeting_info = f.read()
        print(f"📋 已載入會議基本資料：{info_path}")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Step 1: 轉錄
    transcript = transcribe_audio(audio_path)
    print(f"\n📝 逐字稿（前200字）：\n{transcript[:200]}...\n")
    
    # Step 2: 整理
    minutes = generate_minutes(transcript, meeting_info)
    
    # Step 3: 儲存
    save_output(minutes, output_path)
    
    print("\n🎉 完成！")

if __name__ == "__main__":
    main()
