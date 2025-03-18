<!-- templates/view_quizzes.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quizzes </title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-4">
        
        <ul class="list-group">
            {%for subject in subjects%}
                {subject.name}
            {%endfor%}

            {% for quiz in quizzes %}
                <li class="list-group-item">
                    <a href="{{ url_for('take_quiz', quiz_id=quiz.id) }}">Take Quiz</a>
                </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>




<a href="{{url_for('admin_dashboard',username=username)}}" class="btn btn-warning ">admin_dashboard</a>



{% extends "base.html" %}

{% block content %}
<h2>Admin Dashboard</h2>

<!-- Manage Subjects -->
<section id="subjects">
    <h3>Manage Subjects</h3>
    <form action="/add_subject" method="POST">
        <input type="text" name="subject_name" placeholder="Subject Name" required>
        <button type="submit">Add Subject</button>
    </form>
    <ul>
        {% for subject in subjects %}
        <li>{{ subject.name }} <a href="/delete_subject/{{ subject.id }}">Delete</a></li>
        {% endfor %}
    </ul>
</section>

<!-- Manage Chapters -->
<section id="chapters">
    <h3>Manage Chapters</h3>
    <form action="/add_chapter" method="POST">
        <input type="text" name="chapter_name" placeholder="Chapter Name" required>
        <select name="subject_id" required>
            {% for subject in subjects %}
            <option value="{{ subject.id }}">{{ subject.name }}</option>
            {% endfor %}
        </select>
        <button type="submit">Add Chapter</button>
    </form>
    <ul>
        {% for chapter in chapters %}
        <li>{{ chapter.name }} ({{ chapter.subject.name }}) <a href="/delete_chapter/{{ chapter.id }}">Delete</a></li>
        {% endfor %}
    </ul>
</section>

<!-- Manage Quizzes -->
<section id="quizzes">
    <h3>Manage Quizzes</h3>
    <form action="/add_quiz" method="POST">
        <input type="text" name="quiz_name" placeholder="Quiz Name" required>
        <select name="chapter_id" required>
            {% for chapter in chapters %}
            <option value="{{ chapter.id }}">{{ chapter.name }}</option>
            {% endfor %}
        </select>
        <button type="submit">Add Quiz</button>
    </form>
    <ul>
        {% for quiz in quizzes %}
        <li>{{ quiz.name }} ({{ quiz.chapter.name }}) <a href="/delete_quiz/{{ quiz.id }}">Delete</a></li>
        {% endfor %}
    </ul>
</section>

<!-- Manage Questions -->
<section id="questions">
    <h3>Manage Questions</h3>
    <form action="/add_question" method="POST">
        <textarea name="question_text" placeholder="Question Text" required></textarea>
        <select name="quiz_id" required>
            {% for quiz in quizzes %}
            <option value="{{ quiz.id }}">{{ quiz.name }}</option>
            {% endfor %}
        </select>
        <button type="submit">Add Question</button>
    </form>
    <ul>
        {% for question in questions %}
        <li>{{ question.text }} ({{ question.quiz.name }}) <a href="/delete_question/{{ question.id }}">Delete</a></li>
        {% endfor %}
    </ul>
</section>

{% endblock %}









from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set up SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the models for Subjects, Chapters, Quizzes, and Questions
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject = db.relationship('Subject', backref=db.backref('chapters', lazy=True))

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    chapter = db.relationship('Chapter', backref=db.backref('quizzes', lazy=True))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    quiz = db.relationship('Quiz', backref=db.backref('questions', lazy=True))

# Initialize the database (run once)
with app.app_context():
    db.create_all()

# Routes for Admin Dashboard
@app.route('/admin')
def admin_dashboard():
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()
    questions = Question.query.all()
    return render_template('/admin_dashboard.html', subjects=subjects, chapters=chapters, quizzes=quizzes, questions=questions)

# CRUD for Subjects (Admin)
@app.route('/add_subject', methods=['POST'])
def add_subject():
    name = request.form['subject_name']
    new_subject = Subject(name=name)
    db.session.add(new_subject)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_subject/<int:id>')
def delete_subject(id):
    subject = Subject.query.get(id)
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

# CRUD for Chapters (Admin)
@app.route('/add_chapter', methods=['POST'])
def add_chapter():
    name = request.form['chapter_name']
    subject_id = request.form['subject_id']
    new_chapter = Chapter(name=name, subject_id=subject_id)
    db.session.add(new_chapter)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_chapter/<int:id>')
def delete_chapter(id):
    chapter = Chapter.query.get(id)
    db.session.delete(chapter)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

# CRUD for Quizzes (Admin)
@app.route('/add_quiz', methods=['POST'])
def add_quiz():
    name = request.form['quiz_name']
    chapter_id = request.form['chapter_id']
    new_quiz = Quiz(name=name, chapter_id=chapter_id)
    db.session.add(new_quiz)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_quiz/<int:id>')
