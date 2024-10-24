import streamlit as st
from app import ContentCrew  # Import the ContentCrew class
from tasks import ContentTasks  # Import the ContentTasks class
from summarization_tool import summarize_text, get_insight_from_groq  # Import summarization functions


# Set the title of the Streamlit app
st.title("AI Content Generator")

# Create a sidebar for user input
st.sidebar.header("User Input")

# Options for the user to choose
task_option = st.sidebar.selectbox(
    "Select Task",
    ("Generate Content", "Summarize Text")
)

# User input for content generation
if task_option == "Generate Content":
    topic = st.sidebar.text_input("Enter the topic")
    requirements = st.sidebar.text_input("Enter content requirements (e.g., length, format)")
    interests = st.sidebar.text_input("Enter your interests related to this topic")

    if st.sidebar.button("Generate"):
        if topic and requirements and interests:
            try:
                # Initialize the ContentCrew with the user inputs
                content_crew = ContentCrew(topic, requirements, interests, task_type="Generate Content")
                result = content_crew.run()  # Pass the inputs directly
                st.success("Generated Content:")
                st.write(result)  # Display the generated content
            except Exception as e:
                st.error(f"Error occurred while generating content: {e}")
        else:
            st.warning("Please fill in all fields for content generation.")

# User input for summarization
elif task_option == "Summarize Text":
    text_to_summarize = st.sidebar.text_area("Enter text to summarize")
    summary_length = st.sidebar.number_input("Desired summary length (words)", min_value=1, value=50)

    if st.sidebar.button("Summarize"):
        if text_to_summarize:
            try:
                summary_result = summarize_text(text_to_summarize, max_length=summary_length)
                st.success("Summary:")
                st.write(summary_result)  # Display the summary

                # Optionally get insights from Groq API based on the summary
                insight = get_insight_from_groq(summary_result)
                st.subheader("Insight from Groq:")
                st.write(insight)

            except Exception as e:
                st.error(f"Error occurred while summarizing text: {e}")
        else:
            st.warning("Please enter text to summarize.")
