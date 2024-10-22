from crewai import Task
from textwrap import dedent
from tools import ContentResearchTool  # Ensure correct import of your tool

class ContentTasks:
    def content_research_tool(self):
        return ContentResearchTool()  # Instantiate the ContentResearchTool

    def text_summarization_tool(self):
        return Task(
            description=dedent("""
                **Task**: Text Summarization
                **Description**: Summarize the provided text into a concise and engaging format.
            """),
            agent="Content Generation Agent"
        )

    def generate_content(self, agent, topic, length, tone):
        return Task(
            description=dedent(f"""
                **Task**: Generate Content
                **Description**: Create content on the topic "{topic}". The content should be engaging and tailored to the audience's preferences.
                **Length**: {length}
                **Tone**: {tone}
            """),
            agent=agent
        )

    def summarize_content(self, agent, content, summary_length):
        return Task(
            description=dedent(f"""
                **Task**: Summarize Content
                **Description**: Summarize the provided content in approximately {summary_length} words.
            """),
            agent=agent
        )
