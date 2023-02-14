import cohere
import streamlit as st
import os
import textwrap

# Cohere API key
api_key = os.environ["COHERE_API_KEY"]

# Set up Cohere client
co = cohere.Client(api_key)

def generate_output(user_prompt):
  base_prompt = textwrap.dedent("""
    Give six answers to the below question, 
    Give the First answer as how jesus would have given the  answer to that question, 
    Give the second answer as how prophet muhammad  would have given the  answer to that question, 
    Give the third answer as how the lord krishna  would have given the answer to that question,
    Give the forth answer as how osho would have given the  answer to that question,
    Give the fifth answer as how Swami Vivekananda would have given the  answer to that question.
    Question:""")

  # Call the Cohere Generate endpoint
  response = co.generate( 
    model='command-xlarge-20221108', 
    prompt = base_prompt + " " + user_prompt + "\nAnswer: ",
    max_tokens=300, 
    temperature=0.9,
    k=0, 
    p=0.7, 
    frequency_penalty=0.1, 
    presence_penalty=0, 
    stop_sequences=["--"])
  ai_output = response.generations[0].text
  ai_output = ai_output.replace("\n\n--","").replace("\n--","").strip()

  return ai_output


# The front end code starts here

st.title(" Ask Llama")

form = st.form(key="user_settings")
with form:
  st.write("Enter a question and Llama will give you answers from Bible, Quran and Gita")
  # User input - Question
  user_input = st.text_input("Question", key = "user_input")

  # Submit button to start generating answer
  generate_button = form.form_submit_button("Submit Question")
  num_input = 1
  if generate_button:
    if user_input == "":
      st.error("Question cannot be blank")
    else:
      my_bar = st.progress(0.05)
      st.subheader("Answers from Bible, Quran and Gita:")

      for i in range(num_input):
          st.markdown("""---""")
          ai_output = generate_output(user_input)
          st.write(ai_output)
          my_bar.progress((i+1)/num_input)

st.write( '')
st.markdown("Created by [LLAMA](https://www.myllama.co/), inspired by AskAIBhagvadGita")
