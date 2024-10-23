from textwrap import dedent
from groq import Groq
from crewai import Agent
from chromadb import Documents, EmbeddingFunction, Embeddings


class ContentCreators:
    def __init__(self, api_key='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', model_name="llama3-8b-8192"):
        self.api_key = api_key  # Securely manage your API key
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name

    def generate_content(self, prompt):
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model_name,
        )
        return chat_completion.choices[0].message.content

    def content_research_agent(self, tasks):
        return Agent(
            role="Content Research Agent",
            backstory=dedent("An expert in researching various subjects and summarizing key points."),
            goal=dedent("To gather relevant and high-quality information from reliable sources on the given topic, summarizing key points and facts for the content creation process."),
            tools=[tasks.content_research_tool()],
            verbose=True,
            llm=self.generate_content,
        )

    def content_generation_agent(self, tasks):
        return Agent(
            role="Content Generation Agent",
            backstory=dedent("An expert in generating original content based on research."),
            goal=dedent("To produce original content based on the provided research, ensuring that it meets the user's requirements."),
            tools=[tasks.content_research_tool(), tasks.text_summarization_tool()],
            verbose=True,
            llm=self.generate_content,
        )

    def editing_and_optimization_agent(self, tasks):
        return Agent(
            role="Editing and Optimization Agent",
            backstory=dedent("Experienced editor with knowledge of SEO best practices and content optimization."),
            goal=dedent("To review the generated content, optimizing it for readability, SEO, and overall quality."),
            tools=[tasks.text_summarization_tool()],
            verbose=True,
            llm=self.generate_content,
        )

    def feedback_and_iteration_agent(self, tasks):
        return Agent(
            role="Feedback and Iteration Agent",
            backstory=dedent("Experienced editor with knowledge of SEO best practices and content optimization."),
            goal=dedent("To analyze the content and provide constructive feedback, suggesting improvements to better meet audience needs."),
            tools=[tasks.text_summarization_tool()],
            verbose=True,
            llm=self.generate_content,
        )
