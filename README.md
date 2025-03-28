# Quiz Master Project Documentation

## Author
- **Name** – Shikhar Singh 
- **Roll No.** – 23F2003771 
- **Email** - 23f2003771@ds.study.iitm.ac.in 
- **About Me** - I use data to build meaningful applications and make smart decisions. With a background in Mathematics and Computer Applications, I have a strong passion for coding. I'm skilled in Python, web development, and machine learning. 

## Description
The Quiz Master project is designed to create an interactive web application for quiz management and participation. It provides a platform for administrators to create and manage quizzes on various subjects, while allowing regular users to take quizzes, track their performance history, and view analytics. The system facilitates knowledge assessment through structured subjects, chapters, and well-organized quizzes.

## Requirements and Setup

### Prerequisites
- Python 3.8 or higher
- Pip (Python package manager)

### Dependencies
- Flask
- Flask-SQLAlchemy
- Matplotlib
- Jinja2

## Technologies Used
- **Flask**: Python web framework for building the application
- **Flask-SQLAlchemy**: ORM extension for database operations
- **Matplotlib**: Library for generating data visualizations
- **HTML5/CSS3**: Frontend structure and styling
- **Bootstrap**: CSS framework for responsive design
- **Jinja2**: Templating engine for dynamic HTML rendering
- **SQLite**: Lightweight database engine

## DB Schema Design

### Users_Info
- `id` (Integer, PK): Unique identifier for each user
- `username` (String, Unique): Email address used for login
- `password` (String): User's password
- `fullname` (String): User's full name
- `qualifications` (String): Educational background
- `dob` (Date): Date of birth

### Subjects
- `Subject_code` (Integer, PK): Unique identifier for each subject
- `subject_name` (String): Name of the subject
- `subject_description` (String): Detailed description of the subject

### Chapter
- `chapter_id` (Integer, PK): Unique identifier for each chapter
- `chapter_name` (String): Name of the chapter
- `chapter_description` (String): Description of the chapter content
- `subject_code_chapter` (Integer, FK to Subjects): Associates chapter with a subject

### Quiz
- `id` (Integer, PK): Unique identifier for each quiz
- `date_of_quiz` (Date): Scheduled date for the quiz
- `time_duration` (Time): Allocated time for completion
- `chapter_id` (Integer, FK to Chapter): Associates quiz with a chapter

### Questions
- `id` (Integer, PK): Unique identifier for each question
- `chapter_id` (Integer): Related chapter ID
- `question_title` (String): Brief title for the question
- `question_statement` (String): Full question text
- `option1`, `option2`, `option3`, `option4` (String): Multiple choice options
- `correct_answer` (String): The correct option
- `quiz_id` (Integer, FK to Quiz): Associates question with a quiz

### Scores
- `id` (Integer, PK): Unique identifier for each score record
- `user_id` (Integer, FK to Users_Info): User who attempted the quiz
- `quiz_id` (Integer, FK to Quiz): Quiz that was attempted
- `time_stamp_of_attempt` (DateTime): When the quiz was taken
- `score` (Integer): Points earned in the quiz

### Design Rationale:
The database is designed with a hierarchical structure (Subject → Chapter → Quiz → Question) to enable organized content management. Foreign key relationships ensure data integrity across the system. The separation of Scores from Questions allows for efficient tracking of multiple attempts by different users on the same quiz without data duplication.

## Architecture and Features

### Architecture Organization:
The Quiz Master project follows a Model-View-Controller (MVC) architecture:
- **Models**: Located in `models.py`, define database tables and relationships using SQLAlchemy ORM
- **Controllers**: Found in `controllers.py`, contain route handlers and business logic
- **Templates**: HTML files in the `templates/` directory provide the UI using Jinja2
- **Static Files**: CSS, JavaScript, and generated charts reside in the `static/` folder
- **App Configuration**: `app.py` initializes the Flask application and database

The project maintains a clear separation of concerns, with models handling data structures, controllers managing application logic, and templates focusing on presentation. This organization facilitates maintenance and future enhancements.

### Features Implemented:

#### Default Features:
1. **Authentication System**: Registration, login, and session management to control access based on user roles
2. **Subject and Chapter Management**: Admins can create, update, and organize educational content hierarchically
3. **Quiz Creation and Management**: Interface for building quizzes with multiple-choice questions
4. **Quiz Taking Interface**: User-friendly form for attempting quizzes with immediate scoring
5. **Quiz History**: Persistent storage and display of all quiz attempts and scores
6. **Search Functionality**: Dynamic search across subjects, chapters, and quizzes
7. **Analytics**: Visual data representations showing performance and participation trends

The features are implemented using Flask's routing system to handle HTTP requests, SQLAlchemy for database operations, and Matplotlib for generating custom analytics visualizations that help users understand their performance patterns.