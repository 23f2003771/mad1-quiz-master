from flask import Flask,render_template,request,redirect, session
from datetime import datetime, time
from .models import *
from flask import current_app as app
import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt

app.secret_key = 'secret-key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('username')
        pswd = request.form.get('password')
        user = Users_Info.query.filter_by(username=uname, password=pswd).first()
        if user:
            session['user_id'] = user.id
            if user.id == 1:
                return redirect('/admin_dashboard')
            else:
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
            question = Questions.query.filter_by(id=id).first()
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
    
    upcoming_quiz.sort(key=lambda x: (x['quiz_date'], x['quiz_time']))
    
    if 'user_id' not in session:
        return redirect('/')

    user_id = session['user_id']
    recent_scores = Scores.query.filter_by(user_id=user_id).order_by(Scores.time_stamp_of_attempt.desc()).limit(5).all()
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

    quizzes = Quiz.query.filter(
        Quiz.id.ilike(f'%{search_query}%') |
        Quiz.date_of_quiz.ilike(f'%{search_query}%')
    ).all()

    chapters_name = Chapter.query.all()

    users = Users_Info.query.filter(
        (Users_Info.username.ilike(f'%{search_query}%')) |
        (Users_Info.fullname.ilike(f'%{search_query}%')) |
        (Users_Info.qualifications.ilike(f'%{search_query}%'))
    ).all()

    subjects = Subjects.query.filter(
        (Subjects.subject_name.ilike(f'%{search_query}%')) |
        (Subjects.subject_description.ilike(f'%{search_query}%'))
    ).all()

    chapters = Chapter.query.filter(
        (Chapter.chapter_name.ilike(f'%{search_query}%')) |
        (Chapter.chapter_description.ilike(f'%{search_query}%'))
    ).all()

    return render_template(
        'Search.html',
        users=users,
        quizzes=quizzes,
        chapters_name=chapters_name,
        subjects=subjects,
        chapters=chapters,
    )


@app.route('/user_search', methods=['POST'])
def user_search():
    search_query = request.form.get('search_query', '').strip()

    quizzes = Quiz.query.filter(
        Quiz.id.ilike(f'%{search_query}%') |
        Quiz.date_of_quiz.ilike(f'%{search_query}%')
    ).all()

    chapters_name = Chapter.query.all()

    subjects = Subjects.query.filter(
        (Subjects.subject_name.ilike(f'%{search_query}%')) |
        (Subjects.subject_description.ilike(f'%{search_query}%'))
    ).all()

    chapters = Chapter.query.filter(
        (Chapter.chapter_name.ilike(f'%{search_query}%')) |
        (Chapter.chapter_description.ilike(f'%{search_query}%'))
    ).all()

    return render_template(
        'User_Search.html',
        chapters_name=chapters_name,
        quizzes=quizzes,
        subjects=subjects,
        chapters=chapters,
    )


