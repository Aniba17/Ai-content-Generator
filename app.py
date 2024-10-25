import streamlit as st
from crewai import Crew
from textwrap import dedent
from agents import ContentCreators
from tasks import ContentTasks
from dotenv import load_dotenv

load_dotenv()

class ContentCrew:
    def __init__(self, topic, content_length, tone):
        self.topic = topic
        self.content_length = content_length
        self.tone = tone

    def run(self):
        # Initialize your agents and tasks
        agents = ContentCreators()
        tasks = ContentTasks()

        # Define your content creation agents
        content_research_agent = agents.content_research_agent()
        content_generation_agent = agents.content_generation_agent()

        # Check if agents are correctly initialized
        if content_research_agent is None or content_generation_agent is None:
            raise ValueError("One or more content creation agents are not initialized.")

        # Define the task for content generation
        generate_content_task = tasks.generate_content(
            content_generation_agent,
            self.topic,
            self.content_length,
            self.tone
        )

        # Check if the generate_content task is properly initialized
        if generate_content_task is None:
            raise ValueError("Content generation task could not be created.")

        # Define your crew
        crew = Crew(
            agents=[
                content_research_agent,
                content_generation_agent
            ],
            tasks=[
                generate_content_task
            ],
            verbose=True,
        )

        result = crew.kickoff()
        return result

# Streamlit app
def main():
    st.title("Content Creation Crew")
    st.markdown("Welcome to the Content Creation Crew! Create engaging and creative content with ease.")

    # User inputs
    topic = st.text_input("What topic do you want to create content about?")
    content_length = st.selectbox("What is the desired length of the content?", ["Short", "Medium", "Long"])
    tone = st.selectbox("What tone do you want for the content?", ["Formal", "Casual", "Humorous"])

    if st.button("Generate Content"):
        if topic and content_length and tone:
            content_crew = ContentCrew(topic, content_length, tone)
            try:
                result = content_crew.run()
                st.markdown("### Here is your Content Creation Result:")
                st.write(result)
            except ValueError as e:
                st.error(f"Error: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please fill in all fields.")

if __name__ == "__main__":
    main()
