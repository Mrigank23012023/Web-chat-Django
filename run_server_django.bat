@echo off
echo Starting Knowledge Agent (Django)...
echo Activating Virtual Environment (.venv_py311)...
call .venv_py311\Scripts\activate.bat

echo Open your browser at http://127.0.0.1:8000/
python manage.py runserver
pause
