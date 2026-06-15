# SecureDezy: AI-Driven Claims Management System

An intelligent claims management platform built for a final year BCA project. The application automates initial insurance claim processing and provides vision-based damage assessment using Multimodal AI, while enforcing strict regulatory compliance via human-in-the-loop verification.

## 🚀 Features
- **Multimodal AI Intake:** Real-time conversational chatbot for gathering claim details.
- **Computer Vision Analysis:** Automated damage assessment from uploaded images using Google Gemini.
- **Dynamic Domain Routing:** Custom business logic flows for both Vehicle and Home insurance.
- **Human-in-the-Loop Security:** Hardcoded adjuster verification and randomized broker mediation stages to prevent fraud.
- **Consumer Rights Portal:** Built-in escalation matrix and Ombudsman details for rejected quotes.

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Language:** Python 3.10+
- **AI Engine:** Google Gemini API (`gemini-2.5-flash`)
- **Image Processing:** Pillow (PIL)

## 📦 Installation & Setup
1. Clone the repository or download the source code files.
2. Install the required dependencies:
```bash
   pip install -r requirements.txt
