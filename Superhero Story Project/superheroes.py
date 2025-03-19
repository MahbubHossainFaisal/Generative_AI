from dotenv import load_dotenv
from transformers import pipeline
import os
import asyncio
import streamlit as st
# Load environment variables
load_dotenv()




# Hugging Face API key (from .env file)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Configure the Hugging Face model
generator = pipeline(
    'text-generation', 
    model='gpt2',  # Replace with a valid model name
    use_auth_token=HUGGINGFACE_API_KEY
)

# Streamlit UI
st.title("Superhero Story Generator")
st.write("Enter details about your superhero to generate a story!")

# Input fields
superhero_name = st.text_input("Superhero Name", "Spider-Man")
superpower = st.text_input("Superpower", "web-slinging")
villain = st.text_input("Villain", "Green Goblin")
tone = st.selectbox("Tone", ["funny", "serious", "dramatic"])
setting = st.text_input("Setting", "New York City")

# Dynamic prompt template
prompt_template = f"""
In the bustling city of {setting}, a superhero named {superhero_name} protects the streets with their incredible power of {superpower}. 
One day, the notorious villain {villain} threatens to destroy {setting}. 
{superhero_name} must use their {superpower} to stop {villain} and save the day. 

The story begins with {superhero_name} swinging through the skyscrapers of {setting}, when suddenly...
"""

# Generate and display the story
if st.button("Generate Story"):
    story = generator(prompt_template, max_length=200, num_return_sequences=1)
    st.write(story[0]['generated_text'])