import os
import markdown

from flask import Flask, redirect, render_template, request, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ebook')
def ebbok():
    return redirect('https://www.amazon.in/dp/B0CRRW2X7W')



from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), nullable=False)
    photo_url = db.Column(db.String(120), nullable=False)
    auth_date = db.Column(db.Integer, nullable=False)
    hash = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer, nullable=False)
    quiz_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Score %r>' % self.score

if 0:
    with app.app_context():
        db.create_all()
        exit()

@app.route('/auth')
def auth():
    try:
        args = request.args
        # check if user exists
        # if not create user
        # and move to /1
        if not User.query.filter_by(id=args['id']).first():
            user = User(id=args['id'], first_name=args['first_name'], last_name=args.get('last_name',''), username=args.get('username',args['id']), photo_url=args.get('photo_url',''), auth_date=args['auth_date'], hash=args['hash'])
            db.session.add(user)
            db.session.commit()
        session['user_id'] = args['id']
        return redirect('/1')
    except Exception as e:
        return str(e)

tks = {
    '1': ['கடவுள் வாழ்த்து / The Praise of God', 'Follow [Pantheism](https://en.m.wikipedia.org/wiki/Pantheism).'],
    '2': ['2. வான்சிறப்பு / The Blessing of Rain','Plant trees to bring the rain.'],
    '3': ['3. நீத்தார் பெருமை / The Greatness of Ascetics','Build [Artificial general intelligence (AGI)](https://en.wikipedia.org/wiki/Artificial_general_intelligence) ASAP.'],
    '4': ['4. அறன் வலியுறுத்தல் / Assertion of the Strength of Virtue','Do good deeds!'],
    '5': ['5. இல்வாழ்க்கை / Domestic Life', 'Marry the right partner.'],
    '6': ['6. வாழ்க்கைத் துணைநலம் / The Worth of a Wife', 'Have more babies.'],
    }
quizzes = {
    '1': ['What is the correct belief system?', ['Hinduism', 'Christianism', 'Muslimism', 'Pantheism'], 4],
    '2': ['How many saplings will you plant today?', ['None', '1-2', '3-4', 'More than 4'], 4],
    '3': ['How many hours will you spend daily to automate your job?', ['None', '15 minutes', '30 minutes', 'More than 1 hour'], 4],
    '4': ['How many good deeds will you do today?', ['None', '1-2', '3-4', 'More than 4'], 4],
    '5': ['How will you choose the right partner?', ['Astrology', 'Family', 'Friends', 'AI'], 4],
    '6': ['How many babies will you have?', ['None', '1-2', '3-4', 'More than 4'], 4],
}
@app.route('/<int:page>')
def page(page):
    max_quiz = len(tks)
    if page>max_quiz:
        return 'Check back tomorrow for more quizzes!'
    page = str(page)
    tk = tks[page]
    tk[1] = markdown.markdown(tk[1])[3:-4]
    quiz = quizzes[page]
    # shuffle the options
    import random
    correct_answer = quiz[1][quiz[2]-1]
    quiz[1] = random.sample(quiz[1], len(quiz[1]))
    quiz[2] = quiz[1].index(correct_answer)+1

    return render_template('h.html', page = page, tk = tk, quiz = quiz, max_quiz = max_quiz)

@app.route('/score')
def score():
    args = request.args
    # if not update score add, else update score
    if Score.query.filter_by(user_id=session.get('user_id','test'), quiz_id=args['quiz_id']).first():
        score = Score.query.filter_by(user_id=session.get('user_id','test'), quiz_id=args['quiz_id']).first()
        score.score = args['score']
        db.session.commit()
        return 'OK'
    else:
        score = Score(user_id=session.get('user_id','test'), score=args['score'], quiz_id=args['quiz_id'])
        db.session.add(score)
        db.session.commit()
        return 'OK'

@app.route('/leader_board')
def leader_board():
    records = Score.query.all()
    html = ''
    for record in records:
        html += f'<p>{record.user_id} {record.score}</p>'
    return html

if __name__ == '__main__':
    app.run(debug=True, )