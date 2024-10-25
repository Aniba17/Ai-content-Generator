from textwrap import dedent
from groq import Groq
from crewai import Agent
from tasks import ContentTasks  # Assuming ContentTasks is in tasks.py
from Content_Research_tool import ContentResearchTool  # Assuming ContentResearchTool is in tool_1.py
# from summarization_tool import TextSummarizationTool  # Assuming TextSummarizationTool is in tool_2.py

class ContentCreators:

    def __init__(self):
        # Directly set your Groq API key here
        self.api_key = "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"
        self.client = Groq(api_key=self.api_key)
        self.model_name = "gemma-7b-it"  # Use your chosen model

    # Method to create chat completion using Groq
    def generate_content(self, prompt):
        # Create a chat completion request using the Groq client
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model_name,
        )
        return chat_completion.choices[0].message.content

    def content_research_agent(self):
        return Agent(
            role="Content Research Agent",
            backstory=dedent(
                """An expert in researching various subjects and summarizing key points."""
            ),
            goal=dedent(
                """To gather relevant and high-quality information from reliable sources on the given topic, summarizing key points and facts that the content creation process can use."""
            ),
            tools=[ContentResearchTool()],  # Replace with your actual Content Research Tool
            verbose=True,
            llm=self.generate_content,  # Use the Groq-based content generation method
        )

    def content_generation_agent(self):
        return Agent(
            role="Content Generation Agent",
            backstory=dedent(
                """An expert in generating original content based on research."""
            ),
            goal=dedent(
                """To produce original content based on the provided research, ensuring that the content is engaging, informative, and meets the user's requirements."""
            ),
            tools=[ContentResearchTool()],  # Include both tools here
            verbose=True,
            llm=self.generate_content,  # Use the Groq-based content generation method
        )

# Example usage
if __name__ == "__main__":
    content_creators = ContentCreators()
    prompt = "Explain the importance of fast language models."
    result = content_creators.generate_content(prompt)
    print(f"Generated Content:\n{result}")
