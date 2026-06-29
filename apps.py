import streamlit as st
import cv2
import os
import face_recognition
import numpy as np
import pandas as pd
from datetime import datetime
from PIL import Image, ImageOps

# 1. Page Configuration
st.set_page_config(page_title="JUSST IN COLLEGE", layout="wide", page_icon="🎓")

# 2. Updated Student Data (Aapka original data)
STUDENTS = {
    "devkumar": {"Roll": "23SE02ML101", "Program": "B.Tech - ML (Sem 5)", "Image": "devkumar.JPG"},
    "harpal": {"Roll": "23SE02ML150", "Program": "B.Tech - ML (Sem 5)", "Image": "harpal.jpg"},
    "jay": {"Roll": "23SE02ML102", "Program": "B.Tech - ML (Sem 5)", "Image": "jay.jpg"},
    "deshmi": {"Roll": "23SE02ML103", "Program": "B.Tech - ML (Sem 5)", "Image": "deshmi.JPG"},
    "isha": {"Roll": "23SE02ML104", "Program": "B.Tech - ML (Sem 5)", "Image": "isha.jpg"},
    "varshita": {"Roll": "23SE02ML105", "Program": "B.Tech - ML (Sem 5)", "Image": "varshita.jpg"},
}

DATASET_PATH = "Images"
today = datetime.now().strftime("%Y-%m-%d")
CSV_FILE = f"attendance_{today}.csv"

# 3. Custom CSS for Premium Look
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }

    /* Glassmorphism Cards */
    .student-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        text-align: center;
        margin-bottom: 20px;
    }

    /* Professional Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
    }

    /* Metrics Background */
    [data-testid="stMetricValue"] {
        color: #818cf8;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Functions (Original Logic)
@st.cache_resource
def load_known_faces(dataset_path):
    encodings, names = [], []
    for student, info in STUDENTS.items():
        path = os.path.join(dataset_path, info["Image"])
        if os.path.exists(path):
            img = face_recognition.load_image_file(path)
            enc = face_recognition.face_encodings(img)
            if enc:
                encodings.append(enc[0])
                names.append(student)
    return encodings, names

def mark_attendance(name):
    if not os.path.exists(CSV_FILE):
        pd.DataFrame(columns=["Name", "Date", "Time"]).to_csv(CSV_FILE, index=False)
    df = pd.read_csv(CSV_FILE)
    if name.title() not in df["Name"].values:
        now = datetime.now()
        new_entry = pd.DataFrame([[name.title(), now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")]],
                                 columns=["Name","Date","Time"])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        return True
    return False

# 5. Sidebar - Stats and Info
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3429/3429433.png", width=100)
    st.title("Admin Panel")
    st.markdown("---")
    
    # Stats
    df_count = pd.read_csv(CSV_FILE) if os.path.exists(CSV_FILE) else pd.DataFrame()
    st.metric("Total Registered", len(STUDENTS))
    st.metric("Present Today", len(df_count))
    
    st.markdown("---")
    if st.button("🗑️ Reset Attendance"):
        if os.path.exists(CSV_FILE): os.remove(CSV_FILE)
        st.rerun()

# 6. Main Dashboard Header
st.markdown("<h1 style='text-align: center; color: white;'>🎓 JUST IN COLLEGE</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #94a3b8;'>Smart Attendance System | {today}</p>", unsafe_allow_html=True)
st.markdown("---")

# 7. Main Logic Split
col_cam, col_info = st.columns([2, 1])

if "recognized_student" not in st.session_state:
    st.session_state.recognized_student = None

with col_cam:
    st.subheader("📸 Live Security Feed")
    if not st.session_state.recognized_student:
        start_btn = st.button("🚀 Start Scanning")
        frame_placeholder = st.empty()
        
        if start_btn:
            known_encodings, known_names = load_known_faces(DATASET_PATH)
            cap = cv2.VideoCapture(0)
            
            while True:
                ret, frame = cap.read()
                if not ret: break
                
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                faces = face_recognition.face_locations(rgb)
                encs = face_recognition.face_encodings(rgb, faces)
                
                for (top, right, bottom, left), enc in zip(faces, encs):
                    # Draw visual box on frame
                    cv2.rectangle(rgb, (left, top), (right, bottom), (99, 102, 241), 2)
                    
                    matches = face_recognition.compare_faces(known_encodings, enc, tolerance=0.45)
                    if True in matches:
                        name = known_names[matches.index(True)]
                        mark_attendance(name)
                        st.session_state.recognized_student = name
                        cap.release()
                        st.rerun()
                
                frame_placeholder.image(rgb, channels="RGB", use_container_width=True)
            cap.release()
    else:
        st.info("✅ Scan Complete. Profile loaded.")
        if st.button("🔄 Scan Next Student"):
            st.session_state.recognized_student = None
            st.rerun()

with col_info:
    st.subheader("👤 Student Profile")
    if st.session_state.recognized_student:
        name = st.session_state.recognized_student
        info = STUDENTS.get(name, {})
        img_path = os.path.join(DATASET_PATH, info.get("Image",""))
        
        st.markdown(f"""
            <div class="student-card">
                <h2 style='color: #818cf8; margin-bottom: 10px;'>{name.title()}</h2>
                <p style='color: #94a3b8; font-size: 1.1em;'><b>{info.get('Roll')}</b></p>
                <hr style='border: 0.5px solid #334155'>
                <p style='text-align: left;'>📚 <b>Program:</b> {info.get('Program')}</p>
                <p style='text-align: left;'>⏰ <b>Entry Time:</b> {datetime.now().strftime('%H:%M:%S')}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if os.path.exists(img_path):
            img = Image.open(img_path)
            st.image(img, use_container_width=True)
            
        st.success(f"Attendance Recorded for {name.title()}!")
    else:
        st.write("Waiting for face detection...")
        st.image("https://cdn-icons-png.flaticon.com/512/4675/4675250.png", width=150)

# 8. Footer Table
st.markdown("---")
st.subheader("📝 Today's Logs")
if os.path.exists(CSV_FILE):
    log_df = pd.read_csv(CSV_FILE)
    st.dataframe(log_df.style.set_properties(**{'background-color': '#1e293b', 'color': 'white'}), use_container_width=True)
