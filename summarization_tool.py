import os
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from groq import Groq
from huggingface_hub import login

# Log in using your Hugging Face token
hf_token = os.getenv("HUGGINGFACE_TOKEN")  # Replace with your actual Hugging Face token
if hf_token:
    login(token=hf_token)
else:
    st.error("Hugging Face token not found. Please set the environment variable HUGGINGFACE_TOKEN.")

# Set your Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")  # Replace with your actual API key
if groq_api_key:
    os.environ["GROQ_API_KEY"] = groq_api_key
else:
    st.error("Groq API key not found. Please set the environment variable GROQ_API_KEY.")

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Load the model name
model_name = "llama3-8b-8129"  # Ensure this model exists on Hugging Face

# Load the tokenizer and model
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    # Create a text generation pipeline
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
except Exception as e:
    st.error(f"Failed to load model or tokenizer: {e}")

def summarize_text(text: str) -> str:
    """Generates a summary of the provided text using the LLaMA model."""
    try:
        summary = pipe(text, max_length=150, num_return_sequences=1)[0]['generated_text']
        return summary
    except Exception as e:
        st.error(f"Error in text summarization: {e}")
        return ""

def get_insight_from_groq(content: str) -> str:
    """Fetches insights from Groq API based on the provided content."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": content}],
            model="llama3-8b-8192"  # Using the specified Groq model
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error in fetching insights from Groq: {e}")
        return ""

# Streamlit application
def main():
    st.title("Text Summarization and Insight Generator")
    st.write("Enter the text you want to summarize and get insights for:")

    # Input text area for user input
    original_text = st.text_area("Input Text", height=300)  # Define the height as needed

    if st.button("Generate Summary and Insights"):
        if original_text:
            # Generate summary
            summary = summarize_text(original_text)
            if summary:
                st.subheader("Summary:")
                st.write(summary)

                # Get insights based on the summary
                insight = get_insight_from_groq(summary)
                st.subheader("Insight from Groq:")
                st.write(insight)
        else:
            st.warning("Please enter some text before generating a summary.")

if __name__ == "__main__":
    main()
