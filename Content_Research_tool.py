from typing import Any, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from groq import Groq

# Define the input schema for the tool
class ContentResearchToolInput(BaseModel):
    query: str = Field(..., description="The topic or query you want to research.")

# Define the ContentResearchTool class
class ContentResearchTool(BaseTool):
    name: str = "Content Researcher"
    description: str = "A tool that helps in researching content for articles, blogs, or any topic online."
    args_schema: Type[BaseModel] = ContentResearchToolInput

    def _run(self, query: str) -> str:
        """
        Executes the research based on the provided query using the Groq API.
        """
        # Set the API key directly (Replace 'your_groq_api_key_here' with your actual API key)
        api_key = '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'

        # Initialize the Groq client
        client = Groq(api_key=api_key)

        try:
            # Send the query to the Groq API's chat completion feature
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": query,
                    }
                ],
                model="llama3-8b-8192"  # Model can be changed based on available models
            )

            # Extract the result
            research_result = chat_completion.choices[0].message.content
            return f"Research results for query '{query}':\n{research_result}"

        except Exception as e:
            return f"Error occurred while making API request: {e}"

    async def _arun(self, query: str) -> str:
        """
        Asynchronous run for the tool. Can be used in async environments.
        """
        return {
    "query": query,
    "result": research_result
}

# Example of how to use the tool
if __name__ == "__main__":
    content_tool = ContentResearchTool()
    result = content_tool._run(query="Artificial Intelligence in Healthcare")
    print(result)
