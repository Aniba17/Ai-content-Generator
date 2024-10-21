# main.py
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
        agents = ContentCreators()
        tasks = ContentTasks()

        content_research_agent = agents.content_research_agent()
        content_generation_agent = agents.content_generation_agent()
        editing_optimization_agent = agents.editing_and_optimization_agent()

        crew = Crew(
            agents=[
                content_research_agent,
                content_generation_agent,
                editing_optimization_agent,
            ],
            tasks=[
                tasks.ContentResearchTool(),  
                tasks.TextSummarizationTool(),  
            ],
            verbose=True,
        )

        result = crew.kickoff()
        return result

def main():
    st.title("AI Content Generator Crew")
    st.sidebar.header("User Input")

    task_type = st.sidebar.selectbox(
        "Choose the Task",
        ("Generate Content", "Summarize Text")
    )

    topic = st.sidebar.text_input("Topic", "")
    requirements = st.sidebar.text_input("Requirements (e.g., length, format)", "")
    interests = st.sidebar.text_input("Interests related to this topic", "")

    if st.sidebar.button("Submit"):
        if task_type == "Generate Content":
            if topic and requirements and interests:
                content_crew = ContentCrew(topic, requirements, interests, task_type)
                result = content_crew.run()
                st.subheader("Generated Content")
                st.write(result)
            else:
                st.warning("Please fill in all fields.")
        
        elif task_type == "Summarize Text":
            if topic:
                content_crew = ContentCrew(topic, requirements, interests, task_type)
                result = content_crew.run()
                st.subheader("Summarized Content")
                st.write(result)
            else:
                st.warning("Please enter the text to summarize.")

if __name__ == "__main__":
    main()
