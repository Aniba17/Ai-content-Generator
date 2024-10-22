from textwrap import dedent
from groq import Groq
from crewai import Agent
from tasks import ContentTasks

class ContentCreators:
    def __init__(self):
        # Securely manage the Groq API key, do not hardcode it in production
        self.api_key = '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'
        self.client = Groq(api_key=self.api_key)
        self.model_name = "llama3-8b-8192"

    # Method to create chat completion using Groq
    def generate_content(self, prompt):
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model_name,
        )
        return chat_completion.choices[0].message.content

    def content_research_agent(self):
        return Agent(
            role="Content Research Agent",
            backstory=dedent("An expert in researching various subjects and summarizing key points."),
            goal=dedent("To gather relevant and high-quality information from reliable sources on the given topic, summarizing key points and facts for the content creation process."),
            tools=[ContentTasks().content_research_tool()],
            verbose=True,
            llm=self.generate_content,
        )

    def content_generation_agent(self):
        research_tool = ContentTasks().content_research_tool()
        summarization_tool = ContentTasks().text_summarization_tool()
        
        return Agent(
            role="Content Generation Agent",
            backstory=dedent("An expert in generating original content based on research."),
            goal=dedent("To produce original content based on the provided research, ensuring that it meets the user's requirements."),
            tools=[research_tool, summarization_tool],
            verbose=True,
            llm=self.generate_content,
        )

    def editing_and_optimization_agent(self):
        summarization_tool = ContentTasks().text_summarization_tool()
        
        return Agent(
            role="Editing and Optimization Agent",
            backstory=dedent("Experienced editor with knowledge of SEO best practices and content optimization."),
            goal=dedent("To review the generated content, optimizing it for readability, SEO, and overall quality."),
            tools=[summarization_tool],
            verbose=True,
            llm=self.generate_content,
        )

    def feedback_and_iteration_agent(self):
        summarization_tool = ContentTasks().text_summarization_tool()
        
        return Agent(
            role="Feedback and Iteration Agent",
            backstory=dedent("Experienced editor with knowledge of SEO best practices and content optimization."),
            goal=dedent("To analyze the content and provide constructive feedback, suggesting improvements to better meet audience needs."),
            tools=[summarization_tool],
            verbose=True,
            llm=self.generate_content,
        )
