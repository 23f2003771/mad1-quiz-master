from flask import Flask,render_template,request,redirect
from datetime import datetime
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
        chap_lst.append({'sbc': chapters.subject_code_chapter, 'chap_name': chapters.chapter_name, 'chap_code': chapters.chapter_id})
    sub_all = Subjects.query.all()
    sub_lst = []
    for subjects in sub_all:
        sub_lst.append({'s_code': subjects.Subject_code, 'sub_name': subjects.subject_name, 'sub_desc': subjects.subject_description})
    return render_template('Admin_Dashboard.html', chap_lst=chap_lst, sub_lst=sub_lst)


@app.route('/new_chapter',methods = ['GET', 'POST'])
def new_chapter():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'save':
            sub_code = request.form.get('sub_code')
            chap_code = request.form.get('Chap_code')
            chap_name = request.form.get('chap_name')
            chap_desc = request.form.get('chap_desc')
            chapter = Chapter(subject_code_chapter=sub_code,chapter_id=chap_code,chapter_name=chap_name, chapter_description=chap_desc)
            db.session.add(chapter)
            db.session.commit()
            return redirect('/admin_dashboard')
        elif action == 'cancel':
            return redirect('/admin_dashboard')
    return render_template('New_Chapter.html')


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


@app.route('/edit_chapter/<int:id>',methods = ['GET', 'POST'])
def chapter_edit(id):
    Chapter_edit = Chapter.query.filter_by(chapter_id=id).first()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'save':
            sub_code = request.form.get('sub_code')
            chap_code = request.form.get('Chap_code')
            chap_name = request.form.get('chap_name')
            chap_desc = request.form.get('chap_desc')
            chapter = Chapter.query.filter_by(subject_code_chapter=sub_code, chapter_id=chap_code).first()
            chapter.chapter_name = chap_name
            chapter.chapter_description = chap_desc
            chapter.subject_code_chapter = sub_code
            chapter.chapter_id = chap_code
            db.session.commit()
            return redirect('/admin_dashboard')
        elif action == 'cancel':
            return redirect('/admin_dashboard')
    return render_template('Edit_Chapter.html', chapter_edit=Chapter_edit)


@app.route('/chapter_delete/<int:id>',methods = ['GET', 'POST'])
def chapter_delete(id):
    Delete_chapter = Chapter.query.filter_by(chapter_id=id).first()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'delete':
            sub_code = request.form.get('sub_code')
            chap_code = request.form.get('Chap_code')
            chapter = Chapter.query.filter_by(subject_code_chapter=sub_code, chapter_id=chap_code).first()
            db.session.delete(chapter)
            db.session.commit()
            return redirect('/admin_dashboard')
        elif action == 'cancel':
            return redirect('/admin_dashboard')
    return render_template('Delete_Chapter.html', delete_chapter=Delete_chapter)


"""@app.route('/quiz_management')
def quiz_management():
    quiz_all = Chapter.query.all()
    quiz_lst = []
    for chapters in chap_all:
        chap_lst.append({'sbc': chapters.subject_code_chapter, 'chap_name': chapters.chapter_name, 'chap_code': chapters.chapter_id})
    sub_all = Subjects.query.all()
    sub_lst = []
    for subjects in sub_all:
        sub_lst.append({'s_code': subjects.Subject_code, 'sub_name': subjects.subject_name, 'sub_desc': subjects.subject_description})
    return render_template('Admin_Dashboard.html', chap_lst=chap_lst, sub_lst=sub_lst)


@app.route('/new_quiz',methods = ['GET', 'POST'])
def new_quiz():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'save':
            chap_code = request.form.get('chapter_id')
            quiz_date = request.form.get('quiz_date')
            quiz_time = request.form.get('quiz_duration')
            quiz = Quiz(chapter_id=chap_code, date_of_quiz=quiz_date, time_duration=quiz_time)
            db.session.add(quiz)
            db.session.commit()
            return redirect('/admin_dashboard')
        elif action == 'cancel':
            return redirect('/admin_dashboard')
    return render_template('New_Chapter.html')"""