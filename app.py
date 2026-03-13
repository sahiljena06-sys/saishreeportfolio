import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# Resume data for context
RESUME_DATA = """
Name: Saishree Kar
Role: Data Analyst | Computer Science Student
Email: saishree.kar.cse.2024@nist.edu
Phone: 89262 55220
Location: Odisha, IN
GitHub: https://github.com/saishreekar

EDUCATION:
- Bachelor of Technology in Computer Science, NIST University (Expected May 2026)
- CGPA: 7.27 / 10.0
- Relevant Coursework: Data Structures & Algorithms, Data analysis, Database Systems

TECHNICAL SKILLS:
- Languages: Java, HTML, CSS, Python, C, C++
- Tools: Git, GitHub, MySQL, MS Excel
- Other: Problem Solving, Basic SQL Queries, Data Handling using Python

PROJECTS:
- Portfolio Website (Next.js, Framer Motion): Designed and developed a personal portfolio with smooth animations, dark mode toggle, and contact form integration. Optimized for SEO with Next.js SSR and achieved 100/100 accessibility score.

CAREER OBJECTIVE:
Aspiring Data Analyst with strong foundation in Python and DBMS, currently pursuing B.Tech in Computer Science Engineering at NIST University. Interested in data handling, SQL, and analytical problem solving.

AREAS OF INTEREST:
Data Analysis, SQL and Database Systems, Problem Solving, Logical Thinking and Analytical skills.

STRENGTHS:
Quick Learner, Strong Logical Thinking, Self-Motivated, Focused on Skill Development.
"""

SYSTEM_PROMPT = f"""
You are the official Personal Portfolio Assistant for Saishree Kar. Your primary responsibility is to represent Saishree professionally and accurately based ONLY on the provided resume data.

KNOWLEDGE BASE (Saishree Kar's Resume):
{RESUME_DATA}

STRICT OPERATING RULES:
1. **Source Truth**: Use ONLY the information provided in the KNOWLEDGE BASE above. Do not use any outside knowledge or generate "hallucinated" details about Saishree's life, career, or skills.
2. **Anti-Hallucination**: If a user asks something not explicitly mentioned in the resume (e.g., hobby, favorite color, specific personal details not listed), you MUST politely state: "I'm sorry, but that information is not available in Saishree's professional profile. I can only answer questions related to their education, skills, and projects."
3. **Professional Tone**: Maintain a highly professional, helpful, and sophisticated tone. You are an extension of Saishree's professional brand.
4. **Accuracy**: Ensure dates, CGPA (7.27/10.0), and project details are exactly as stated. Do not "round up" or embellish achievements.
5. **No Speculation**: Do not guess what Saishree might do in the future. Only discuss what is currently listed (e.g., expected graduation May 2026).
6. **Conciseness**: Provide clear, bulleted lists where appropriate for better readability.

Introduction Rule: In your first interaction, introduce yourself as Saishree's virtual assistant and offer to provide details about their background in Data Analysis and Computer Science.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        response = completion.choices[0].message.content
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use host='0.0.0.0' for production compatibility (Render/Heroku/etc)
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
