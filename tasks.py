from crewai import Task
from textwrap import dedent

class ContentTasks:
    def __tip_section(self):
        return "Remember, your job is to ensure the content is creative, accurate, and engaging. Deliver top-quality work to help improve the overall user experience!"

    def generate_content(self, agent, topic, length, tone):
        return Task(
            description=dedent(
                f"""
                **Task**: Generate Creative Content
                **Description**: Create a {length} article, blog post, or social media content on the topic "{topic}". 
                    The content should be engaging and tailored to the audience's preferences. Ensure the tone is {tone} 
                    and the structure is appropriate for the format chosen (e.g., blog post, social media caption, etc.).

                **Parameters**:
                - Topic: {topic}
                - Content Length: {length}
                - Tone: {tone}

                **Note**: Ensure content flows well and is tailored to the target audience.
                """
            ),
            agent=agent,
        )

    def optimize_for_seo(self, agent, content, primary_keywords, secondary_keywords):
        return Task(
            description=dedent(
                f"""
                **Task**: SEO Optimization
                **Description**: Optimize the provided content for SEO. Integrate the primary and secondary keywords 
                    naturally into the content, improve headings, meta tags, and ensure proper keyword density.
                    Additionally, check for readability and provide suggestions for SEO improvement.

                **Parameters**:
                - Content: {content}
                - Primary Keywords: {primary_keywords}
                - Secondary Keywords: {secondary_keywords}

                **Note**: Ensure the content remains readable while being optimized for search engines.
                """
            ),
            agent=agent,
        )

    def fact_check_content(self, agent, content):
        return Task(
            description=dedent(
                f"""
                **Task**: Fact-Check Generated Content
                **Description**: Cross-check the accuracy of facts, statistics, and claims made in the provided content. 
                    Verify information from reputable sources to ensure that the content is trustworthy and factually correct.

                **Parameters**:
                - Content: {content}

                **Note**: Flag any discrepancies or inaccuracies, and suggest credible sources for corrections.
                """
            ),
            agent=agent,
        )

    def summarize_content(self, agent, content, summary_length):
        return Task(
            description=dedent(
                f"""
                **Task**: Summarize Content
                **Description**: Condense the provided content into a summary of approximately {summary_length} words. 
                    Ensure the summary captures all the key points while making it easy for the reader to grasp the main ideas quickly.

                **Parameters**:
                - Content: {content}
                - Summary Length: {summary_length}

                **Note**: Focus on the core ideas while maintaining the integrity of the original content.
                """
            ),
            agent=agent,
        )
