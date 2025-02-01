from flask import Flask,render_template,request,redirect
from datetime import datetime, time
from .models import *
from flask import current_app as app

@app.route('/',methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('username')
        pswd = request.form.get('password')
        user = Users_Info.query.filter_by(username=uname, password=pswd).first()
        if user and user.id == 1:
            return redirect('/admin_dashboard')
        elif user and user.id != 1:
            return render_template('User_Dashboard.html', usr_name=user.fullname)
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