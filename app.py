import os
import autogen
from autogen import AssistantAgent, UserProxyAgent
import streamlit as st

# Define agent creation functions
def get_groq_configuration():
    return [
        {
            "model": "gemma-7b-it",  # Replace with your desired Groq model
            "api_key": "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",  # Use environment variable for API key
            "api_type": "groq"
        }
    ]

def create_agents():
    config_list = get_groq_configuration()

    try:
        AI_Counselor = autogen.AssistantAgent(
            name="AI Counselor",
            llm_config={"config_list": config_list},
            system_message=""" 
            You are an AI Counselor providing empathetic support to users based on their emotional states. Respond with comforting and supportive messages tailored to how the user is feeling. Avoid providing feedback or analysis unrelated to their emotional state.
            """,
            human_input_mode="NEVER"
        )

        Mood_Tracker_Agent = autogen.AssistantAgent(
            name="Mood Tracker Agent",
            llm_config={"config_list": config_list},
            system_message=""" 
            You are responsible for logging and tracking the user's emotional states. Record the user's reported mood and maintain a history of these logs. Provide mood data to the AI Counselor when requested.
            """,
            human_input_mode="NEVER"
        )

        Mindfulness_Guide_Agent = autogen.AssistantAgent(
            name="Mindfulness Guide Agent",
            llm_config={"config_list": config_list},
            system_message=""" 
            You guide users through mindfulness and relaxation exercises. Offer techniques to reduce stress and anxiety, such as breathing exercises or meditation practices.
            """,
            human_input_mode="NEVER"
        )

        User_Agent = autogen.UserProxyAgent(
            name="User_Agent",
            llm_config={"config_list": config_list},
            human_input_mode="NEVER",
            is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
            code_execution_config={
                "last_n_messages": 3,
                "work_dir": "tasks",
                "use_docker": False,
            }
        )

        nested_chats_config = [
            {
                "sender": AI_Counselor,
                "recipient": Mood_Tracker_Agent,
                "message": "Provide mood data for the user based on their recent interactions.",
                "max_turns": 2,
                "summary_method": "last_msg",
            },
            {
                "sender": AI_Counselor,
                "recipient": Mindfulness_Guide_Agent,
                "message": "Offer mindfulness exercises based on the user's needs and current state.",
                "max_turns": 2,
                "summary_method": "last_msg",
            },
            {
                "sender": Mood_Tracker_Agent,
                "recipient": AI_Counselor,
                "message": "Send recent mood data collected from the user.",
                "max_turns": 2,
                "summary_method": "last_msg",
            },
            {
                "sender": Mindfulness_Guide_Agent,
                "recipient": AI_Counselor,
                "message": "Provide a summary of mindfulness exercises given to the user.",
                "max_turns": 2,
                "summary_method": "last_msg",
            }
        ]

        User_Agent.register_nested_chats(
            nested_chats_config,
            trigger=AI_Counselor
        )

        return User_Agent, AI_Counselor

    except Exception as e:
        st.error(f"Error creating agents: {e}")
        raise

# Task processing function
def process_task(task):
    try:
        User_Agent, AI_Counselor = create_agents()
        result = User_Agent.initiate_chat(
            recipient=AI_Counselor,
            message=task,
            max_turns=2,
            summary_method="last_msg"
        )
        
        # Check if result is a ChatResult object and extract content
        if isinstance(result, autogen.ChatResult):
            response_content = result.summary  # Adjust this according to the actual attribute for response content
            return {"response": response_content}
        else:
            return {"error": "Unexpected result type"}
    
    except Exception as e:
        return {"error": str(e)}

# Main function for processing user input
def main():
    st.title("AI-powered Mental Health Support System")

    # Input field for user's feelings
    user_input = st.text_area("How are you feeling today?")

    if st.button("Submit"):
        if user_input:
            # Construct the task based on the user's input
            task = f"The user says: '{user_input}'. Respond with empathetic and supportive advice directly related to the user's feelings."
            
            # Process the task with the agents
            response = process_task(task)
            
            # Display the response
            if "error" in response:
                st.error(f"Error: {response['error']}")
            else:
                st.success(f"AI Counselor's Response: {response['response']}")
        else:
            st.warning("Please share how you're feeling.")

# Run the app
if __name__ == "__main__":
    main()
