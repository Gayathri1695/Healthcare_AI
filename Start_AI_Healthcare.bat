@echo off
echo Starting AI Healthcare Server...
cd "c:\Users\gayas\Downloads\project CC\healthcare_ai"
start http://127.0.0.1:8080/
.\venv\Scripts\python.exe manage.py runserver 8080
