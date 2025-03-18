# for routes

from flask import Flask,render_template,redirect,url_for,request,flash

from flask import current_app as app #importing the app from the current module in app.py
from datetime import datetime
from .models import * #both are in same folder


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        curr_user=User.query.filter_by(username=username,password=password).first() # it will give object of user
        if curr_user:
            if curr_user.password==password:
                if curr_user.type=='admin':
                    return redirect(url_for("admin_dashboard",username=username))
                else:
                    return redirect(url_for("user_dashboard",username=username))
                #    return render_template('user.html',username=username)  # this is only showing the base url
        else:
            
            return render_template('login.html',msg='Invalid username or password')


    return render_template('login.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form.get('fullname')
        email=request.form.get('username')
        password=request.form.get('password')
        curr_user=User.query.filter_by(username=username).first()
        if curr_user:
            return 'username already exists'
        else:
            curr_user=User(username=username,email=email,password=password)
            db.session.add(curr_user)
            db.session.commit()
            return redirect("login.html",msg='User registered successfully')
    return render_template('signup.html')


@app.route("/admin_page/<username>")
def admin_page(username):
    return render_template('admin_dashboard.html',username=username)


@app.route("/admin/<username>")
def admin_dashboard(username):
    return render_template('admin_dashboard.html',username=username)

@app.route("/user/<username>")
def user_dashboard(username):
     return render_template('user.html',username=username)     




@app.route('/manage_subjects')
def manage_subjects():
    subjects = Subject.query.all()
    return render_template('manage_subjects.html', subjects=subjects)

@app.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        user_id=1
        new_subject = Subject(name=name, description=description, user_id=user_id)
        db.session.add(new_subject)
        db.session.commit()
        return redirect(url_for('manage_subjects'))
    return render_template('add_subject.html')


@app.route('/edit_subject/<int:id>', methods=['GET', 'POST'])
def edit_subject(id):
    subject = Subject.query.get_or_404(id)
    if request.method == 'POST':
        subject.name = request.form['name']
        subject.description = request.form['description']
        db.session.commit()
        
        return redirect(url_for('manage_subjects'))
    return render_template('edit_subject.html', subject=subject)


@app.route('/delete_subject/<int:id>')
def delete_subject(id):
    subject = Subject.query.get(id)
    if subject:
        db.session.delete(subject)
        db.session.commit()
        
    return redirect(url_for('manage_subjects'))
            

@app.route('/manage_chapters')
def manage_chapters():
    chapters = Chapter.query.all()
    return render_template('manage_chapters.html', chapters=chapters)

@app.route('/add_chapter', methods=['GET', 'POST'])
def add_chapter():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        subject_id = request.form['subject_id']
        new_chapter = Chapter(name=name, description=description, subject_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        return redirect(url_for('manage_chapters'))
    subjects = Subject.query.all()
    return render_template('add_chapter.html', subjects=subjects)


    
@app.route('/edit_chapter/<int:id>', methods=['GET', 'POST'])
def edit_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    if request.method == 'POST':
        chapter.name = request.form['name']
        chapter.description = request.form['description']
        db.session.commit()
        
        return redirect(url_for('manage_chapters'))
    return render_template('edit_chapter.html', chapter=chapter)


@app.route('/delete_chapter/<int:id>')
def delete_chapter(id):
    chapter =Chapter.query.get(id)
    if chapter:
        db.session.delete(chapter)
        db.session.commit()
        
    return redirect(url_for('manage_chapters'))
            


@app.route('/manage_quizzes')
def manage_quizzes():
    quizzes = Quiz.query.all()
    return render_template('manage_quizzes.html', quizzes=quizzes)


@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        chapter_id = request.form['chapter_id']
        new_quiz = Quiz(date=date, chapter_id=chapter_id)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('manage_quizzes'))
    chapters = Chapter.query.all()
    return render_template('add_quiz.html', chapters=chapters)


@app.route('/edit_quiz/<int:id>', methods=['GET', 'POST'])
def edit_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    if request.method == 'POST':
        date_str = request.form['date']
        quiz.date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        db.session.commit()
        
        return redirect(url_for('manage_quizzes'))
    return render_template('edit_quiz.html')


@app.route('/delete_quiz/<int:id>')
def delete_quiz(id):
    quiz =Quiz.query.get(id)
    if quiz:
        db.session.delete(quiz)
        db.session.commit()
        
    return redirect(url_for('manage_quizzes'))
            


@app.route('/manage_questions')
def manage_questions():
    questions = Question.query.all()
    return render_template('manage_questions.html', questions=questions)

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question_text = request.form['question_text']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option = request.form['correct_option']
        quiz_id = request.form['quiz_id']
        subject_id = request.form['subject_id']
        
        new_question = Question(
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            quiz_id=quiz_id,
            subject_id=subject_id
        )
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('manage_questions'))
    
    quizzes = Quiz.query.all()
    subjects = Subject.query.all()
    return render_template('add_question.html', quizzes=quizzes,subjects=subjects)



@app.route('/delete_question/<int:id>')
def delete_question(id):
    question =Question.query.get(id)
    if question:
        db.session.delete(question)
        db.session.commit()
        
    return redirect(url_for('manage_questions')) 

@app.route('/manage_scores')
def manage_scores():
    scores = Scores.query.all()
    return render_template('manage_scores.html', scores=scores)













@app.route('/quizzes')
def quizzes():
    subjects=Subject.query.all()
    chapters=Chapter.query.all()
    quizzes = Quiz.query.all()  
    return render_template('user_quizzes.html', subjects=subjects,chapters=chapters,quizzes=quizzes)




@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    if request.method == 'POST':
        score = 0
        for question in questions:
            option=question.option1
            user_answer = request.form.get(str(question.id))
            if user_answer == question.correct_option:
                score += 1
        # Save score
        user_score = Score(user_id=session['user_id'], quiz_id=quiz.id, total_score=score)
        db.session.add(user_score)
        db.session.commit()
        return redirect(url_for('view_score', score_id=user_score.id))
    
    return render_template('take_quiz.html', quiz=quiz, questions=questions)


# Route to display the user's score after completing the quiz
@app.route('/score/<int:score_id>')
def view_score(score_id):
    score = Score.query.get_or_404(score_id)
    return render_template('user_score.html', score=score)