import streamlit as st
import pandas as pd
import json
import io
import base64

st.set_page_config(
    page_title="OpenAI JSONL to CSV Converter",
    page_icon="🔄",
    layout="wide"
)

st.markdown("""
# OpenAI JSONL to CSV Converter

This tool converts OpenAI fine-tuning format JSONL files to CSV format.

## How to use:
1. Upload your JSONL file containing supervised fine-tuning data
2. Click "Convert" to process the file
3. Download the resulting CSV

## Expected JSONL format:

```json
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}, {"role": "assistant", "content": "Hi there! How can I help you today?"}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What's the weather like?"}, {"role": "assistant", "content": "I don't have access to real-time weather data. To get the current weather, you could check a weather website or app."}]}
```

## How it works:
- The tool extracts the messages from each JSONL line
- For chat completions format, it separates messages into three columns:
  - system: System message content
  - user: User message content
  - assistant: Assistant message content
- The result is downloadable as a CSV file
""")

def process_jsonl(content):
    data = []
    
    # Process each line
    for line in content.strip().split('\n'):
        if not line.strip():
            continue
            
        try:
            # Parse the JSON line
            json_obj = json.loads(line)
            
            # Check if the expected format exists
            if 'messages' in json_obj:
                messages = json_obj['messages']
                
                # Initialize variables for system, user and assistant content
                system_content = ""
                user_content = ""
                assistant_content = ""
                
                # Process each message based on its role
                for message in messages:
                    role = message.get('role', '')
                    content = message.get('content', '')
                    
                    if role == 'system':
                        system_content = content
                    elif role == 'user':
                        user_content = content
                    elif role == 'assistant':
                        assistant_content = content
                
                # Add to data with separate columns
                data.append({
                    'system': system_content.strip(),
                    'user': user_content.strip(),
                    'assistant': assistant_content.strip()
                })
            else:
                # Handle simple prompt-completion format
                data.append({
                    'system': '',
                    'user': json_obj.get('prompt', ''),
                    'assistant': json_obj.get('completion', '')
                })
                
        except json.JSONDecodeError:
            st.error(f"Error parsing JSON: {line}")
    
    return pd.DataFrame(data)

def get_csv_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="converted_data.csv">Download CSV File</a>'
    return href

def main():
    st.header("Upload your JSONL file")
    
    uploaded_file = st.file_uploader("Choose a JSONL file", type="jsonl")
    
    if uploaded_file is not None:
        # Read the file
        content = uploaded_file.getvalue().decode("utf-8")
        
        if st.button("Convert to CSV"):
            with st.spinner("Converting..."):
                # Process the JSONL
                df = process_jsonl(content)
                
                # Show a preview
                st.success(f"Conversion complete! Found {len(df)} examples.")
                st.subheader("Preview:")
                st.dataframe(df.head(10))
                
                # Provide download link
                st.markdown(get_csv_download_link(df), unsafe_allow_html=True)
                
                # Show some stats
                st.subheader("Statistics:")
                st.write(f"Total examples: {len(df)}")
                st.write(f"Average system message length: {df['system'].str.len().mean():.1f} characters")
                st.write(f"Average user message length: {df['user'].str.len().mean():.1f} characters")
                st.write(f"Average assistant message length: {df['assistant'].str.len().mean():.1f} characters")

if __name__ == "__main__":
    main()
