import os
import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from groq import Groq
from huggingface_hub import login

# Log in using your Hugging Face token
hf_token = "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"  # Replace with your actual Hugging Face token
login(token=hf_token)

# Set your Groq API key
os.environ["GROQ_API_KEY"] = "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"  # Replace with your actual API key

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Load the model name
model_name = "meta-llama/Llama-2-8b-hf"  # Ensure this model exists on Hugging Face

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load the model on CPU (no quantization)
device = "cpu"  # Specify CPU usage
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32).to(device)  # Use full precision

# Create a text generation pipeline on CPU
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)  # Set device to CPU (-1)

def summarize_text(text):
    """Generates a summary of the provided text using the LLaMA model."""
    with torch.no_grad():  # Reduce memory usage during inference
        summary = pipe(text, max_length=150, num_return_sequences=1)[0]['generated_text']
    return summary

def get_insight_from_groq(content):
    """Fetches insights from Groq API based on the provided content."""
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": content}],
        model="llama3-8b-8192",  # Update to your desired Groq model
    )
    return chat_completion.choices[0].message.content

# Streamlit application
def main():
    st.title("Text Summarization and Insight Generator")
    st.write("Enter the text you want to summarize and get insights for:")

    # Input text area for user input
    original_text = st.text_area("Input Text", height=min(len(original_text)//2 + 50, 500))

    if st.button("Generate Summary and Insights"):
        if original_text:
            try:
                # Generate summary
                summary = summarize_text(original_text)
                st.subheader("Summary:")
                st.write(summary)

                # Get insights based on the summary
                insight = get_insight_from_groq(summary)
                st.subheader("Insight from Groq:")
                st.write(insight)

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter some text before generating a summary.")

if __name__ == "__main__":
    main()
