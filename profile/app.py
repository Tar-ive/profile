import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
import openai

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()

# Set OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Ensure it is set in the environment variables.")
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return "Hello, this is Saksham's Flask app!"

def process_text(text):
    # Check if the text is being processed
    if not text:
        raise ValueError("No text provided for processing.")
    
    # Split the text into chunks
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = text_splitter.split_text(text)
    
    # Debugging statement to check the chunks
    print(f"Chunks: {chunks}")
    
    # Check if chunks are created
    if not chunks:
        raise ValueError("Text splitting resulted in no chunks.")
    
    # Create embeddings
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    
    return knowledge_base

knowledge_base = None
text_files = ["tech-Resume.txt", "saksham.txt"]

combined_text = ""

for text_file in text_files:
    logging.debug(f"Current working directory: {os.getcwd()}")
    logging.debug(f"Files in current directory: {os.listdir('.')}")
    logging.debug(f"Checking text file path: {text_file}")

    if not os.path.exists(text_file):
        logging.error(f"Text file not found at {text_file}")
        raise ValueError(f"Text file not found at {text_file}")

    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read()
        combined_text += text + "\n"

# Debugging statement to check if text is extracted
logging.debug(f"Extracted text: {combined_text}")

if not combined_text:
    raise ValueError("Failed to extract text from text files.")
    
