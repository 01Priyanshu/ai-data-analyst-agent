"""
AI Data Analyst Agent
Powered by Google Gemini API - Analyzes datasets using natural language.
"""

import os
import json
import re
from data_loader import DataLoader
from chart_generator import (
    create_bar_chart,
    create_line_chart,
    create_pie_chart,
    create_horizontal_bar_chart,
)

try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


class DataAnalystAgent:
    """An AI-powered data analyst that answers questions about your data."""

    def __init__(self, api_key: str = None):
        self.loader = DataLoader()
        self.data_loaded = False
        self.profile = None
        self.chat = None

        if not HAS_GENAI:
            raise ImportError(
                "google-genai package not found. Install it with: pip install google-genai"
            )

        # Initialize Gemini client
        resolved_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not resolved_key:
            raise ValueError(
                "No API key found. Set GEMINI_API_KEY environment variable or pass api_key parameter."
            )

        self.client = genai.Client(api_key=resolved_key)
        self.model = "gemini-2.5-flash"

    def load_data(self, file_path: str) -> str:
        """Load a CSV file and return a summary."""
        self.profile = self.loader.load_csv(file_path)

        if "error" in self.profile:
            return f"Error: {self.profile['error']}"

        self.data_loaded = True
        self._init_chat()

        summary = f"""✅ Data loaded successfully!

📁 File: {self.profile['file_name']}
📊 Shape: {self.profile['rows']} rows × {self.profile['columns']} columns
💾 Memory: {self.profile['memory_usage']}
⚠️ Missing values: {self.profile['missing_values']}
🔄 Duplicate rows: {self.profile['duplicate_rows']}

📋 Columns:"""

        for col in self.profile['column_details']:
            dtype_icon = "🔢" if col['dtype'] in ('int64', 'float64') else "📝"
            summary += f"\n  {dtype_icon} {col['name']} ({col['dtype']}) - {col['unique_values']} unique values"

        summary += "\n\n💡 Ask me anything about this data! For example:"
        summary += "\n  • \"What's the total revenue by region?\""
        summary += "\n  • \"Show me the monthly sales trend\""
        summary += "\n  • \"Which product has the highest profit margin?\""
        summary += "\n  • \"Give me the SQL query for top 5 sales reps\""

        return summary

    def _init_chat(self):
        """Initialize the Gemini chat session with data context."""
        schema = self.loader.get_schema()
        sample = self.loader.get_sample(5)

        system_instruction = f"""You are an expert Data Analyst Agent. You help users analyze datasets by answering questions in plain English.

You have access to a dataset loaded into an SQLite database. Here is the schema and sample data:

--- DATABASE SCHEMA ---
{schema}

--- SAMPLE DATA (first 5 rows) ---
{sample}

--- INSTRUCTIONS ---
1. When the user asks a data question, respond with a JSON object containing your analysis.
2. Always include a SQL query that answers the question.
3. Format your response as a valid JSON object with these fields:
   - "answer": A clear, concise plain English answer to the question
   - "sql_query": The SQL query used (against table named 'data')
   - "chart_type": One of "bar", "line", "pie", "horizontal_bar", or "none"
   - "chart_title": Title for the chart (if applicable)
   - "chart_data": A dictionary of label:value pairs for the chart (if applicable)
   - "insights": A list of 2-3 key business insights
4. The SQL table is named 'data'. Column names are exactly as shown in the schema.
5. For trend questions, use "line" chart. For comparisons, use "bar" or "horizontal_bar". For proportions, use "pie".
6. Keep answers professional but conversational — like a senior data analyst presenting findings.
7. IMPORTANT: Return ONLY the JSON object, no markdown formatting, no code blocks, just raw JSON."""

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.3,
        )

        self.chat = self.client.chats.create(
            model=self.model,
            config=config,
        )

    def ask(self, question: str) -> dict:
        """Ask a question about the loaded data."""
        if not self.data_loaded:
            return {
                "answer": "Please load a dataset first using the load_data() method.",
                "chart": None,
            }

        try:
            response = self.chat.send_message(question)
            raw_text = response.text.strip()

            # Clean up response - remove markdown code blocks if present
            if raw_text.startswith("```"):
                raw_text = re.sub(r'^```(?:json)?\n?', '', raw_text)
                raw_text = re.sub(r'\n?```$', '', raw_text)

            result = json.loads(raw_text)

            # Execute the SQL query to get actual data
            if "sql_query" in result and result["sql_query"]:
                sql_result = self.loader.run_sql(result["sql_query"])
                result["sql_result"] = sql_result

            # Generate chart if requested
            chart_base64 = None
            if result.get("chart_type") and result.get("chart_data") and result["chart_type"] != "none":
                chart_data = result["chart_data"]
                chart_title = result.get("chart_title", "Chart")

                if result["chart_type"] == "bar":
                    chart_base64 = create_bar_chart(chart_data, chart_title)
                elif result["chart_type"] == "line":
                    chart_base64 = create_line_chart(chart_data, chart_title)
                elif result["chart_type"] == "pie":
                    chart_base64 = create_pie_chart(chart_data, chart_title)
                elif result["chart_type"] == "horizontal_bar":
                    chart_base64 = create_horizontal_bar_chart(chart_data, chart_title)

            result["chart"] = chart_base64
            return result

        except json.JSONDecodeError:
            return {
                "answer": raw_text,
                "chart": None,
                "insights": [],
            }
        except Exception as e:
            return {
                "answer": f"Error analyzing data: {str(e)}",
                "chart": None,
                "insights": [],
            }


def main():
    """Run the agent in interactive terminal mode."""
    print("\n" + "=" * 60)
    print("  🤖 AI Data Analyst Agent")
    print("  Powered by Google Gemini")
    print("=" * 60)

    agent = DataAnalystAgent()

    # Load sample data
    sample_path = os.path.join(os.path.dirname(__file__), "sample_data", "sales_data.csv")
    if os.path.exists(sample_path):
        print("\n" + agent.load_data(sample_path))
    else:
        csv_path = input("\n📂 Enter path to your CSV file: ").strip()
        print("\n" + agent.load_data(csv_path))

    print("\n" + "-" * 60)
    print("Type your questions below (type 'quit' to exit)")
    print("-" * 60)

    while True:
        try:
            question = input("\n🧑 You: ").strip()
            if question.lower() in ('quit', 'exit', 'q'):
                print("\n👋 Goodbye!")
                break
            if not question:
                continue

            print("\n🔍 Analyzing...")
            result = agent.ask(question)

            print(f"\n🤖 Agent: {result.get('answer', 'No answer generated.')}")

            if result.get('sql_query'):
                print(f"\n📝 SQL: {result['sql_query']}")

            if result.get('insights'):
                print("\n💡 Insights:")
                for insight in result['insights']:
                    print(f"   • {insight}")

            if result.get('chart'):
                print("\n📊 [Chart generated - visible in web interface]")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break


if __name__ == "__main__":
    main()
