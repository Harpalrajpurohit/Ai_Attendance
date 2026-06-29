# 🎓 AI Attendance System

An AI-powered attendance management system that automatically recognizes registered students using computer vision and marks their attendance.

> Built using **Python**, **OpenCV**, and **face recognition** libraries.

---

# 📌 Features

- ✅ Automatic face detection
- ✅ Face recognition of registered students
- ✅ Real-time webcam attendance
- ✅ Automatic CSV attendance generation
- ✅ Student database using JSON
- ✅ Simple and lightweight interface

---

# 🛠 Tech Stack

- Python 3
- OpenCV
- face_recognition
- NumPy
- JSON
- CSV

---

# 📂 Project Structure
Ai_Attendance/
│
├── apps.py                 # Main application
├── students_db.json        # Student database
├── Images/                 # Training images (ignored in GitHub)
├── Imagess/                # Screenshots for README
├── .gitignore
└── README.md
---

# 🚀 Installation

Clone the repository

->bash
git clone https://github.com/Harpalrajpurohit/Ai_Attendance.git

# Move into the project folder
cd Ai_Attendance

# Create virtual environment
python3 -m venv .venv

# Activate environment for-macOS/Linux
source .venv/bin/activate
 # windows
 .venv\Scripts\activate

 # Install dependencies
 pip install -r requirements.txt

 # Run the project
python apps.py