@app.route('/quiz_history')
def quiz_history():
    if 'user_id' not in session:
        return redirect('/')

    user_id = session['user_id']

    scores = Scores.query.filter_by(user_id=user_id).order_by(Scores.time_stamp_of_attempt.desc()).all()
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

        result = {
            'subject_name': subject.subject_name if subject else 'Unknown Subject',
            'chapter_name': chapter.chapter_name if chapter else 'Unknown Chapter',
            'time_stamp_of_attempt': score.time_stamp_of_attempt,
            'score': score.score,
            'total_questions': len(questions),
            'questions': []
        }

        for question in questions:
            result['questions'].append({
                'question_title': question.question_title,
                'question_statement': question.question_statement,
                'options': [question.option1, question.option2, question.option3, question.option4],
                'user_answer': 'Not Available',
                'correct_answer': question.correct_answer,
                'is_correct': False
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
    charts_dir = os.path.join(app.static_folder, 'charts')
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'summary_charts_{timestamp}.png'
    filepath = os.path.join(charts_dir, filename)

    subjects = Subjects.query.all()
    subject_names = []
    top_scores = []

    for subject in subjects:
        chapters = Chapter.query.filter_by(subject_code_chapter=subject.Subject_code).all()
        chapter_ids = [chapter.chapter_id for chapter in chapters]
        quiz_ids = Quiz.query.filter(Quiz.chapter_id.in_(chapter_ids)).with_entities(Quiz.id).all()
        quiz_ids = [quiz.id for quiz in quiz_ids]
        top_score = Scores.query.filter(Scores.quiz_id.in_(quiz_ids)).order_by(Scores.score.desc()).first()

        subject_names.append(subject.subject_name)
        top_scores.append(top_score.score if top_score else 0)

    total_attempts = []

    for subject in subjects:
        chapters = Chapter.query.filter_by(subject_code_chapter=subject.Subject_code).all()
        chapter_ids = [chapter.chapter_id for chapter in chapters]
        quiz_ids = Quiz.query.filter(Quiz.chapter_id.in_(chapter_ids)).with_entities(Quiz.id).all()
        quiz_ids = [quiz.id for quiz in quiz_ids]
        attempt_count = Scores.query.filter(Scores.quiz_id.in_(quiz_ids)).count()

        total_attempts.append(attempt_count)

    plt.figure(figsize=(15, 6))

    plt.subplot(1, 2, 1)
    plt.bar(subject_names, top_scores, color=['skyblue', 'lightgreen', 'lightpink'][:len(subject_names)])
    plt.title('Subject-wise Top Scores', pad=20)
    plt.ylabel('Top Scores')
    plt.xticks(rotation=45)

    plt.subplot(1, 2, 2)
    if sum(total_attempts) > 0:
        wedges, texts, autotexts = plt.pie(total_attempts, labels=subject_names, autopct='%d', pctdistance=0.85)
        for wedge in wedges:
            wedge.set_edgecolor('white')
        plt.gca().add_artist(plt.Circle((0, 0), 0.5, color='white'))
    else:
        plt.pie([1], labels=['No Data'], colors=['lightgray'])
    plt.title('Subject-wise Total Quiz Attempts')

    # Save the figure
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close()

    return render_template('Summary_Charts.html', chart_image=f'charts/{filename}')


@app.route('/user_summary')
def user_summary():

    charts_dir = os.path.join(app.static_folder, 'charts')
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'user_summary_{timestamp}.png'
    filepath = os.path.join(charts_dir, filename)

    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']

    subjects = Subjects.query.all()
    subject_names = []
    quiz_attempts = []

    for subject in subjects:
        chapters = Chapter.query.filter_by(subject_code_chapter=subject.Subject_code).all()
        chapter_ids = [chapter.chapter_id for chapter in chapters]
        quiz_ids = Quiz.query.filter(Quiz.chapter_id.in_(chapter_ids)).with_entities(Quiz.id).all()
        quiz_ids = [quiz.id for quiz in quiz_ids]
        attempt_count = Scores.query.filter(Scores.quiz_id.in_(quiz_ids), Scores.user_id == user_id).count()

        subject_names.append(subject.subject_name)
        quiz_attempts.append(attempt_count)

    current_month = datetime.now().month
    month_attempts = []
    month_names = []

    for month_offset in range(-2, 1):
        actual_month = (current_month + month_offset - 1) % 12 + 1
        year = datetime.now().year + (month_offset // 12)
        month_name = datetime(year, actual_month, 1).strftime('%B')
        month_names.append(month_name)

        start_date = datetime(year, actual_month, 1)
        end_date = datetime(year, actual_month + 1, 1) if actual_month < 12 else datetime(year + 1, 1)
        attempt_count = Scores.query.filter(
            Scores.time_stamp_of_attempt >= start_date,
            Scores.time_stamp_of_attempt < end_date,
            Scores.user_id == user_id
        ).count()
        month_attempts.append(attempt_count)

    plt.figure(figsize=(15, 6))

    plt.subplot(1, 2, 1)
    plt.bar(subject_names, quiz_attempts, color=['skyblue', 'lightgreen', 'lightpink'][:len(subject_names)])
    plt.title('Subject-wise No. of Quizzes Attempted', pad=20)
    plt.ylabel('Number of Quizzes')
    plt.xticks(rotation=45)

    plt.subplot(1, 2, 2)

    all_month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']
    colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#C2C2F0', '#FFB3E6',
              '#FF6666', '#B3B3CC', '#FFFF99', '#B3E6B3', '#FF99CC', '#66E6FF']

    all_month_attempts = [0] * 12
    for i, month_name in enumerate(month_names):
        month_index = all_month_names.index(month_name)
        all_month_attempts[month_index] = month_attempts[i]


    if sum(all_month_attempts) > 0:
        plt.pie(
            all_month_attempts,
            colors=colors,
            startangle=90,
            autopct='%1.1f%%'
        )
        plt.legend(
            all_month_names,
            loc="lower right",
            bbox_to_anchor=(1.2, 0),
            title="Months",
            fontsize="small"
        )
    else:
        plt.pie([1], labels=['No Data'], colors=['lightgray'])

    plt.title('Month-wise No. of Quizzes Attempted')
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close()

    return render_template('User_Summary.html', chart_image=f'charts/{filename}')


@app.route('/take_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Questions.query.filter_by(quiz_id=quiz_id).all()

    if request.method == 'POST':
        if 'user_id' not in session:
            return redirect('/')

        user_id = session['user_id']
        score = 0
        user_answers = {}

        for question in questions:
            user_answer = request.form.get(f'question_{question.id}')
            user_answers[question.id] = user_answer
            if user_answer == question.correct_answer:
                score += 1

        new_score = Scores(
            user_id=user_id,
            quiz_id=quiz_id,
            time_stamp_of_attempt=datetime.now(),
            score=score
        )
        db.session.add(new_score)
        db.session.commit()

        return redirect('/quiz_history')

    return render_template('Take_Quiz.html', quiz=quiz, questions=questions)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')