knowledge_base = process_text(combined_text)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get('query', '').strip().lower()

    print(f"Received query: {query}")  # Debug statement

    qualifications_query = [
        "what are your qualifications?",
        "can you tell me your qualifications?",
        "what is your qualification?",
        "tell me about your qualifications"
    ]

    greetings_query = [
        "hi", "hello", "hey", "how are you", "how are you doing"
    ]

    general_query = [
        "what is this?", "who are you?", "what can you do?"
    ]

    thanks_query = [
        "thanks", "thank you", "thx", "ty", "Thank You", "Thankyou"
    ]

    bye_query = [
        "bye", "goodbye", "see you", "later", "Thank you, Bye" 
    ]

    okay_query = [
        "okay", "ok", "alright", "Okay" "Ok", "Great", "Wow"
    ]

    if query in qualifications_query:
        qualifications = {
            "academic_background": "Saksham Adhikari is currently pursuing a Bachelor of Business Administration in Computer Information Systems with a focus on Data Science at Texas State University. He has a cumulative GPA of 4.0 and is expected to graduate in May 2027. Saksham has been on the Dean’s List for Fall 2023 and Spring 2024 and has received several scholarships including the Texas State Merit Scholarship, Merry Kone Fitzpatrick Endowed Scholarship, and Web Service Company/Montgomery Endowed Scholarship.",
            "professional_experience": "Saksham has a diverse range of professional experiences. He worked as a Conference Assistant at Texas State University during Summer 2024, assisting event groups with check-in/out processes and providing support in residence halls. Additionally, he served as a Food Service Operator and Cashier at Chartwells at Texas State University from 2023 to 2024. He also interned as a Data Analyst at Dursikshya Education Network Pvt. Ltd in Summer 2023, where he gained hands-on experience in data analysis and machine learning. Earlier, he worked as a Social Media Intern at Intern Nepal Initiatives, significantly growing their online presence.",
            "projects": "One of Saksham’s notable projects is the 'Impact of AI in Education Process'. He analyzed an open dataset on students' perceptions of AI in education, applying data cleaning, preprocessing, and exploratory data analysis (EDA) techniques to derive meaningful insights and create visualizations. He also presented a conference paper on this topic at the TXST Analytics Showcase.",
            "skills": "Saksham possesses a broad skill set including research, teamwork, Excel, Python, social media marketing, data analytics, and API workflow. He is also proficient in languages like Hindi and Nepali and has a keen interest in areas such as Vipassana, personal finance, artificial intelligence, options trading, books, and blogging. Additionally, he holds certifications like the Scottish Qualifications Certificate (Python) and has participated in the Nepali Economics Olympiad (BCA)."
        }

        response = f"Academic Background: {qualifications['academic_background']}\n\nProfessional Experience: {qualifications['professional_experience']}\n\nProjects: {qualifications['projects']}\n\nSkills: {qualifications['skills']}"
        return jsonify({'answer': response})

    elif query in greetings_query:
        response = "Hi! Welcome to Saksham's chatbot. How can I assist you today?"
        return jsonify({'answer': response})

    elif query in general_query:
        response = "This is Saksham's chatbot. I can answer questions about Saksham's qualifications, experiences, and projects. How can I help you today?"
        return jsonify({'answer': response})

    elif query in thanks_query:
        response = "You're welcome! Is there anything else I can help you with?"
        return jsonify({'answer': response})

    elif query in bye_query:
        response = "Goodbye! Have a great day!"
        return jsonify({'answer': response})

    elif query in okay_query:
        response = "Alright. Is there anything else you need?"
        return jsonify({'answer': response})

    if knowledge_base and query:
        docs = knowledge_base.similarity_search(query)
        llm = OpenAI(model="gpt-3.5-turbo-instruct")
        chain = load_qa_chain(llm, chain_type='stuff')

        # Few-shot examples
        few_shot_examples = [
            {"question": "Can you tell me about Saksham Adhikari's academic background?", "answer": "Sure! Saksham Adhikari is currently pursuing a Bachelor of Business Administration in Computer Information Systems with a focus on Data Science at Texas State University. He has a cumulative GPA of 4.0 and is expected to graduate in May 2027. Saksham has been on the Dean’s List for Fall 2023 and Spring 2024 and has received several scholarships including the Texas State Merit Scholarship, Merry Kone Fitzpatrick Endowed Scholarship, and Web Service Company/Montgomery Endowed Scholarship."},
            {"question": "What professional experience does Saksham Adhikari have?", "answer": "Saksham has a diverse range of professional experiences. He worked as a Conference Assistant at Texas State University during Summer 2024, assisting event groups with check-in/out processes and providing support in residence halls. He also interned as a Data Analyst at Dursikshya Education Network Pvt. Ltd in Summer 2023, where he gained hands-on experience in data analysis and machine learning. Earlier, he worked as a Social Media Intern at Intern Nepal Initiatives, significantly growing their online presence."},
            {"question": "Can you describe a project Saksham has worked on?", "answer": "Certainly! One of Saksham’s notable projects is the his Stock Anomolies Detection Algorithm and AI Finance Researcher. He has created an LSTM encoder and Isolation Forest Model which predicts anomolies and an AI finance researcher which finds news if any realted to these anomolies. Then Saksham can get notifications on his phone if there are any anomolies. "},
            {"question": "What skills does Saksham Adhikari have?", "answer": "Saksham possesses a broad skill set including research, teamwork, Excel, Python, social media marketing, data analytics, and API workflow. He is also proficient in languages like Hindi and Nepali and has a keen interest in areas such as Vipassana, personal finance, artificial intelligence, options trading, books, and blogging. Additionally, he holds certifications like the Scottish Qualifications Certificate (Python) and has participated in the Nepali Economics Olympiad (BCA)."}
        ]

        # Construct few-shot prompt
        few_shot_prompt = ""
        for example in few_shot_examples:
            few_shot_prompt += f"Q: {example['question']}\nA: {example['answer']}\n\n"

        # Add the main query and constraints
        prompt = f"{few_shot_prompt}Q: {query}\nA: Please provide a summarized response within 800 tokens. You are Saksham Adhikari and will answer all questions as this person. You will not respond in no and list out details of the person using the pdf provided. Be kind and humble."

        system_prompt = "You are Saksham Adhikari. Answer all questions as if you are Saksham Adhikari. Be kind and humble. "

        response = chain.run(input_documents=docs, question=system_prompt + prompt)

        if not response:
            response = "How about you ask that Saksham directly by emailing him at adhsaksham27@gmail.com"

        print(f"Response: {response}")  # Debug statement

        return jsonify({'answer': response})

    return jsonify({'answer': 'How about you ask that Saksham directly by emailing him at adhsaksham27@gmail.com'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
