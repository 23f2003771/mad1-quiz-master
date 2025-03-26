from flask import Flask,render_template,request,redirect
from datetime import datetime, time
from .models import *
from flask import current_app as app
import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt

app.secret_key = 'secret-key'

@app.route('/',methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('username')
        pswd = request.form.get('password')
        user = Users_Info.query.filter_by(username=uname, password=pswd).first()
        if user and user.id == 1:
            return redirect('/admin_dashboard')
        elif user and user.id != 1:
            return redirect('/user_dashboard')
        else:
            return 'User not found'
    return render_template('login.html')


@app.route('/register',methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form.get('reg_uname')
        pswd = request.form.get('reg_pswd')
        fname = request.form.get('reg_fullname')
        qual = request.form.get('reg_qualifications')
        dob = request.form.get('reg_dob')
        date_dob = datetime.strptime(dob, "%Y-%m-%d").date()
        user = Users_Info(username=uname, password=pswd, fullname=fname, qualifications=qual, dob=date_dob)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('SignUp.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    chap_all = Chapter.query.all()
    chap_lst = []
    for chapters in chap_all:
        ques_count = Questions.query.filter_by(chapter_id=chapters.chapter_id).count()
        chap_lst.append({ 'c_id': chapters.chapter_id, 'sbc': chapters.subject_code_chapter, 'chap_name': chapters.chapter_name, 'ques_count': ques_count})
    sub_all = Subjects.query.all()
    sub_lst = []
    for subjects in sub_all:
        sub_lst.append({'s_code': subjects.Subject_code, 'sub_name': subjects.subject_name})
    return render_template('Admin_Dashboard.html', chap_lst=chap_lst, sub_lst=sub_lst)


@app.route('/new_subject',methods = ['GET', 'POST'])
def new_subject():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'save':
            sub_code = request.form.get('sub_code')
            sub_name = request.form.get('sub_name')
            sub_desc = request.form.get('sub_desc')
            subject = Subjects(Subject_code=sub_code, subject_name=sub_name, subject_description=sub_desc)
            db.session.add(subject)
            db.session.commit()
            return redirect('/admin_dashboard')
        elif action == 'cancel':
            return redirect('/admin_dashboard')
    return render_template('New_Subject.html')


@app.route('/new_chapter/<int:sub_code>',methods = ['GET', 'POST'])
def new_chapter(sub_code):
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'save':
            chap_id = request.form.get('chap_id')
            chap_name = request.form.get('chap_name')
            chap_desc = request.form.get('chap_desc')
            chapter = Chapter(chapter_id=chap_id,subject_code_chapter=sub_code,chapter_name=chap_name, chapter_description=chap_desc)
            db.session.add(chapter)
            db.session.commit()
            return redirect('/admin_dashboard')
        elif action == 'cancel':
            return redirect('/admin_dashboard')
    return render_template('New_Chapter.html',sub_code=sub_code)


@app.route('/edit_chapter/<int:id>',methods = ['GET', 'POST'])
def chapter_edit(id):
    chapter_edit = Chapter.query.filter_by(chapter_id=id).first()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'save':
            chap_name = request.form.get('chap_name')
            chap_desc = request.form.get('chap_desc')
            chapter = Chapter.query.filter_by(chapter_name=chap_name, chapter_description=chap_desc).first()
            chapter.chapter_name = chap_name
            chapter.chapter_description = chap_desc
            db.session.commit()
            return redirect('/admin_dashboard')
        elif action == 'cancel':
            return redirect('/admin_dashboard')
    return render_template('Edit_Chapter.html', chapter_edit=chapter_edit)


@app.route('/chapter_delete/<int:id>',methods = ['GET', 'POST'])
def chapter_delete(id):
    chapter_delete = Chapter.query.filter_by(chapter_id=id).first()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'delete':
            chap_name = request.form.get('chap_name')
            chap_desc = request.form.get('chap_desc')
            chapter = Chapter.query.filter_by(chapter_name=chap_name, chapter_description=chap_desc).first()
            ch_id = chapter.chapter_id
            quiz = Quiz.query.filter_by(chapter_id=ch_id).all()
            question = Questions.query.filter_by(chapter_id=ch_id).all()
            for ques in question:
                db.session.delete(ques)
            for qz in quiz:
                db.session.delete(qz)
            db.session.delete(chapter)
            db.session.commit()
            return redirect('/admin_dashboard')
        elif action == 'cancel':
            return redirect('/admin_dashboard')
    return render_template('Delete_Chapter.html', delete_chapter=chapter_delete)


@app.route('/quiz_management')
def quiz_management():
    quiz_all = Quiz.query.all()
    quiz_lst = []
    for quizzes in quiz_all:
        chap = Chapter.query.filter_by(chapter_id=quizzes.chapter_id).first()
        quiz_lst.append({'quiz_id': quizzes.id, 'chap_id': quizzes.chapter_id, 'chap_name': chap.chapter_name})
    questions_all = Questions.query.all()
    q_lst = []
    for questions in questions_all:
        q_lst.append({'q_id': questions.id, 'q_text': questions.question_title, 'quiz_code': questions.quiz_id})
    return render_template('Quiz_Management.html', quiz_lst=quiz_lst, q_lst=q_lst)

@app.route('/new_quiz',methods = ['GET', 'POST'])
def new_quiz():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'save':
            chap_code = request.form.get('chapter_id')
            quiz_date = request.form.get('date_quiz')
            quiz_time = request.form.get('quiz_duration')
            date_quiz = datetime.strptime(quiz_date, "%Y-%m-%d").date()
            time_quiz = datetime.strptime(quiz_time, "%H:%M").time()
            chap = Chapter.query.filter_by(chapter_id=chap_code).first()
            if chap:
                quiz = Quiz(chapter_id=chap_code, date_of_quiz=date_quiz, time_duration=time_quiz)
                db.session.add(quiz)
                db.session.commit()
                return redirect('/quiz_management')
            else:
                return 'Chapter not found'
        elif action == 'cancel':
            return redirect('/quiz_management')
    return render_template('New_Quiz.html')


@app.route('/new_question/<int:id>',methods = ['GET', 'POST'])
def new_question(id):
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'save':
            quiz = Quiz.query.filter_by(id=id).first()
            q_chap = quiz.chapter_id
            q_text = request.form.get('q_text')
            q_statement = request.form.get('q_statement')
            q_opt1 = request.form.get('q_opt1')
            q_opt2 = request.form.get('q_opt2')
            q_opt3 = request.form.get('q_opt3')
            q_opt4 = request.form.get('q_opt4')
            q_ans = request.form.get('q_ans')
            question = Questions(chapter_id=q_chap, quiz_id=id, question_title=q_text, question_statement=q_statement, option1=q_opt1, option2=q_opt2, option3=q_opt3, option4=q_opt4, correct_answer=q_ans)
            db.session.add(question)
            db.session.commit()
            return redirect('/quiz_management')
        elif action == 'cancel':
            return redirect('/quiz_management')
    return render_template('New_Question.html', quizz_id=id)


@app.route('/edit_question/<int:id>',methods = ['GET', 'POST'])
def edit_question(id):
    question_edit = Questions.query.filter_by(id=id).first()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'save':
            q_text = request.form.get('q_text')
            q_statement = request.form.get('q_statement')
            q_opt1 = request.form.get('q_opt1')
            q_opt2 = request.form.get('q_opt2')
            q_opt3 = request.form.get('q_opt3')
            q_opt4 = request.form.get('q_opt4')
            q_ans = request.form.get('q_ans')
            question = Questions.query.filter_by(question_title=q_text).first()
            question.question_title = q_text
            question.question_statement = q_statement
            question.option1 = q_opt1
            question.option2 = q_opt2
            question.option3 = q_opt3
            question.option4 = q_opt4
            question.correct_answer = q_ans
            db.session.commit()
            return redirect('/quiz_management')
        elif action == 'cancel':
            return redirect('/quiz_management')
    return render_template('Edit_Question.html', question_edit=question_edit)


@app.route('/delete_question/<int:id>',methods = ['GET', 'POST'])
def delete_question(id):
    delete_question = Questions.query.filter_by(id=id).first()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'delete':
            quiz_code = request.form.get('quiz_code')
            q_text = request.form.get('q_text')
            question = Questions.query.filter_by(question_title=q_text).first()
            db.session.delete(question)
            db.session.commit()
            return redirect('/quiz_management')
        elif action == 'cancel':
            return redirect('/quiz_management')
    return render_template('Delete_Question.html', delete_question=delete_question)


@app.route('/view_subjects/<int:id>',methods = ['GET', 'POST'])
def view_subjects(id):
    sub_view = Subjects.query.filter_by(Subject_code=id).first()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'back':
            return redirect('/admin_dashboard')
        elif action == 'edit':
            sub_name = request.form.get('sub_name')
            sub_desc = request.form.get('sub_desc')
            subject_edit = Subjects.query.filter_by(Subject_code=id).first()
            subject_edit.subject_name = sub_name
            subject_edit.subject_description = sub_desc
            db.session.commit()
            return redirect('/admin_dashboard')
        elif action == 'delete':
            subject = Subjects.query.filter_by(Subject_code=id).first()
            chap_del = Chapter.query.filter_by(subject_code_chapter=id).all()
            for chap in chap_del:
                quiz = Quiz.query.filter_by(chapter_id=chap.chapter_id).all()
                question = Questions.query.filter_by(chapter_id=chap.chapter_id).all()
                for ques in question:
                    db.session.delete(ques)
                for qz in quiz:
                    db.session.delete(qz)
                db.session.delete(chap)
            db.session.delete(subject)
            db.session.commit()
            return redirect('/admin_dashboard')
    return render_template('View_Subjects.html', sub_view=sub_view)


@app.route('/view_quizzes/<int:id>',methods = ['GET', 'POST'])
def view_quizzes(id):
    quiz_view = Quiz.query.filter_by(id=id).first()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'back':
            return redirect('/quiz_management')
        elif action == 'edit':
            quiz_date = request.form.get('date_quiz')
            quiz_time = request.form.get('quiz_duration')
            date_quiz = datetime.strptime(quiz_date, "%Y-%m-%d").date()
            time_quiz = datetime.strptime(quiz_time, "%H:%M").time()
            quiz_edit = Quiz.query.filter_by(id=id).first()
            quiz_edit.date_of_quiz = date_quiz
            quiz_edit.time_duration = time_quiz
            db.session.commit()
            return redirect('/quiz_management')
        elif action == 'delete':
            quiz = Quiz.query.filter_by(id=id).first()
            question_del = Questions.query.filter_by(quiz_id=id).all()
            for ques in question_del:
                db.session.delete(ques)
            db.session.delete(quiz)
            db.session.commit()
            return redirect('/quiz_management')
    return render_template('View_Quizzes.html', quiz_view=quiz_view)


@app.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():
    # Get upcoming quizzes
    upcoming_quiz = []
    quizzes = Quiz.query.all()
    
    for quiz in quizzes:
        if quiz.date_of_quiz > datetime.now().date() or (
            quiz.date_of_quiz == datetime.now().date() and 
            quiz.time_duration > datetime.now().time()
        ):
            chapter = Chapter.query.filter_by(chapter_id=quiz.chapter_id).first()
            if chapter:
                ques_count = Questions.query.filter_by(quiz_id=quiz.id).count()
                upcoming_quiz.append({
                    'quiz_id': quiz.id,
                    'chap_name': chapter.chapter_name,
                    'ques_count': ques_count,
                    'quiz_date': quiz.date_of_quiz,
                    'quiz_time': quiz.time_duration
                })
    
    # Sort upcoming quizzes by date and time
    upcoming_quiz.sort(key=lambda x: (x['quiz_date'], x['quiz_time']))
    
    # Get recent quiz scores
    recent_scores = Scores.query.order_by(Scores.time_stamp_of_attempt.desc()).limit(5).all()
    scores_with_details = []
    for score in recent_scores:
        quiz = Quiz.query.filter_by(id=score.quiz_id).first()
        if quiz:
            chapter = Chapter.query.filter_by(chapter_id=quiz.chapter_id).first()
            scores_with_details.append({
                'id': score.id,
                'quiz_name': chapter.chapter_name if chapter else 'Unknown Quiz',
                'time_stamp_of_attempt': score.time_stamp_of_attempt,
                'score': score.score
            })
    
    return render_template('User_Dashboard.html',
                         upcoming=upcoming_quiz,
                         recent_scores=scores_with_details)


@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search_query', '').strip()
    
    # Search in users
    users = Users_Info.query.filter(
        (Users_Info.username.ilike(f'%{search_query}%')) |
        (Users_Info.fullname.ilike(f'%{search_query}%')) |
        (Users_Info.qualifications.ilike(f'%{search_query}%'))
    ).all()
    
    # Search in subjects
    subjects = Subjects.query.filter(
        (Subjects.subject_name.ilike(f'%{search_query}%')) |
        (Subjects.subject_description.ilike(f'%{search_query}%'))
    ).all()
    
    # Search in chapters
    chapters = Chapter.query.filter(
        (Chapter.chapter_name.ilike(f'%{search_query}%')) |
        (Chapter.chapter_description.ilike(f'%{search_query}%'))
    ).all()
    
    # Search in questions
    questions = Questions.query.filter(
        (Questions.question_title.ilike(f'%{search_query}%')) |
        (Questions.question_statement.ilike(f'%{search_query}%'))
    ).all()
    
    return render_template('Search.html', 
                         users=users,
                         subjects=subjects,
                         chapters=chapters,
                         questions=questions)


@app.route('/quiz_history')
def quiz_history():
    # Get all scores for the current user
    scores = Scores.query.order_by(Scores.time_stamp_of_attempt.desc()).all()
    scores_with_details = []
    
    for score in scores:
        quiz = Quiz.query.filter_by(id=score.quiz_id).first()
        if quiz:
            chapter = Chapter.query.filter_by(chapter_id=quiz.chapter_id).first()
            if chapter:
                subject = Subjects.query.filter_by(Subject_code=chapter.subject_code_chapter).first()
                scores_with_details.append({
                    'id': score.id,
                    'subject_name': subject.subject_name if subject else 'Unknown Subject',
                    'chapter_name': chapter.chapter_name,
                    'time_stamp_of_attempt': score.time_stamp_of_attempt,
                    'score': score.score
                })
    
    return render_template('Quiz_History.html', scores=scores_with_details)

@app.route('/view_result/<int:score_id>')
def view_result(score_id):
    score = Scores.query.get_or_404(score_id)
    quiz = Quiz.query.filter_by(id=score.quiz_id).first()

    if quiz:
        chapter = Chapter.query.filter_by(chapter_id=quiz.chapter_id).first()
        subject = Subjects.query.filter_by(Subject_code=chapter.subject_code_chapter).first() if chapter else None
        questions = Questions.query.filter_by(quiz_id=quiz.id).all()

        # Prepare result data
        result = {
            'subject_name': subject.subject_name if subject else 'Unknown Subject',
            'chapter_name': chapter.chapter_name if chapter else 'Unknown Chapter',
            'time_stamp_of_attempt': score.time_stamp_of_attempt,
            'score': score.score,
            'total_questions': len(questions),
            'questions': []
        }

        # Add question details
        for question in questions:
            result['questions'].append({
                'question_title': question.question_title,
                'question_statement': question.question_statement,
                'options': [question.option1, question.option2, question.option3, question.option4],
                'user_answer': 'Not Available',  # Replace with actual user answer if stored
                'correct_answer': question.correct_answer,
                'is_correct': False  # Replace with actual comparison logic if user answers are stored
            })

        return render_template('View_Result.html', result=result)

    return redirect('/quiz_history')

@app.route('/view_quiz/<int:quiz_id>')
def view_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    chapter = Chapter.query.filter_by(chapter_id=quiz.chapter_id).first()
    subject = Subjects.query.filter_by(Subject_code=chapter.subject_code_chapter).first() if chapter else None
    questions = Questions.query.filter_by(quiz_id=quiz.id).all()
    
    quiz_details = {
        'subject_name': subject.subject_name if subject else 'Unknown Subject',
        'chapter_name': chapter.chapter_name if chapter else 'Unknown Chapter',
        'date_of_quiz': quiz.date_of_quiz,
        'time_duration': quiz.time_duration,
        'total_questions': len(questions),
        'questions': []
    }
    
    for question in questions:
        quiz_details['questions'].append({
            'question_title': question.question_title,
            'question_statement': question.question_statement,
            'option1': question.option1,
            'option2': question.option2,
            'option3': question.option3,
            'option4': question.option4
        })
    
    return render_template('View_Quiz.html', quiz=quiz_details)


@app.route('/summary_charts')
def summary_charts():
    # Create charts directory if it doesn't exist
    charts_dir = os.path.join(app.static_folder, 'charts')
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'summary_charts_{timestamp}.png'
    filepath = os.path.join(charts_dir, filename)
    
    # Get all subjects
    subjects = Subjects.query.all()
    subject_names = [subject.subject_name for subject in subjects]
    
    # Count quizzes for each subject
    quiz_counts = []
    for subject in subjects:
        chapters = Chapter.query.filter_by(subject_code_chapter=subject.Subject_code).all()
        chapter_ids = [chapter.chapter_id for chapter in chapters]
        quiz_count = Quiz.query.filter(Quiz.chapter_id.in_(chapter_ids)).count()
        quiz_counts.append(quiz_count)
    
    # Get month-wise quiz attempts
    current_month = datetime.now().month
    month_attempts = []
    month_names = []
    
    for month in range(current_month - 2, current_month + 1):
        if month <= 0:
            actual_month = 12 + month
            year = datetime.now().year - 1
        else:
            actual_month = month
            year = datetime.now().year
        
        month_name = datetime(year, actual_month, 1).strftime('%B')
        month_names.append(month_name)
        
        start_date = datetime(year, actual_month, 1)
        if actual_month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, actual_month + 1, 1)
        
        attempt_count = Scores.query.filter(
            Scores.time_stamp_of_attempt >= start_date,
            Scores.time_stamp_of_attempt < end_date
        ).count()
        month_attempts.append(attempt_count)
    
    # Create figure with two subplots
    plt.figure(figsize=(15, 6))
    
    # Subject-wise quiz counts (Bar Chart)
    plt.subplot(1, 2, 1)
    colors = ['lightblue', 'green', 'pink']
    plt.bar(subject_names, quiz_counts, color=colors[:len(subject_names)])
    plt.title('Subject wise no.of quizzes', pad=20)
    plt.ylabel('Number of Quizzes')
    
    # Month-wise attempts (Pie Chart)
    plt.subplot(1, 2, 2)
    if sum(month_attempts) > 0:
        patches, texts, autotexts = plt.pie(month_attempts,
                autopct=lambda pct: f'{int(pct*sum(month_attempts)/100)}',
                pctdistance=0.75)
        # Add labels manually with better positioning
        plt.legend(patches, month_names, title="Months", 
                  loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title('Month wise no.of quizzes attempted', pad=20)
    
    # Save the figure
    plt.savefig(filepath, bbox_inches='tight', dpi=300, facecolor='white')
    plt.close()
    
    return render_template('Summary_Charts.html', chart_image=f'charts/{filename}')


@app.route('/user_summary')
def user_summary():
    # Create charts directory if it doesn't exist
    charts_dir = os.path.join(app.static_folder, 'charts')
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'user_summary_{timestamp}.png'
    filepath = os.path.join(charts_dir, filename)
    
    # Get all subjects and their quiz counts
    subjects = Subjects.query.all()
    subject_names = []
    quiz_counts = []
    
    for subject in subjects:
        chapters = Chapter.query.filter_by(subject_code_chapter=subject.Subject_code).all()
        chapter_ids = [chapter.chapter_id for chapter in chapters]
        quiz_count = Quiz.query.filter(Quiz.chapter_id.in_(chapter_ids)).count()
        
        subject_names.append(subject.subject_name)
        quiz_counts.append(quiz_count if quiz_count is not None else 0)
    
    # Get month-wise quiz attempts for the last 3 months
    current_month = datetime.now().month
    month_attempts = {}
    
    # Calculate the last 3 months
    for i in range(3):
        month_num = ((current_month - i - 1) % 12) + 1  # This ensures we wrap around to previous year if needed
        month_attempts[month_num] = 0
    
    # Get all scores and count attempts by month
    scores = Scores.query.all()
    for score in scores:
        month = score.time_stamp_of_attempt.month
        if month in month_attempts:
            month_attempts[month] += 1
    
    # Convert month numbers to labels (01, 02, 03)
    month_labels = [f"{m:02d}" for m in sorted(month_attempts.keys())]
    month_values = [month_attempts[m] for m in sorted(month_attempts.keys())]
    
    # Create figure with two subplots
    plt.figure(figsize=(15, 6))
    
    # Subject-wise number of quizzes (Bar Chart)
    plt.subplot(1, 2, 1)
    colors = ['skyblue', 'lightgreen', 'lightpink']
    plt.bar(subject_names, quiz_counts, color=colors[:len(subject_names)])
    plt.title('Subject-wise No. of Quizzes')
    plt.ylabel('Number of Quizzes')
    plt.xticks(rotation=45)
    
    # Month-wise quiz attempts (Pie Chart)
    plt.subplot(1, 2, 2)
    if sum(month_values) > 0:  # Only create pie chart if there are attempts
        plt.pie(month_values, labels=month_labels,
                autopct='%d', pctdistance=0.85)
    else:
        # Create an empty pie chart with "No Data" message
        plt.pie([1], labels=['No Data'],
               colors=['lightgray'])
    plt.title('Month-wise No. of Quizzes Attempted')
    
    # Save the figure
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close()
    
    return render_template('User_Summary.html', chart_image=f'charts/{filename}')

@app.route('/take_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Questions.query.filter_by(quiz_id=quiz_id).all()

    if request.method == 'POST':
        score = 0
        user_answers = {}

        for question in questions:
            user_answer = request.form.get(f'question_{question.id}')
            user_answers[question.id] = user_answer
            if user_answer == question.correct_answer:
                score += 1

        # Save the score and user answers to the database
        user_id = 1  # Replace with the actual logged-in user ID
        new_score = Scores(
            user_id=user_id,
            quiz_id=quiz_id,
            time_stamp_of_attempt=datetime.now(),
            score=score
        )
        db.session.add(new_score)
        db.session.commit()

        # Save user answers (if needed, create a new table for storing answers)
        for question_id, answer in user_answers.items():
            # Example: Save answers to a new table if required
            pass

        return redirect('/quiz_history')

    return render_template('Take_Quiz.html', quiz=quiz, questions=questions)