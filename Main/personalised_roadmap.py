import streamlit as st
import google.generativeai as genai

# Configure the Google Generative AI API
api_key = "AIzaSyAxPJTpSHwA2Ng-rZ7FPXyUuhXc8Jgs_nE"
genai.configure(api_key=api_key)
gemini_model = genai.GenerativeModel("gemini-pro")

def generate_result():
    # Access user input from Streamlit widgets
    graduated = st.radio("Have you graduated?", (0, 1), format_func=lambda x: "%d - No" % x if x == 0 else "%d - Yes" % x)
    job = ""  # Initialize job with an empty string
    target_job = ""  # Initialize target_job with an empty string
    if graduated == 1:
        job = st.text_input("What job role are you currently involved in?").lower()
        target_job = st.text_input("What job are you targeting for?").lower()
    else:
        year = st.slider("Which year are you currently studying in?", 1, 4, 1)
    branch = st.text_input("Which branch have you graduated from or will you graduate from?").lower()
    subject = st.text_input("What topic are you searching for?").lower()
    exam = st.radio("Are you targeting any exam?", (0, 1), format_func=lambda x: "%d - No" % x if x == 0 else "%d - Yes" % x)
    exam_name = ""  # Initialize exam_name with an empty string
    if exam == 1:
        exam_name = st.text_input("Enter the exam you are targeting:").lower()
    time = st.slider("Enter the time you want the workshop for in months:", 1, 12, 1)

    # Build the prompt template
    prompt_template = "{graduated_condition}{year_condition}{subject_condition}{exam_condition}{time_condition}"

    # Create the prompt with user inputs
    prompt = prompt_template.format(
        graduated_condition=graduated_condition(graduated, job, branch, target_job),
        year_condition=year_condition(graduated, year, branch),
        subject_condition=subject_condition(subject),
        exam_condition=exam_condition(exam, exam_name),
        time_condition=time_condition(time),
    )

    # Generate the result using the Gemini model
    result = gemini_model.generate_content(prompt)

    st.markdown("## Personalized Roadmap:")
    st.write(result.text)

def graduated_condition(graduated, job, branch, target_job):
    if graduated == 1:
        return f"Give me a very personalized roadmap as I am a graduate working in {job} with a degree in {branch} aiming for {target_job}."
    else:
        return f"Give me a very personalized roadmap as I am studying in {branch}."

def year_condition(graduated, year, branch):
    if graduated == 0:
        return f" and studying in {year} year of {branch}"
    else:
        return ""

def subject_condition(subject):
    return f" for the topic {subject}"

def exam_condition(exam, exam_name):
    if exam == 1:
        return f" targeting the {exam_name} exam"
    else:
        return ""

def time_condition(time):
    return f" with a duration of {time} months."

if __name__ == "__main__":
    st.title("Personalized Roadmap")
    generate_result()