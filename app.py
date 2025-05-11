# OpenAI JSONL to CSV Converter

A simple Streamlit web application that converts OpenAI's fine-tuning JSONL format to CSV format.

## Features

- Upload OpenAI supervised fine-tuning JSONL files
- Convert to a simple two-column CSV format with "prompt" and "completion" columns
- Preview the converted data
- Download the resulting CSV file
- View basic statistics about your dataset

## How it Works

The converter:
1. Processes each JSONL line containing message arrays
2. Extracts system messages into a "system" column
3. Extracts user messages into a "user" column
4. Extracts assistant messages into an "assistant" column
5. Organizes the data into a downloadable CSV format

## Installation

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/openai-jsonl-to-csv.git
cd openai-jsonl-to-csv

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run openai_jsonl_to_csv.py
```

### Deploy on Streamlit Cloud

1. Fork this repository to your GitHub account
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and connect it to your forked repository
4. Deploy the app with the following settings:
   - Main file path: `openai_jsonl_to_csv.py`

## Expected Input Format

The JSONL file should follow OpenAI's fine-tuning format:

```json
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}, {"role": "assistant", "content": "Hi there! How can I help you today?"}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What's the weather like?"}, {"role": "assistant", "content": "I don't have access to real-time weather data. To get the current weather, you could check a weather website or app."}]}
```

## Output Format

The resulting CSV will have two columns:
- `prompt`: Combined system and user messages
- `completion`: Assistant's response

## License

MIT
