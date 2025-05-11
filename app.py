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
- For chat completions format, it combines system and user messages into one "prompt" column
- The assistant messages become the "completion" column
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
                
                # Initialize variables for prompt and completion
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
                
                # Create the prompt (combining system and user messages)
                prompt = ""
                if system_content:
                    prompt += f"System: {system_content}\n\n"
                prompt += f"User: {user_content}"
                
                # Add to data
                data.append({
                    'prompt': prompt.strip(),
                    'completion': assistant_content.strip()
                })
            else:
                # Handle simple prompt-completion format
                data.append({
                    'prompt': json_obj.get('prompt', ''),
                    'completion': json_obj.get('completion', '')
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
                st.write(f"Average prompt length: {df['prompt'].str.len().mean():.1f} characters")
                st.write(f"Average completion length: {df['completion'].str.len().mean():.1f} characters")

if __name__ == "__main__":
    main()
