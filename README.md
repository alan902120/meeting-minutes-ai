# 📝 Meeting Minutes AI

自動化會議記錄工具，使用 OpenAI Whisper 將會議錄音轉為逐字稿，再透過 Claude AI 整理成正式會議記錄。

## ✨ 功能

- 🎙️ **語音轉文字**：支援 `.m4a`、`.mp3`、`.wav` 等常見音檔格式
- 🤖 **AI 整理**：自動產出四段式會議記錄格式
- 📄 **Markdown 輸出**：會議記錄儲存為 `.md` 檔案，方便後續編輯

## 📋 會議記錄格式

- **重點說明**：本次會議主要討論事項摘要
- **意見整理**：各方意見與討論內容
- **主席裁示**：主席的決定或指示
- **擬辦**：後續行動事項，含負責人與期限

## 🚀 快速開始

### 1. 安裝套件

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 設定 API Key

```bash
cp .env.example .env
```

編輯 `.env`，填入你的 Anthropic API Key：

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
```

> 前往 [console.anthropic.com](https://console.anthropic.com) 取得 API Key

### 3. 執行

```bash
python src/main.py <音檔路徑> [輸出路徑]
```

**範例：**

```bash
python src/main.py meeting.m4a output/minutes.md
```

## 🛠️ 技術架構

| 元件 | 說明 |
|------|------|
| [OpenAI Whisper](https://github.com/openai/whisper) | 語音轉文字（本地端執行，免費） |
| [Anthropic Claude](https://www.anthropic.com) | AI 整理會議記錄 |
| Python 3.10+ | 主要開發語言 |

## 📁 專案結構

```
meeting-minutes-ai/
├── src/
│   └── main.py        # 主程式
├── output/            # 會議記錄輸出位置
├── requirements.txt   # 套件清單
├── .env.example       # 環境變數範本
└── README.md
```

## 👤 作者

**Alan** — [@alan902120](https://github.com/alan902120)

## 📋 使用方式更新

### 基本用法（只有音檔）
```bash
python src/main.py meeting.m4a output/minutes.md
```

### 完整用法（音檔 + 會議基本資料）
```bash
python src/main.py meeting.m4a output/minutes.md info.txt
```

### info.txt 範例
```
會議名稱：XXX計畫第N次部會溝通會議
會議主席：XX單位 XXX副執秘
會議出席人員：A單位 XXX、B單位 XXX
本署出席人員：金屬機電組 XXX科長、航太小組 XXX副組長、覃炳瑞專案經理
```
