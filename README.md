# 🤖 AI Data Analyst Agent

> **An AI-powered data analyst that answers questions about your datasets using natural language.**
> Built with Google Gemini API • Python • Flask
   
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-API-4285F4?logo=google&logoColor=white)](https://ai.google.dev)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 **Natural Language Queries** | Ask questions about your data in plain English |
| 📊 **Auto-Generated Charts** | Bar, line, pie, and horizontal bar charts with dark theme |
| 🗄️ **SQL Generation** | See the exact SQL query used for every answer |
| 💡 **Business Insights** | Get 2-3 key takeaways with every analysis |
| 📁 **CSV Upload** | Upload any CSV file or use the built-in sample dataset |
| 🌐 **Web Interface** | Beautiful dark-mode chat UI with glassmorphism design |
| 🖥️ **CLI Mode** | Run the agent directly in your terminal |

---

## 🎬 Demo

### Web Interface
Upload a CSV → Ask questions → Get instant answers with charts!

**Example conversations:**
```
You:    "What's the total revenue by region?"
Agent:  The North region leads with $182K in total revenue, followed by West at $156K...
        📊 [Bar chart generated]
        📝 SQL: SELECT Region, SUM(Revenue) FROM data GROUP BY Region ORDER BY SUM(Revenue) DESC

You:    "Show me the monthly sales trend"
Agent:  Revenue shows a strong upward trend from January ($52K) to December ($89K)...
        📈 [Line chart generated]

You:    "Which product has the highest profit margin?"
Agent:  Cloud Suite leads with a 70% profit margin, significantly higher than...
        💡 Insights:
          • Software products have 2x the margin of hardware
          • Accessories have the lowest margin but highest volume
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-data-analyst-agent.git
cd ai-data-analyst-agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Your API Key
```bash
# Linux/macOS
export GEMINI_API_KEY="your_api_key_here"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"
```

### 4. Run the Web App
```bash
python app.py
```
Open **http://localhost:5000** in your browser. 🎉

### 4b. Or Run in Terminal Mode
```bash
python agent.py
```

---

## 📁 Project Structure

```
ai-data-analyst-agent/
├── 📄 README.md              ← You are here
├── 🤖 agent.py               ← Core Gemini-powered analysis agent
├── 🗄️ data_loader.py         ← CSV loading, profiling & SQLite engine
├── 📊 chart_generator.py     ← Dark-themed chart generation (matplotlib)
├── 🌐 app.py                 ← Flask web server
├── 🎨 index.html             ← Chat web interface
├── 📦 requirements.txt       ← Python dependencies
├── 📁 sample_data/
│   └── sales_data.csv        ← Built-in demo dataset (100 rows)
├── 📁 static/                ← Generated chart images
├── 📁 uploads/               ← User-uploaded CSV files
└── 📁 screenshots/           ← Demo screenshots
```

---

## 🏗️ Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Web UI      │────▶│  Flask App   │────▶│  Agent Core  │
│  (HTML/JS)   │◀────│  (app.py)    │◀────│  (agent.py)  │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                          ┌───────────────────────┼───────────────────────┐
                          ▼                       ▼                       ▼
                   ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
                   │  Gemini API  │       │  Data Loader  │       │    Chart     │
                   │  (NL → SQL)  │       │  (SQLite)     │       │  Generator   │
                   └──────────────┘       └──────────────┘       └──────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| [Google Gemini API](https://ai.google.dev) | Natural language understanding & SQL generation |
| [Python](https://python.org) | Core language |
| [Flask](https://flask.palletsprojects.com) | Web server |
| [Pandas](https://pandas.pydata.org) | Data manipulation & profiling |
| [SQLite](https://sqlite.org) | In-memory SQL query engine |
| [Matplotlib](https://matplotlib.org) | Chart generation |

---

## 📊 Sample Dataset

The included `sales_data.csv` contains 100 rows of realistic sales data:

| Column | Type | Description |
|--------|------|-------------|
| Date | date | Transaction date (2024) |
| Region | text | North, South, East, West |
| Product | text | 6 product types |
| Category | text | Electronics, Accessories, Software |
| Units_Sold | int | Quantity sold |
| Unit_Price | float | Price per unit |
| Revenue | float | Total revenue |
| Cost | float | Total cost |
| Profit | float | Revenue - Cost |
| Sales_Rep | text | 6 sales representatives |
| Customer_Segment | text | Enterprise, SMB, Consumer |

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built during the [5-Day AI Agents Intensive Vibe Coding Course with Google](https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google) (June 2026)
- Powered by [Google Gemini API](https://ai.google.dev)
- Data visualization inspired by modern dashboard design patterns

---

**⭐ If you found this useful, please give it a star!**
