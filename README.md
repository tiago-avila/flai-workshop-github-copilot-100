# Mergington High School Activities Sign-Up System

<img src="https://octodex.github.com/images/Professortocat_v2.png" align="right" height="200px" />

A modern web application that allows students of Mergington High School to browse and sign up for extracurricular activities. Built with FastAPI backend and vanilla JavaScript frontend.

## 🎓 Features

- **Browse Activities**: View all available extracurricular activities with detailed information
- **Real-time Availability**: See current enrollment numbers and available spots
- **Smart Sign-Up**: Register for activities with email validation (@mergington.edu only)
- **Duplicate Prevention**: Automatically prevents signing up for the same activity twice
- **Capacity Management**: Full activities are automatically disabled for new sign-ups
- **Responsive Design**: Beautiful gradient UI that works on desktop and mobile devices
- **Email Validation**: Real-time validation ensures only school email addresses are accepted
- **Confirmation Dialogs**: Prevents accidental sign-ups with confirmation prompts

## 📋 Available Activities

- **Chess Club** - Learn strategies and compete in tournaments
- **Programming Class** - Build software projects and learn coding
- **Gym Class** - Physical education and sports activities
- **Drama Club** - Theater performances and acting workshops
- **Debate Team** - Develop critical thinking and public speaking
- **Art Club** - Explore painting, drawing, and sculpture

## 🚀 Getting Started

### Prerequisites

- Python 3.13 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/tiago-avila/flai-workshop-github-copilot-100.git
cd flai-workshop-github-copilot-100
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install 'pydantic[email]'
```

### Running the Application

1. Start the server:
```bash
cd src
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

The application will automatically reload when you make changes to the code.

## 🧪 Running Tests

Run the test suite with pytest:
```bash
pytest tests/ -v
```

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Server**: Uvicorn ASGI server
- **Validation**: Pydantic with email validation
- **Testing**: pytest with FastAPI TestClient

## 📁 Project Structure

```
flai-workshop-github-copilot-100/
├── src/
│   ├── app.py              # FastAPI backend application
│   └── static/
│       ├── index.html      # Main HTML page
│       ├── app.js          # Frontend JavaScript
│       └── styles.css      # Styling
├── tests/
│   └── test_app.py         # Unit tests
├── requirements.txt        # Python dependencies
├── pytest.ini             # Pytest configuration
└── README.md              # This file
```

## 🔌 API Endpoints

### GET `/activities`
Returns all available activities with their details.

### POST `/activities/{activity_name}/signup`
Sign up a student for an activity.
- **Body**: `{"email": "student@mergington.edu"}`
- **Validations**: Mergington email, no duplicates, capacity check

### DELETE `/activities/{activity_name}/signup`
Cancel a student's sign-up for an activity.
- **Query Param**: `email=student@mergington.edu`

## 🎨 Features Implemented with GitHub Copilot

This project was enhanced using various GitHub Copilot features including:
- Code generation and completion
- Test creation
- Documentation writing
- Error handling improvements
- API endpoint development

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