def delete_quiz(id):
    quiz = Quiz.query.get(id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

# CRUD for Questions (Admin)
@app.route('/add_question', methods=['POST'])
def add_question():
    text = request.form['question_text']
    quiz_id = request.form['quiz_id']
    new_question = Question(text=text, quiz_id=quiz_id)
    db.session.add(new_question)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_question/<int:id>')
def delete_question(id):
    question = Question.query.get(id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

# Routes for User Dashboard
@app.route('/')
def home():
    subjects = Subject.query.all()
    return render_template('/home.html', subjects=subjects)

@app.route('/take_quiz/<int:quiz_id>')
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    return render_template('/take_quiz.html', quiz=quiz, questions=questions)

if __name__ == "__main__":
    app.run(debug=True)









{%extends "admin_base.html"%}
{%block content%}       
       
      <div class="container">
        {%if subject%}
        <div class="row">
          {%for sub in subject%}
          <div class="col">
            <div class="card" style="width: 18rem;">
                <div class="card-body">
                  <h5 class="card-title">{{sub.name}}</h5>
                  <h6 class="card-subtitle mb-2 text-muted">{{sub.description}}</h6>
                 
                  {%if sub.chapters%}
                  <div id="main">
                  <table>
                    <tr>
                      <th>Id</th>
                      <th>Name</th>
                      <th>Description</th>
                    </tr>
                    
                    {%for chapter in sub.chapters%}
                    <tr>
                      <td>{{chapter.id}}</td>
                      <td>{{chapter.name}}</td>
                      <td>{{chapter.description}}</td>
                    </tr>
                            {%include "add_quiz.html"%}



                    {%endfor%}
                  </table>
                  <a class="nav-link" href="/quiz"><h4>Quizes</h4></a></label>
                  </div>
                  {%else%}
                     <p>No chapters Yet</p>
                  {%endif%}
                  </div>
              
                  <a href="/chapter/{{sub.id}}/{{username}}" type="button" class="btn btn-outline-primary">Add Chapters</a>
                 
                </div>
              </div>
            </div>
          {%endfor%}
        </div>
        {%else%}
        <h3 id="center">No subjct avilable</h3>
        {%endif%}
      </div>
      <div id="center">
      <a href="/add_subject/{{username}}" type="button" class="btn btn-primary" >+add Subject</a>
      </div>
{%endblock%}






from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask and the database

db = SQLAlchemy()
def new_app():
    app=Flask(__name__)
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///quiz_test.sqlite3'  #3rd step database
    db.init_app(app) #4th step from database.py
    app.app_context().push() # bring everything under the  context of flask
    return app

app=new_app()

# Database Models (for reference, you already have these models)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), default='general')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question = db.Column(db.String, nullable=False)
    option1 = db.Column(db.String, nullable=False)
    option2 = db.Column(db.String, nullable=False)
    option3 = db.Column(db.String, nullable=False)
    option4 = db.Column(db.String, nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_score = db.Column(db.Integer, nullable=False)

# Routes for Admin Dashboard and CRUD operations

@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

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

@app.route('/manage_quizzes')
def manage_quizzes():
    quizzes = Quiz.query.all()
    return render_template('manage_quizzes.html', quizzes=quizzes)

@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        date = request.form['date']
        chapter_id = request.form['chapter_id']
        new_quiz = Quiz(date=date, chapter_id=chapter_id)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('manage_quizzes'))
    chapters = Chapter.query.all()
    return render_template('add_quiz.html', chapters=chapters)

@app.route('/manage_questions')
def manage_questions():
    questions = Question.query.all()
    return render_template('manage_questions.html', questions=questions)

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question_text = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option = request.form['correct_option']
        quiz_id = request.form['quiz_id']
        
        new_question = Question(
            question=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            quiz_id=quiz_id
        )
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('manage_questions'))
    
    quizzes = Quiz.query.all()
    return render_template('add_question.html', quizzes=quizzes)

@app.route('/manage_scores')
def manage_scores():
    scores = Scores.query.all()
    return render_template('manage_scores.html', scores=scores)


# Run the application
if __name__ == '__main__':
    
    app.run(debug=True)







@app.route('/edit_category/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    if not session.get('user_email',None) or session.get('role', None) != 'admin':
        flash('Unauthorized Access')
        return redirect(url_for('home'))
    
    category = Categories.query.get(id)
    if not category:
        flash('Category not found')
        return redirect(url_for('home'))
    
    if request.method == "GET":
        return render_template('edit_category.html', category=category)
    
    if request.method == "POST":
        name = request.form.get('name', None)
        description = request.form.get('description', None)

        new_category = Categories.query.filter_by(name = name).first()

        if new_category and new_category.id != category.id:
            flash('Category with this name already exists')
            return render_template('edit_category.html', category=category)