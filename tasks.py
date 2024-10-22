from crewai import Task

class ContentTasks:
    def content_research_tool(self):
        """
        Creates a task for content research.
        This task will gather high-quality information from reliable sources.
        """
        return Task(
            name="Content Research",
            description="Gathers high-quality information from reliable sources.",
            parameters={
                "topic": {"type": "string", "description": "The topic for which content is to be researched."},
                "requirements": {"type": "string", "description": "Specific requirements or constraints for the research."},
                "interest_areas": {"type": "string", "description": "Areas of interest related to the topic."}
            }
        )

    def text_summarization_tool(self):
        """
        Creates a task for summarizing text.
        This task will summarize provided content based on the given parameters.
        """
        return Task(
            name="Text Summarization",
            description="Summarizes the provided text.",
            parameters={
                "text": {"type": "string", "description": "The text that needs to be summarized."},
                "length": {"type": "string", "description": "Desired length of the summary (short, medium, long)."},
                "format": {"type": "string", "description": "Desired format for the summary (bullet points, paragraphs, etc.)."}
            }
        )
