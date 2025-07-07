import streamlit as st
from llama_cpp import Llama

# Load model
@st.cache_resource
def load_model():
    return Llama(model_path="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")

llm = load_model()



# Function for long paragraphs
def explain_paragraph_like_five(paragraph):
    prompt = f"""
You are Ms. Teacher, a fun, silly science teacher who explains hard science ideas to 5-year-olds. You speak like you're telling a fun bedtime story with toys, food, and animals. Use short sentences. Don't repeat the paragraph. Avoid big words.

Example:
Text: "Photosynthesis is a process in which plants use sunlight to synthesize food from carbon dioxide and water. It releases oxygen as a byproduct and occurs in the chloroplasts."
Explain it like I’m five: "Plants are little chefs! 🌿 They grab sunshine, water, and air to make yummy sugar snacks. While cooking, they puff out fresh air for us to breathe. Pretty cool, right?"

Text: "{paragraph}"
Explain it like I’m five:
"""
    response = llm(prompt, max_tokens=300, temperature=0.7, stop=["Text:", "\n\n", "Q:"])
    return response["choices"][0]["text"].strip()




# Function for short questions
def explain_question_like_five(question):
    prompt = f"""
You are Ms. Teacher, a fun and silly science teacher who explains science to 5-year-olds using fun stories and easy words. Use silly examples with toys, food, or animals.

Only give one short paragraph. No lists. No numbers. Be cheerful.

Q: What is gravity?
A: Gravity is like a big invisible hand that pulls your toys back down when you toss them in the air! It keeps us on the ground so we don’t float away like balloons!

Q: Why is the sky blue?
A: Because sunlight gets scattered in the air, and blue light spreads the most—so our eyes see a big beautiful blue sky!

Q: {question}
A:"""
    response = llm(prompt, max_tokens=200, temperature=0.7, stop=["Q:", "\n\n"])
    return response["choices"][0]["text"].strip()




# Streamlit UI
st.set_page_config(page_title="Explain Like I'm 5", page_icon="🧠")
st.title("🧠 Explain Like I'm 5")
st.markdown("Ask any science question or paste a hard paragraph — I'll explain it like you're 5! 👧🧒")

user_input = st.text_area("Enter a science question or paragraph here:", height=150)

if st.button("Explain it!"):
    if user_input.strip() == "":
        st.warning("Please type something first!")
    else:
        with st.spinner("Thinking like a 5-year-old... 🤔"):
            if len(user_input.split()) <= 10:
                answer = explain_question_like_five(user_input)
            else:
                answer = explain_paragraph_like_five(user_input)
        st.success("Here's your kid-friendly explanation:")
        st.markdown(f"### ✨ {answer}")