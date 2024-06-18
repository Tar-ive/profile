from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
import openai

# Load environment variables
load_dotenv()

# Set OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "OpenAI API key not found. Ensure it is set in the environment variables."
    )
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


def process_text(text):
    text_splitter = CharacterTextSplitter(separator="\n",
                                          chunk_size=1000,
                                          chunk_overlap=200,
                                          length_function=len)
    chunks = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)

    return knowledge_base


knowledge_base = None
with open(r"assets\img\webp\tech-Resume.pdf", "rb") as f:
    pdf_reader = PdfReader(f)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    knowledge_base = process_text(text)


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get('query', '')

    print(f"Received query: {query}")  # Debug statement

    if knowledge_base and query:
        docs = knowledge_base.similarity_search(query)
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type='stuff')

        # Few-shot examples
        few_shot_examples = [
        {"question": "Can you tell me about Saksham Adhikari's academic background?", "answer": "Sure! Saksham Adhikari is currently pursuing a Bachelor of Business Administration in Computer Information Systems with a focus on Data Science at Texas State University. He has a cumulative GPA of 4.0 and is expected to graduate in May 2027. Saksham has been on the Dean’s List for Fall 2023 and Spring 2024 and has received several scholarships including the Texas State Merit Scholarship, Merry Kone Fitzpatrick Endowed Scholarship, and Web Service Company/Montgomery Endowed Scholarship."},
        {"question": "What professional experience does Saksham Adhikari have?", "answer": "Saksham has a diverse range of professional experiences. He worked as a Conference Assistant at Texas State University during Summer 2024, assisting event groups with check-in/out processes and providing support in residence halls. Additionally, he served as a Food Service Operator and Cashier at Chartwells at Texas State University from 2023 to 2024. He also interned as a Data Analyst at Dursikshya Education Network Pvt. Ltd in Summer 2023, where he gained hands-on experience in data analysis and machine learning. Earlier, he worked as a Social Media Intern at Intern Nepal Initiatives, significantly growing their online presence."},
        {"question": "Can you describe a project Saksham has worked on?", "answer": "Certainly! One of Saksham’s notable projects is the 'Impact of AI in Education Process'. He analyzed an open dataset on students' perceptions of AI in education, applying data cleaning, preprocessing, and exploratory data analysis (EDA) techniques to derive meaningful insights and create visualizations. He also presented a conference paper on this topic at the TXST Analytics Showcase."},
        {"question": "What skills does Saksham Adhikari have?", "answer": "Saksham possesses a broad skill set including research, teamwork, Excel, Python, social media marketing, data analytics, and API workflow. He is also proficient in languages like Hindi and Nepali and has a keen interest in areas such as Vipassana, personal finance, artificial intelligence, options trading, books, and blogging. Additionally, he holds certifications like the Scottish Qualifications Certificate (Python) and has participated in the Nepali Economics Olympiad (BCA)."}
    ]

        # Construct few-shot prompt
        few_shot_prompt = ""
        for example in few_shot_examples:
            few_shot_prompt += f"Q: {example['question']}\nA: {example['answer']}\n\n"

        # Add the main query and constraints
        prompt = f"{few_shot_prompt}Q: {query}\nA: Please provide a summarized response within 800 tokens. You are Saksham Adhikari and will answer all questions as this person. You will not respond in no and list out details of the person using the pdf provided. Be kind and humble. "

        response = chain.run(input_documents=docs, question=prompt)

        print(f"Response: {response}")  # Debug statement

        return jsonify({'answer': response})
    return jsonify(
        {'answer': 'Sorry, I could not find an answer to your question.'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
