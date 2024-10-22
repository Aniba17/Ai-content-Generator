import streamlit as st
from crewai import Crew
from agents import ContentCreators
from tasks import ContentTasks

class ContentCrew:
    def __init__(self, topic, requirements, interests, task_type):
        self.topic = topic
        self.requirements = requirements
        self.interests = interests
        self.task_type = task_type

    def run(self):
        # Initialize agents and tasks
        agents = ContentCreators()
        tasks = ContentTasks()

        # Initialize agents based on the selected task
        content_research_agent = agents.content_research_agent()
        content_generation_agent = agents.content_generation_agent()
        editing_optimization_agent = agents.editing_and_optimization_agent()

        # Create task list based on the task type
        task_list = []
        if self.task_type == "Generate Content":
            task_list = [tasks.content_research_tool()]  # Call the correct method
            # Check if the content research agent is defined and matches the task
            if content_research_agent is None:
                st.error("Content Research Agent is not available.")
                return
        elif self.task_type == "Summarize Text":
            task_list = [tasks.text_summarization_tool()]  # Call the correct method
            # Check if the content generation agent is defined and matches the task
            if content_generation_agent is None:
                st.error("Content Generation Agent is not available.")
                return

        # Create a crew with agents and tasks
        crew = Crew(
            agents=[content_research_agent, content_generation_agent, editing_optimization_agent],
            tasks=task_list,
            verbose=True,
        )

        try:
            # Run the crew's kickoff process and return the result
            result = crew.kickoff()
        except Exception as e:
            result = f"Error during task execution: {str(e)}"

        return result

def main():
    # Streamlit UI setup
    st.title("AI Content Generator Crew")
    st.sidebar.header("User Input")

    # Task type selection
    task_type = st.sidebar.selectbox(
        "Choose the Task",
        ("Generate Content", "Summarize Text")
    )

    # User input fields
    topic = st.sidebar.text_input("Topic", "")
    
    # Only show requirements and interests fields if generating content
    if task_type == "Generate Content":
        requirements = st.sidebar.text_input("Requirements (e.g., length, format)", "")
        interests = st.sidebar.text_input("Interests related to this topic", "")
    else:
        requirements, interests = "", ""  # Not necessary for text summarization

    # Submit button action
    if st.sidebar.button("Submit"):
        if task_type == "Generate Content":
            # Check if all required fields are filled for content generation
            if topic and requirements and interests:
                content_crew = ContentCrew(topic, requirements, interests, task_type)
                result = content_crew.run()
                st.subheader("Generated Content")
                st.write(result)
            else:
                st.warning("Please fill in all fields for content generation.")
        elif task_type == "Summarize Text":
            # Only check if topic is filled for summarization
            if topic:
                content_crew = ContentCrew(topic, requirements, interests, task_type)
                result = content_crew.run()
                st.subheader("Summarized Content")
                st.write(result)
            else:
                st.warning("Please enter the text to summarize.")

if __name__ == "__main__":
    main()
