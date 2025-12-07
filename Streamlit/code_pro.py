import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import re
from dotenv import load_dotenv
import os
load_dotenv()

import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "Enter your HuggingFace API Token here"

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",  # lightweight but smart model
    temperature=0.5,
    max_new_tokens=512,
)
model = ChatHuggingFace(llm=llm)

#  Streamlit UI
st.set_page_config(page_title="CodeGenius", page_icon="🤖", layout="centered")
st.title("🤖 CodeGenius — Your AI Coding Assistant")
st.markdown("Choose what you want to do:")

option = st.radio("Select Mode", ["🧠 Code Analyzer", "⚙️ Code Generator"])


#  Code Analyzer Section
if option == "🧠 Code Analyzer":
    st.subheader("Analyze Your Code")

    analysis_options = st.multiselect(
        "Select what you want to know:",
        [
            "Approach Explanation",
            "Time Complexity",
            "Language Detection",
            "Suggest Better Code",
            "Suggest Better Approach"
        ]
    )

    user_code = st.text_area("Paste your code below:")

    if st.button("Analyze Code"):
        if not re.search(r"(def |class |#include|public |System\.|function )", user_code):
            st.error("❌ Please paste only code (no plain text).")
        elif not analysis_options:
            st.warning("⚠️ Please select at least one analysis option.")
        else:
            analysis_tasks = ", ".join(analysis_options)
            prompt = f"""
            You are a coding expert. Analyze the following code:
            {user_code}

            The user wants to know: {analysis_tasks}.
            Provide concise and accurate analysis.
            """
            with st.spinner("Analyzing your code..."):
                response = model.invoke(prompt)
            st.success("✅ Analysis Complete:")
            st.write(response.content)

#  Code Generator Section

  
elif option == "⚙️ Code Generator":
    st.subheader("Generate Code for a Topic")

    topic = st.text_input("Enter the topic or problem statement:")
    lang = st.selectbox("Select programming language:", ["Python", "C++", "Java", "JavaScript", "Go", "Rust"])
    complexity = st.selectbox("Include time complexity?", ["Yes", "No"])
    approach = st.selectbox("Select approach type:", ["Optimal", "Brute Force"])

if st.button("Generate Code"):
    if not topic.strip():
        st.warning("⚠️ Please enter a topic or problem statement.")
    elif not lang:
        st.warning("⚠️ Please select a programming language.")
    else:
        validation_prompt = f"""
        You are a classifier that determines if an input describes a programming problem or concept.
        Input: "{topic}"
        Respond strictly with only one word: YES or NO.
        """

        with st.spinner("Analyzing input..."):
            decision = model.invoke(validation_prompt).content.strip().lower()

        if "no" in decision and "yes" not in decision:
            st.error(f"❌ No result found for '{topic}'. Please enter a valid programming topic.")
        elif "yes" in decision:
            prompt = f"""
            You are an expert software engineer.
            Generate {approach.lower()} {lang} code for the topic: "{topic}".
            {'Also explain its time complexity.' if complexity == 'Yes' else ''}
            Include comments for clarity and maintain clean code structure.
            """

            with st.spinner("Generating code..."):
                response = model.invoke(prompt)

            st.success("✅ Code Generated Successfully:")
            st.code(response.content, language=lang.lower())
        else:
            st.warning("⚠️ Could not determine if topic is valid. Please try again.")
