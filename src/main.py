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

PROMPT_TEMPLATE = """你是一位專業的會議記錄助手。請根據以下會議逐字稿，整理出一份正式的會議記錄。

格式如下：
## 重點說明
（本次會議的主要討論事項摘要）

## 意見整理
（各方意見與討論內容）

## 主席裁示
（主席的決定或指示）

## 擬辦
（後續行動事項，包含負責人與期限）

---
以下是逐字稿：
{transcript}
"""

def transcribe_audio(audio_path: str, model_size: str = "base") -> str:
    """使用 Whisper 將音檔轉為文字"""
    print(f"📢 載入 Whisper 模型（{model_size}）...")
    model = whisper.load_model(model_size)
    
    print(f"🎙️ 開始轉錄：{audio_path}")
    result = model.transcribe(audio_path, language="zh")
    
    return result["text"]

def generate_minutes(transcript: str) -> str:
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
                "content": PROMPT_TEMPLATE.format(transcript=transcript)
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
    
    if not os.path.exists(audio_path):
        print(f"❌ 找不到音檔：{audio_path}")
        sys.exit(1)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Step 1: 轉錄
    transcript = transcribe_audio(audio_path)
    print(f"\n📝 逐字稿（前200字）：\n{transcript[:200]}...\n")
    
    # Step 2: 整理
    minutes = generate_minutes(transcript)
    
    # Step 3: 儲存
    save_output(minutes, output_path)
    
    print("\n🎉 完成！")

if __name__ == "__main__":
    main()
