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

tks = {'1': [['கடவுள் வாழ்த்து / The Praise of God',
        'Follow [Pantheism](https://en.m.wikipedia.org/wiki/Pantheism).'],
       ['What is the correct belief system?',
        ['Hinduism', 'Christianism', 'Muslimism', 'Pantheism'],
        4]],
 '2': [['வான்சிறப்பு / The Blessing of Rain',
        'Plant trees to bring the rain.'],
       ['How many saplings will you plant today?',
        ['None', '1-2', '3-4', 'More than 4'],
        4]],
 '3': [['நீத்தார் பெருமை / The Greatness of Ascetics',
        'Build [Artificial general intelligence '
        '(AGI)](https://en.wikipedia.org/wiki/Artificial_general_intelligence) '
        'ASAP.'],
       ['How many hours will you spend daily to automate your job?',
        ['None', '15 minutes', '30 minutes', 'More than 1 hour'],
        4]],
 '4': [['அறன் வலியுறுத்தல் / Assertion of the Strength of Virtue',
        'Do good deeds!'],
       ['How many good deeds will you do today?',
        ['None', '1-2', '3-4', 'More than 4'],
        4]],
 '5': [['இல்வாழ்க்கை / Domestic Life', 'Marry the right partner.'],
       ['How will you choose the right partner?',
        ['Astrology', 'Family', 'Friends', 'AI'],
        4]],
 '6': [['வாழ்க்கைத் துணைநலம் / The Worth of a Wife', 'Have more babies.'],
       ['How many babies will you have?',
        ['None', '1-2', '3-4', 'More than 4'],
        4]],
 '7': [['மக்கட்பேறு / The Wealth of Children', 'Educate your child.'],
       ['How will you educate your child?',
        ['School', 'College', 'University', 'AI'],
        4]],
 '8': [['அன்புடைமை / The Possession of Love', 'Show compassion 🥰'],
       ['What might be a reason why most people do not show compassion?',
        ['Lack of understanding or awareness',
         'Selfishness or self-centeredness',
         'Fear of vulnerability',
         'Belief that compassion is not important'],
        1]],
 '9': [['விருந்தோம்பல் / Hospitality', 'Care your guests.'],
       ['What is the best way to care your guests?',
        ['Food', 'Shelter', 'Love', 'AI'],
        3]],
 '10': [['இனியவைகூறல் / The Utterance of Pleasant Words',
         'Speak pleasant words.'],
        ['Which words will you use when you are angry?',
         ['Curse', 'Polite', 'Sarcative', 'Expletives'],
         2]],
'11': [['செய்ந்நன்றி அறிதல் / Gratitude','Give [AppreciCoin](https://shareg.pt/56ZzUra)'],['How will you show gratitude?',['Thank you','Gift','Hug','Give AppreciCoin'],4]],
'12': [['நடுவு நிலைமை / Impartiality', 'Follow justice.'], ['What will you do when someone is getting bribed?',['Ignore','Report','Support','Take bribe'],2]],
'13':[['அடக்கமுடைமை / The Possession of Self-restraint','Be humble.'],['What will you do when someone is boasting?',['Ignore','Confront','Encourage','Boast'],1]],
'14':[['ஒழுக்கமுடைமை / The Possession of Decorum','Be disciplined.'],['What will you do when someone is misbehaving?',['Ignore','Confront','Encourage','Misbehave'],2]],
'15':[['பிறனில் விழையாமை / Not coveting another\'s Wife','Subset of Chapter [18](/18); Don\'t covet others\' wife.'],['What will you do when someone is flirting with your partner?', ['Ignore it', 'Politely intervene and redirect the conversation', 'Find them another partner', 'Join the conversation and defuse the flirting with humor'], 3]],
   '16': [['பொறையுடைமை / The Possession of Patience, Forbearance', 'Be a role model.'], ['How will you respond when someone is being impatient with you?', ['React with impatience', 'Stay calm and explain calmly', 'Ignore their impatience', 'Become impatient with them'], 2]],
'17': [['அழுக்காறாமை / Not Envying', 'Don\'t envy.'], ['How will you respond when someone achieves something you desire?', ['Feel envious', 'Congratulate them and work smarter', 'Try to undermine their achievement', 'Ignore their achievement'], 2]],
'18': [['வெஃகாமை / Not Coveting', 'Avoid coveting.'], ['How will you respond when you covet something someone else has?', ['Try to take it from them', 'Be content with what you have', 'Wish them well and work to acquire it through your own efforts', 'Ignore your desire'], 3]],
'19': [['புறங்கூறாமை / Not Backbiting', 'Avoid backbiting.'], ['How will you respond when someone speaks ill of others in front of you?', ['Join in and speak ill with them', 'Politely change the subject', 'Encourage them to consult with the person directly', 'Agree with their criticisms'], 3]],
'20': [['பயனில சொல்லாமை / Against Vain Speaking', 'Speak wisely!'], ['How will you respond when someone is speaking frivolously or without purpose?', ['Join in and speak frivolously', 'Politely steer the conversation towards a meaningful topic', 'Listen without engaging', 'Encourage them to speak more frivolously'], 2]],
'21': [['தீவினையச்சம் / Dread of Evil Deeds', 'Avoid evil deeds.'], ['What are the side effects of doing evil deeds?', ['Misfortune and unhappiness', 'Lack of inner peace', 'Loss of reputation', 'Spiritual degradation'], 3]],
'22': [['ஒப்புரவறிதல் / Duty to Society', 'Help others.'], ['Why do some people not help others?', ['Selfishness', 'Lack of empathy', 'Fear of being exploited', 'Busy lifestyles'], 1]],
'23': [['ஈகை / Giving', 'Give something useful to the poor.'], ['What are the benefits of giving to the poor?', ['Improves their living conditions', 'Encourages societal equality', 'Boosts the giver’s morale', 'Creates a sense of community'], 3]],
'24': [['புகழ் / Renown', 'Result of the [previous chapter](/23).'], ['How does giving to the poor lead to renown?', ['Increases social recognition', 'Builds a positive public image', 'Inspires others to give', 'Strengthens community trust'], 1]],
'25': [['அருளுடைமை / Compassion', 'Be compassionate.'], ['Why is compassion important in society?', ['Promotes emotional support', 'Helps alleviate suffering', 'Strengthens community bonds', 'Encourages empathy and understanding'], 2]],
'26': [['புலால் மறுத்தல் / Abstinence from Flesh', 'Be a vegan!'], ['What are the benefits of adopting a vegan lifestyle?', ['Improves personal health', 'Reduces environmental impact', 'Promotes animal welfare', 'Supports sustainable food practices'], 1]],
'27': [['தவம் / Penance', 'Meditate 🧘'], ['Why do most people not meditate?', ['Lack of awareness', 'Perceived lack of time', 'Difficulty concentrating', 'Skepticism about benefits'], 1]],
'28': [['கூடாவொழுக்கம் / Imposture', 'Be yourself!'], ['Why is it important to be yourself?', ['Promotes authenticity', 'Builds self-confidence', 'Encourages personal growth', 'Attracts genuine relationships'], 1]],
'29': [['கள்ளாமை / The Absence of Fraud', "Don't steal!"], ['What are the consequences of stealing?', ['Legal repercussions', 'Loss of trust', 'Personal guilt', 'Social stigma'], 2]],
}

@app.route('/<int:page>')
def page(page):
    max_quiz = len(tks)
    if page>max_quiz:
        return 'Check back tomorrow for more quizzes!'
    page = str(page)
    tk,quiz = tks[page]
    tk[1] = markdown.markdown(tk[1])[3:-4]
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