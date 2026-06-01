import streamlit as st
import requests
import json

be_url = st.secrets[be_url_server]
st.title("AI Interview Helper Bot")

with st.form("Details"):
    topic = st.text_input("Enter lang-topic:--")
    level = st.selectbox("Select level", ["Beginner", "Intermediate", "Advanced"])
    question_type = st.multiselect("choose any of below",["MCQs","Theory Questions","Coding Questions"])
    submit = st.form_submit_button("Generate")

if submit:
    prompt = f"""
        Generate exactly 10 {level} interview questions on {topic}.

        Selected Types: {question_type}

        IMPORTANT:

        If Question Type contains MCQS, every question MUST be:

        {{
            "type":"MCQS",
            "question":"What is Python?",
            "options":[
                "A. Operating System",
                "B. Programming Language",
                "C. Database",
                "D. Browser"
            ],
            "answer":"B. Programming Language"
        }}

        If Question Type contains Coding:

        {{
            "type":"Coding",
            "question":"Write a Python program to reverse a string",
            "answer":"def reverse(s): return s[::-1]"
        }}

        If Question Type contains Theory:

        {{
            "type":"Theory",
            "question":"What is Python?",
            "answer":"Python is ..."
        }}


        Return ONLY a JSON array of objects:

        [
        {{
            "question": "What is Python?",
            "answer": "Python is a high-level programming language..."
        }}
        ]

        Rules:
        - No markdown
        - No explanation
        - Only valid JSON
        """

    response =requests.post(f"{be_url}/generate_questions", json={"prompt": prompt})
    st.write("Status:", response.status_code)
    res = response.json()
    st.session_state.questions = json.loads(res["object"])

if "questions" in st.session_state:
    st.subheader("Interview Q&A")

    for i, item in enumerate(st.session_state.questions):
        qtype = item.get("type", "Theory")

        with st.expander(f"{qtype} Q{i}: {item['question']}"):

            # MCQ Questions
            if qtype == "MCQS":

                st.radio(
                    "Choose an option:",
                    item.get("options", []),
                    key=f"mcq_{i}"
                )

                if st.button("Show Answer", key=f"answer_{i}"):
                    st.success(item["answer"])

        # Coding Questions
            elif qtype == "Coding":

                st.write("### Solution")
                st.code(item["answer"], language="python")

            # Theory Questions
            else:
                st.write(item["answer"])
