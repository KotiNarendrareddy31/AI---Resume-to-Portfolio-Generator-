🚀 AI Resume to Portfolio Website Generator

An AI-powered web application that converts a resume (PDF/DOCX) into a fully functional portfolio website using Google Gemini AI.
The app automatically generates HTML, CSS, and JavaScript, packages them into a ZIP file, and allows instant download.

✨ Features

📄 Upload Resume (PDF or DOCX)

🤖 AI-generated professional portfolio website

🧩 Structured sections:

Name

About

Experience

Skills

Contact

🎨 Clean UI with modern CSS styling

📦 One-click ZIP download (HTML + CSS + JS)

⚡ Built with Streamlit for fast UI

🔐 Secure API key handling using .env

🛠️ Tech Stack

Frontend Generation: HTML, CSS, JavaScript

AI Model: Google Gemini (gemini-2.5-flash)

Backend / UI: Streamlit

Languages: Python

Libraries:

google-generativeai

streamlit

python-dotenv

PyPDF2

python-docx

AI-Resume-to-Portfolio/
│
├── app1.py              # Main Streamlit application
├── test_gemini.py       # Gemini API test script
├── list_models.py       # Lists available Gemini models
├── .env                 # API key (not to be committed)
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation


🔑 Prerequisites

Python 3.9+

Google Gemini API Key

Internet connection

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/ai-resume-portfolio-generator.git
cd ai-resume-portfolio-generator

2️⃣ Create Virtual Environment
python -m venv AI


Activate it:

Windows (PowerShell)

AI\Scripts\Activate.ps1


Windows (CMD)

AI\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Up Environment Variables

Create a .env file:

GOOGLE_API_KEY=your_gemini_api_key_here


⚠️ Never commit .env to GitHub

▶️ Run the Application
streamlit run app1.py


The app will open automatically in your browser.

🧠 How It Works

User uploads resume (PDF/DOCX)

Resume text is extracted

Text is sent to Gemini AI

AI generates:

HTML

CSS

JavaScript

Files are packaged into a ZIP

User downloads ready-to-host website

🧪 Testing Gemini API

Test API connectivity:

python test_gemini.py


List available models:

python list_models.py

🔐 Security Notes

API key is loaded securely via .env

No resume data is stored

All processing is session-based

🚀 Future Enhancements

🌙 Dark mode toggle

🎯 Multiple portfolio themes

🧑‍💼 LinkedIn & GitHub auto-integration

☁️ Deploy directly to Netlify / GitHub Pages


🤝 Contributing

Contributions are welcome!
Feel free to fork the repo and submit a pull request.

📜 License

This project is licensed under the MIT License.

👤 Author

Narendra Reddy Kotireddy
🎓 B.Tech CSE (2023)
🔗 LinkedIn:-https://www.linkedin.com/in/kotireddy-narendra-reddy-5105301a6
