import streamlit as st
from biography_generator import process_quiz_results
from image_generator_bedrock import process_biography_for_image

# Configure the page
st.set_page_config(
    page_title="Future Vision Quiz",
    page_icon="🔮",
    layout="wide"
)

# Initialize session state variables
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

if 'answers' not in st.session_state:
    st.session_state.answers = {}

if 'biography_generated' not in st.session_state:
    st.session_state.biography_generated = False

if 'biography_text' not in st.session_state:
    st.session_state.biography_text = ""

if 'name' not in st.session_state:
    st.session_state.name = ""

# Define questions and options
questions = [
    {
        "question": "Which area of study interests you the most?",
        "options": ["Sciences", "Humanities", "Arts", "Technology", "Business"]
    },
    {
        "question": "How do you see yourself in 10 years?",
        "options": ["Studying a postgraduate degree", "Working in a large company", "Running my own business", "Traveling the world", "Dedicated to research"]
    },
    {
        "question": "What skill do you think will be most important in your future?",
        "options": ["Communication", "Problem-solving", "Creativity", "Leadership", "Adaptability"]
    },
    {
        "question": "In what type of environment do you prefer to work?",
        "options": ["Traditional office", "Remote from home", "Outdoors", "Laboratory or workshop", "Mixed/flexible environment"]
    },
    {
        "question": "What kind of impact do you want to have on the world?",
        "options": ["Advancing science or technology", "Directly helping people", "Creating art or entertainment", "Driving social or political changes", "Innovating in business"]
    }
]

# Main app layout
st.title("🔮 Future Vision Quiz")
st.write("Answer these questions to discover your potential future path!")

# Name input section (only shown at the beginning)
if not st.session_state.name:
    st.write("### Welcome! Let's start with your name")
    name_input = st.text_input("What's your name?", key="name_input")
    if name_input:
        if st.button("Start Quiz"):
            st.session_state.name = name_input
            st.rerun()
else:
    st.write(f"### Welcome, {st.session_state.name}! 👋")
    
    # Display current question
    if st.session_state.current_question < len(questions):
        # Progress bar
        progress = st.session_state.current_question / len(questions)
        st.progress(progress)
        
        current_q = questions[st.session_state.current_question]
        st.write(f"### Question {st.session_state.current_question + 1} of {len(questions)}")
        st.write(f"**{current_q['question']}**")
        
        # Radio buttons for options
        answer = st.radio(
            "Choose your answer:",
            current_q["options"],
            key=f"q{st.session_state.current_question}",
            label_visibility="collapsed"
        )
        
        # Store answer in session state
        st.session_state.answers[st.session_state.current_question] = answer
        
        # Next button
        if st.button("Next Question ➡️"):
            st.session_state.current_question += 1
            st.rerun()

    # Display results and generate content
    else:
        st.write("### Your Answers")
        st.write(f"**Name:** {st.session_state.name}")
        for i, answer in st.session_state.answers.items():
            st.write(f"**{questions[i]['question']}**")
            st.write(f"*Your answer:* {answer}")
        
        st.write("---")

        # Biography Generation Section
        if not st.session_state.biography_generated:
            if st.button("🌟 Generate My Future Biography"):
                with st.spinner("Creating your future biography..."):
                    biography = process_quiz_results(st)
                    st.rerun()  # Rerun to update the UI with new state
        
        # Display biography and image generation option if biography exists
        if st.session_state.biography_generated and st.session_state.biography_text:
            st.write("### 🌟 Your Future Biography")
            st.markdown(st.session_state.biography_text)
            
            st.write("---")
            st.write("### 🎨 Visualize Your Future")
            
            # Image Generation Button
            if st.button("Generate Future Vision Image 🖼️"):
                career_area = st.session_state.answers[0]  # First answer is career area
                process_biography_for_image(st, st.session_state.biography_text, career_area, st.session_state.name)

        # Reset button
        st.write("---")
        if st.button("🔄 Start Over"):
            for key in ['current_question', 'answers', 'biography_generated', 'biography_text', 'name']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()