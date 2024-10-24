from langchain_community.chat_models import BedrockChat
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import streamlit as st

def create_biography_chain():
    # Initialize the Bedrock Chat model
    llm = BedrockChat(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        region_name="us-east-1",
        model_kwargs={
            "max_tokens": 700,
            "temperature": 0.7,
            "top_p": 0.9,
        }
    )

    # Create the prompt template
    template = """You are a creative career counselor and future biographer. 
    Based on the following answers from a Future Vision Quiz, create a detailed and inspiring 
    biography of this person's hypothetical future journey.

    Name: {name}
    Quiz Answers:
    1. Area of study interest: {area_of_study}
    2. Vision in 10 years: {vision_10_years}
    3. Most important future skill: {important_skill}
    4. Preferred work environment: {work_environment}
    5. Desired impact on the world: {desired_impact}

    Write an engaging biography of approximately 300 words that spans from their current 
    high school years to 20 years into the future. Include key milestones, career achievements, 
    and how their early choices shaped their path."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional biographer specializing in creating inspiring future life stories."),
        ("human", template)
    ])

    # Create the chain
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain

def generate_biography(answers):
    # Create the chain
    chain = create_biography_chain()
    
    # Prepare the input dictionary
    input_dict = {
        "name": st.session_state.name,
        "area_of_study": answers[0],
        "vision_10_years": answers[1],
        "important_skill": answers[2],
        "work_environment": answers[3],
        "desired_impact": answers[4]
    }
    
    # Generate the biography
    try:
        result = chain.run(input_dict)
        return result.strip()
    except Exception as e:
        return f"An error occurred while generating the biography: {str(e)}"

def process_quiz_results(st):
    """Process quiz results and store biography in session state"""
    if 'answers' in st.session_state and len(st.session_state.answers) == 5:
        answers = [st.session_state.answers[i] for i in range(5)]
        biography = generate_biography(answers)
        
        if biography:
            # Store biography in session state
            st.session_state.biography_text = biography
            st.session_state.biography_generated = True
            
            # Display the biography
            st.write("### 🌟 Your Future Biography")
            st.markdown(biography)
            return biography
    else:
        st.warning("Please complete all questions first.")
        return None