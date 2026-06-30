# 🤖 CrewAI LinkedIn Content Generator

An AI-powered multi-agent system built with **CrewAI**, **Google Gemini**, and **Serper** that researches a topic, analyzes YouTube videos, writes engaging LinkedIn posts, and generates AI image prompts.

---

## 🚀 Features

- 🌐 Web Research using Serper API
- 🎥 YouTube Video Research
- ✍️ AI-powered LinkedIn Post Generation
- 🎨 AI Image Prompt Generation with Gemini
- 🤖 Multi-Agent workflow using CrewAI
- 📝 Markdown export for generated LinkedIn posts

---

## 🛠 Tech Stack

- Python 3.11+
- CrewAI
- Google Gemini API
- Serper API
- crewai-tools
- python-dotenv

---

## 📂 Project Structure

```
.
├── skills/
│   └── linkedin-writing/
│       └── skill.md
├── writer_agent/
├── main.py
├── exta.py
├── linkedin_post.md
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/creatorKrishna05/Crewai-Agent.git

cd Crewai-Agent
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux/Mac

```bash
source .venv/bin/activate
```

### Install Dependencies

Using uv

```bash
uv sync
```

or pip

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
```

---

## ▶️ Run the Project

```bash
python main.py
```

---

## 📋 Example Input

```python
topic = "AI Agents"

youtube_video_url = "https://www.youtube.com/watch?v=HsQ9szWv1kM"
```

---

## 📤 Output

The project generates:

- Research Summary
- LinkedIn Post
- AI Image Prompt
- `linkedin_post.md`

---

## 🤖 Agents

### 🌐 Web Research Agent

Researches the latest information from the internet.

### 🎥 YouTube Research Agent

Extracts key insights from YouTube videos.

### ✍️ LinkedIn Writer Agent

Creates engaging and professional LinkedIn posts.

### 🎨 Image Creator Agent

Generates detailed AI image prompts using Gemini.

---

## 📸 Workflow

```
User Input
      │
      ▼
Web Research Agent
      │
      ▼
YouTube Research Agent
      │
      ▼
LinkedIn Writer Agent
      │
      ▼
Image Prompt Agent
      │
      ▼
Final LinkedIn Post + AI Image Prompt
```

---

## 📌 Future Improvements

- Streamlit Web App
- Image Generation Support
- LinkedIn Auto Posting
- Memory-enabled Agents
- RAG Integration
- PDF Research Support

---

## 👨‍💻 Author

**Kanchan**

GitHub:
https://github.com/creatorKrishna05

---

## ⭐ If you like this project

Please give this repository a ⭐ on GitHub.
