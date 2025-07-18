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
    # பால்: அறத்துப்பால்
    "1": [
        [
            "கடவுள் வாழ்த்து / The Praise of God",
            "Follow [Pantheism](https://en.m.wikipedia.org/wiki/Pantheism).",
        ],
        [
            "What is the correct belief system?",
            ["Hinduism", "Christianism", "Muslimism", "Pantheism"],
            4,
        ],
    ],
    "2": [
        ["வான்சிறப்பு / The Blessing of Rain", "Plant trees to bring the rain."],
        [
            "How many saplings will you plant today?",
            ["None", "1-2", "3-4", "More than 4"],
            4,
        ],
    ],
    "3": [
        [
            "நீத்தார் பெருமை / The Greatness of Ascetics",
            "Build [Artificial general intelligence "
            "(AGI)](https://en.wikipedia.org/wiki/Artificial_general_intelligence) "
            "ASAP.",
        ],
        [
            "How many hours will you spend daily to automate your job?",
            ["None", "15 minutes", "30 minutes", "More than 1 hour"],
            4,
        ],
    ],
    "4": [
        ["அறன் வலியுறுத்தல் / Assertion of the Strength of Virtue", "Do good deeds!"],
        [
            "How many good deeds will you do today?",
            ["None", "1-2", "3-4", "More than 4"],
            4,
        ],
    ],
    "5": [
        ["இல்வாழ்க்கை / Domestic Life", "Marry the right partner."],
        [
            "How will you choose the right partner?",
            ["Astrology", "Family", "Friends", "AI"],
            4,
        ],
    ],
    "6": [
        ["வாழ்க்கைத் துணைநலம் / The Worth of a Wife", "Have more babies."],
        ["How many babies will you have?", ["None", "1-2", "3-4", "More than 4"], 4],
    ],
    "7": [
        ["மக்கட்பேறு / The Wealth of Children", "Rightly educate your child."],
        [
            "How will you educate your child?",
            ["School", "College", "University", "AI Tutor"],
            4,
        ],
    ],
    "8": [
        ["அன்புடைமை / The Possession of Love", "Embrace Love 🥰"],
        [
            "What might be a reason why most people do not embrace love?",
            [
                "Lack of people to love",
                "Lack of time",
                "Lack of resources",
                "Belief that love is not important",
            ],
            1,
        ],
    ],
    "9": [
        ["விருந்தோம்பல் / Hospitality", "Care your guests."],
        [
            "What is the best way to care your guests?",
            ["Food", "Shelter", "Love", "AI"],
            3,
        ],
    ],
    "10": [
        ["இனியவைகூறல் / The Utterance of Pleasant Words", "Speak pleasant words."],
        [
            "Which words will you use when you are angry?",
            ["Curse", "Polite", "Sarcative", "Expletives"],
            2,
        ],
    ],
    "11": [
        ["செய்ந்நன்றி அறிதல் / Gratitude", "Pay it forward."],
        [
            "How will you show gratitude?",
            ["Thank you", "Gift", "Pray", "Pay it forward"],
            4,
        ],
    ],
    "12": [
        ["நடுவு நிலைமை / Impartiality", "Follow justice."],
        [
            "What will you do when someone is getting bribed?",
            ["Ignore", "Report", "Support", "Take bribe"],
            2,
        ],
    ],
    "13": [
        ["அடக்கமுடைமை / The Possession of Self-restraint", "Have self-control."],
        [
            "If you are very angry, 'having self-control' means you should first:",
            [
                "Express anger loudly",
                "Pause and calm down",
                "Blame others immediately",
                "Seek revenge later",
            ],
            2,
        ],
    ],
    "14": [
        ["ஒழுக்கமுடைமை / The Possession of Decorum", "Always follow decorum."],
        [
            "What will you do when someone is misbehaving?",
            ["Ignore", "Confront", "Encourage", "Misbehave"],
            2,
        ],
    ],
    "15": [
        [
            "பிறனில் விழையாமை / Not coveting another's Wife",
            "Subset of Chapter [18](/18); Never covet others' wife.",
        ],
        [
            "What will you do when someone is flirting with your partner?",
            [
                "Ignore it",
                "Politely intervene and redirect the conversation",
                "Find them another partner",
                "Join the conversation and defuse the flirting with humor",
            ],
            3,
        ],
    ],
    "16": [
        ["பொறையுடைமை / The Possession of Patience, Forbearance", "Be a role model."],
        [
            "How will you respond when someone is being impatient with you?",
            [
                "React with impatience",
                "Stay calm and explain calmly",
                "Ignore their impatience",
                "Become impatient with them",
            ],
            2,
        ],
    ],
    "17": [
        ["அழுக்காறாமை / Not Envying", "Never envy."],
        [
            "How will you respond when someone achieves something you desire?",
            [
                "Feel envious",
                "Congratulate them and work smarter",
                "Try to undermine their achievement",
                "Ignore their achievement",
            ],
            2,
        ],
    ],
    "18": [
        ["வெஃகாமை / Not Coveting", "Never covet."],
        [
            "How will you respond when you covet something someone else has?",
            [
                "Try to take it from them",
                "Be content with what you have",
                "Wish them well and work to acquire it through your own efforts",
                "Ignore your desire",
            ],
            3,
        ],
    ],
    "19": [
        ["புறங்கூறாமை / Not Backbiting", "Never backbite."],
        [
            "How will you respond when someone speaks ill of others in front of you?",
            [
                "Join in and speak ill with them",
                "Politely change the subject",
                "Encourage them to consult with the person directly",
                "Agree with their criticisms",
            ],
            3,
        ],
    ],
    "20": [
        ["பயனில சொல்லாமை / Against Vain Speaking", "Speak wisely!"],
        [
            "How will you respond when someone is speaking frivolously or without purpose?",
            [
                "Join in and speak frivolously",
                "Politely steer the conversation towards a meaningful topic",
                "Listen without engaging",
                "Encourage them to speak more frivolously",
            ],
            2,
        ],
    ],
    "21": [
        ["தீவினையச்சம் / Dread of Evil Deeds", "Avoid evil deeds."],
        [
            "What are the side effects of doing evil deeds?",
            [
                "Misfortune and unhappiness",
                "Lack of inner peace",
                "Loss of reputation",
                "Spiritual degradation",
            ],
            3,
        ],
    ],
    "22": [
        ["ஒப்புரவறிதல் / Duty to Society", "Make helping others your duty."],
        [
            "Why do some people not help others?",
            [
                "Selfishness",
                "Lack of empathy",
                "Fear of being exploited",
                "Busy lifestyles",
            ],
            1,
        ],
    ],
    "23": [
        ["ஈகை / Giving", "Give something useful to the poor."],
        [
            "What are the benefits of giving to the poor?",
            [
                "Improves their living conditions",
                "Encourages societal equality",
                "Boosts the giver’s morale",
                "Creates a sense of community",
            ],
            3,
        ],
    ],
    "24": [
        ["புகழ் / Renown", "Result of moral actions."],
        [
            "How does giving to the poor lead to renown?",
            [
                "Increases social recognition",
                "Builds a positive public image",
                "Inspires others to give",
                "Strengthens community trust",
            ],
            1,
        ],
    ],
    "25": [
        ["அருளுடைமை / Compassion", "Always be compassionate."],
        [
            "Why is compassion important in society?",
            [
                "Promotes emotional support",
                "Helps alleviate suffering",
                "Strengthens community bonds",
                "Encourages empathy and understanding",
            ],
            2,
        ],
    ],
    "26": [
        ["புலால் மறுத்தல் / Abstinence from Flesh", "Be a vegan!"],
        [
            "What are the benefits of adopting a vegan lifestyle?",
            [
                "Improves personal health",
                "Reduces environmental impact",
                "Promotes animal welfare",
                "Supports sustainable food practices",
            ],
            1,
        ],
    ],
    "27": [
        ["தவம் / Penance", "Meditate 🧘"],
        [
            "Why do most people not meditate?",
            [
                "Lack of awareness",
                "Perceived lack of time",
                "Difficulty concentrating",
                "Skepticism about benefits",
            ],
            1,
        ],
    ],
    "28": [
        ["கூடாவொழுக்கம் / Imposture", "Be yourself!"],
        [
            "Why is it important to be yourself?",
            [
                "Promotes authenticity",
                "Builds self-confidence",
                "Encourages personal growth",
                "Attracts genuine relationships",
            ],
            1,
        ],
    ],
    "29": [
        ["கள்ளாமை / The Absence of Fraud", "Never think about fraud!"],
        [
            "What are the consequences of stealing?",
            ["Legal repercussions", "Loss of trust", "Personal guilt", "Social stigma"],
            2,
        ],
    ],
    "30": [
        ["வாய்மை / Veracity", "Speak with compassion."],
        [
            "What are the benefits of speaking with compassion?",
            [
                "Enhances relationships",
                "Enhances personal integrity",
                "Reduces stress from deception",
                "Improves societal standards",
            ],
            1,
        ],
    ],
    "31": [
        ["வெகுளாமை / Restraining Anger", "Restrain anger."],
        [
            "What is the primary benefit of restraining anger?",
            [
                "Improves mental health",
                "Enhances relationships",
                "Promotes better decision-making",
                "Reduces stress",
            ],
            1,
        ],
    ],
    "32": [
        [
            "இன்னாசெய்யாமை / Not doing Evil",
            "1️⃣ Never do harm to any creatures.\n2️⃣ Answer harm with kindness, and then let it go.",
        ],
        [
            "What are the benefits of not doing evil?",
            [
                "Promotes peace and harmony",
                "Builds positive karma",
                "Strengthens moral integrity",
                "Encourages forgiveness and healing",
            ],
            2,
        ],
    ],
    "33": [
        ["கொல்லாமை / Not killing", "Never kill anything."],
        [
            "What are the benefits of not killing?",
            [
                "Promotes respect for all life",
                "Maintains ecological balance",
                "Encourages compassion and empathy",
                "Reduces violence in society",
            ],
            2,
        ],
    ],
    "34": [
        ["நிலையாமை / Instability", "Do good deeds immediately when you have wealth."],
        [
            "Why is it important to do good deeds immediately when you have wealth?",
            [
                "Wealth is transient",
                "Maximizes positive impact",
                "Encourages others to give",
                "Strengthens community bonds",
            ],
            1,
        ],
    ],
    "35": [
        ["துறவு / Renunciation", "Abandon negativity!"],
        [
            "What is the primary benefit of abandoning negativity?",
            [
                "Improves mental health",
                "Enhances personal relationships",
                "Fosters positive thinking",
                "Increases life satisfaction",
            ],
            1,
        ],
    ],
    "36": [
        ["மெய்யுணர்தல் / Truth-Consciousness", "Learn the Truth!"],
        [
            "What is the primary benefit of learning the truth?",
            [
                "Enhances self-awareness",
                "Promotes intellectual growth",
                "Builds honest relationships",
                "Guides moral and ethical decisions",
            ],
            1,
        ],
    ],
    "37": [
        ["அவாவறுத்தல் / Curbing of Desire", "Control your desires!"],
        [
            "What is the primary benefit of controlling your desires?",
            [
                "Increases contentment",
                "Reduces stress and anxiety",
                "Enhances self-discipline",
                "Promotes mindful living",
            ],
            2,
        ],
    ],
    "38": [
        ["ஊழ் / Fate", "Do your duty without expecting the rewards!"],
        [
            "What is the primary benefit of focusing on duty rather than rewards?",
            [
                "Reduces anxiety about outcomes",
                "Increases job satisfaction",
                "Enhances work ethic",
                "Promotes intrinsic motivation",
            ],
            1,
        ],
    ],
    # பால்: பொருட்பால்
    "39": [
        ["இறைமாட்சி / The Greatness of a King", "Convert the harshest criticism to praise!"],
        [
            "What is the primary benefit of a king not showing partiality?",
            [
                "Ensures justice for all",
                "Builds trust among subjects",
                "Strengthens leadership credibility",
                "Promotes social harmony",
            ],
            1,
        ],
    ],
    "40": [
        ["கல்வி / Learning", "Learn good things thoroughly and follow that."],
        [
            "What is the primary benefit of thorough learning?",
            [
                "Deepens understanding",
                "Enhances problem-solving skills",
                "Builds a strong knowledge base",
                "Promotes lifelong learning",
            ],
            1,
        ],
    ],
    "41": [
        [
            "கல்லாமை / Illiteracy",
            "Side effects of not following [the previous chapter](/40).",
        ],
        [
            "What is the primary drawback of illiteracy?",
            [
                "Limits career opportunities",
                "Hinders personal growth",
                "Restricts access to information",
                "Impacts quality of life",
            ],
            4,
        ],
    ],
    "42": [
        ["கேள்வி / Hearing", "Listen to good things."],
        [
            "What is the primary benefit of listening to good things?",
            [
                "Gains wisdom",
                "Improves moral character",
                "Enhances knowledge",
                "Promotes positive thinking",
            ],
            1,
        ],
    ],
    "43": [
        ["அறிவுடைமை / The Possession of Knowledge", "Possess True Knowledge."],
        [
            "What is the primary benefit of possessing true knowledge?",
            [
                "Enables informed decisions",
                "Enhances critical thinking",
                "Builds intellectual confidence",
                "Fosters lifelong learning",
            ],
            1,
        ],
    ],
    "44": [
        ["குற்றங்கடிதல் / The Correction of Faults", "Prevent your wrongs!"],
        [
            "What is the primary benefit of preventing your wrongs?",
            [
                "Promotes growth",
                "Enhances relationships",
                "Improves self-respect",
                "Restores trust in you",
            ],
            1,
        ],
    ],
    "45": [
        ["பெரியாரைத் துணைக்கோடல் / Seeking the Aid of Great Men", "Have a right mentor!"],
        [
            "What is the primary benefit of having a right mentor?",
            [
                "Gains valuable insights",
                "Receives guidance and support",
                "Accelerates personal development",
                "Builds a strong network",
            ],
            2,
        ],
    ],
    "46": [
        ["சிற்றினஞ்சேராமை / Avoiding mean Associations", "Correct negativity!"],
        [
            "What is the primary benefit of correcting negativity?",
            [
                "Maintains positive mindset",
                "Protects personal integrity",
                "Encourages healthy relationships",
                "Promotes personal growth",
            ],
            1,
        ],
    ],
    "47": [
        ["தெரிந்துசெயல்வகை / Acting after due Consideration", "Do thoughtful action!"],
        [
            "What is the primary benefit of acting after due consideration?",
            [
                "Reduces mistakes",
                "Increases success rate",
                "Builds a good reputation",
                "Enhances decision-making skills",
            ],
            1,
        ],
    ],
    "48": [
        [
            "வலியறிதல் / The Knowledge of Power",
            "Know your strength and act accordingly!",
        ],
        [
            "What is the primary benefit of knowing your strength and acting accordingly?",
            [
                "Enhances confidence",
                "Optimizes resource usage",
                "Increases effectiveness",
                "Promotes realistic goal setting",
            ],
            1,
        ],
    ],
    "49": [
        ["காலமறிதல் / Knowing the fitting Time", "Act timely."],
        [
            "What is the primary benefit of acting timely?",
            [
                "Maximizes effectiveness",
                "Reduces missed opportunities",
                "Enhances decision-making",
                "Increases efficiency",
            ],
            2,
        ],
    ],
    "50": [
        [
            "இடனறிதல் / Knowing the Place",
            "Act locally unlike [Zoot Suit Riots (1943)](https://en.wikipedia.org/wiki/Zoot_Suit_Riots)",
        ],
        [
            "What is the primary benefit of acting locally?",
            [
                "Promotes community cohesion",
                "Ensures cultural sensitivity",
                "Optimizes resource allocation",
                "Reduces conflict",
            ],
            4,
        ],
    ],
    "51": [
        ["தெரிந்துதெளிதல் / Selection and Confidence", "Choose your leader confidently!"],
        [
            "What is the primary benefit of choosing your leader confidently?",
            [
                "Ensures strong leadership",
                "Builds trust in governance",
                "Promotes stability and progress",
                "Encourages active participation",
            ],
            1,
        ],
    ],
    "52": [
        ["தெரிந்துவினையாடல் / Selection and Employment", "Assign tasks wisely!"],
        [
            "What is the primary benefit of assigning tasks wisely?",
            [
                "Increases productivity",
                "Ensures task suitability",
                "Enhances team morale",
                "Optimizes resource utilization",
            ],
            1,
        ],
    ],
    "53": [
        ["சுற்றந்தழால் / Cherishing Kinsmen", "Build an emotional companion humanoid for your relatives!"],
        [
            "What is the primary benefit of cherishing kinsmen?",
            [
                "Strengthens family bonds",
                "Provides emotional support",
                "Ensures mutual assistance",
                "Creates a sense of belonging",
            ],
            1,
        ],
    ],
    "54": [
        [
            "பொச்சாவாமை / Unforgetfulness",
            "Be aware!",
        ],
        [
            "What is the primary benefit of being aware?",
            [
                "Reduces stress",
                "Improves mental health",
                "Increases resilience",
                "Improves mindfulness",
            ],
            4,
        ],
    ],
    "55": [
        ["செங்கோன்மை / The Right Sceptre", "Do Greater Good!"],
        [
            "What is the primary benefit of doing greater good?",
            [
                "Ensures justice",
                "Promotes public trust",
                "Encourages ethical leadership",
                "Fosters societal harmony",
            ],
            4,
        ],
    ],
    "56": [
        ["கொடுங்கோன்மை / The Cruel Sceptre", "Avoid all forms of cruelty!"],
        [
            "What is the primary benefit of avoiding cruelty?",
            [
                "Promotes justice",
                "Builds public trust",
                "Encourages humane behavior",
                "Fosters societal harmony",
            ],
            3,
        ],
    ],
    "57": [
        ["வெருவந்தசெய்யாமை / Absence of Terrorism", "End terrorism!"],
        [
            "What is the primary benefit of ending terrorism?",
            [
                "Promotes global security",
                "Fosters societal harmony",
                "Encourages economic growth",
                "Builds public trust",
            ],
            2,
        ],
    ],
    "58": [
        ["கண்ணோட்டம் / Benignity", "Practice Empathy 🤝"],
        [
            "What is the primary benefit of practicing empathy?",
            [
                "Promotes social harmony",
                "Builds strong relationships",
                "Encourages understanding",
                "Enhances personal happiness",
            ],
            4,
        ],
    ],
    "59": [
        ["ஒற்றாடல் / Detectives", "Be a Sherlock 🕵️‍♂️"],
        [
            "What is the primary benefit of having detective skills?",
            [
                "Enhances problem-solving abilities",
                "Improves critical thinking",
                "Strengthens observational skills",
                "Promotes justice",
            ],
            1,
        ],
    ],
    "60": [
        ["ஊக்கமுடைமை / Energy", " Have willpower!"],
        [
            "What is the primary benefit of having willpower?",
            [
                "Achieves difficult goals",
                "Increases resilience",
                "Improves self-discipline",
                "Enhances decision-making",
            ],
            1,
        ],
    ],
    "61": [
        ["மடியின்மை / Unsluggishness", "Be proactive 💪"],
        [
            "What is the primary benefit of being proactive?",
            [
                "Increases productivity",
                "Reduces stress",
                "Enhances problem-solving skills",
                "Builds self-confidence",
            ],
            1,
        ],
    ],
    "62": [
        ["ஆள்வினையுடைமை / Manly Effort", "Always act with sustainable vigor 💪"],
        [
            "What is the primary benefit of always acting with sustainable vigor?",
            [
                "Achieves goals efficiently",
                "Builds resilience",
                "Promotes personal growth",
                "Increases self-confidence and self-esteem",
            ],
            1,
        ],
    ],
    "63": [
        ["இடுக்கணழியாமை / Hopefulness in Trouble", "Face sorrow with smile 🥰"],
        [
            "What is the primary benefit of remaining hopeful in trouble?",
            [
                "Reduces stress",
                "Improves mental health",
                "Increases resilience",
                "Promotes problem-solving",
            ],
            2,
        ],
    ],
    "64": [
        ["அமைச்சு / The Office of Minister of State", "Choose Virtuous Decisions."],
        [
            "What is the primary benefit of choosing virtuous decisions?",
            [
                "Ensures ethical governance",
                "Builds public trust",
                "Promotes justice",
                "Enhances societal welfare",
            ],
            1,
        ],
    ],
    "65": [
        ["சொல்வன்மை / Power of Speech", "Speak precisely."],
        [
            "What is the primary benefit of speaking precisely?",
            [
                "Avoids misunderstandings",
                "Conveys clear messages",
                "Enhances credibility",
                "Promotes effective communication",
            ],
            1,
        ],
    ],
    "66": [
        ["வினைத்தூய்மை / Purity in Action", "Act purely!"],
        [
            "What is the primary benefit of acting purely?",
            [
                "Maintains moral integrity",
                "Builds trust with others",
                "Promotes self-respect",
                "Ensures ethical outcomes",
            ],
            2,
        ],
    ],
    "67": [
        ["வினைத்திட்பம் / Power in Action", "Execute with determination!"],
        [
            "What is the primary benefit of executing with determination?",
            [
                "Increases productivity",
                "Reduces stress",
                "Enhances problem-solving skills",
                "Builds self-confidence",
            ],
            1,
        ],
    ],
    "68": [
        ["வினைசெயல்வகை / Modes of Action", "Plan and Act!"],
        [
            "What is the primary benefit of planning and acting?",
            [
                "Increases success rate",
                "Reduces errors",
                "Enhances efficiency",
                "Promotes goal achievement",
            ],
            1,
        ],
    ],
    "69": [
        ["தூது / The Envoy", "Criticize constructively!"],
        [
            "What is the primary benefit of constructive criticism?",
            [
                "Promotes personal growth",
                "Builds mutual respect",
                "Encourages improvement",
                "Enhances communication",
            ],
            3,
        ],
    ],
    "70": [
        ["மன்னரைச் சேர்ந்தொழுதல் / Conduct in the Presence of the King", "Show respect 🙏"],
        [
            "What is the primary benefit of showing respect in all situations?",
            [
                "Builds positive relationships",
                "Ensures favorable treatment",
                "Demonstrates loyalty",
                "Maintains social order",
            ],
            1,
        ],
    ],
    "71": [
        ["குறிப்பறிதல் / The Knowledge of Indications", "Read faces!"],
        [
            "What is the primary benefit of reading facial expressions?",
            [
                "Detects underlying emotions",
                "Builds empathy",
                "Improves social interactions",
                "Strengthens relationships",
            ],
            4,
        ],
    ],
    "72": [
        ["அவையறிதல் / The Knowledge of the Council Chamber", "Read surroundings!"],
        [
            "What is the primary benefit of reading your surroundings?",
            [
                "Enhances situational awareness",
                "Improves decision-making",
                "Promotes safety",
                "Builds strategic advantage",
            ],
            1,
        ],
    ],
    "73": [
        ["அவையஞ்சாமை / Not to dread the Council", "Speak boldly!"],
        [
            "What is the primary benefit of speaking boldly?",
            [
                "Builds confidence",
                "Gains respect",
                "Encourages open dialogue",
                "Promotes effective communication",
            ],
            1,
        ],
    ],
    "74": [
        ["நாடு / The Land", "Respect the land!"],
        [
            "What is the primary benefit of respecting the land?",
            [
                "Promotes environmental sustainability",
                "Preserves natural resources",
                "Enhances community well-being",
                "Ensures long-term prosperity",
            ],
            1,
        ],
    ],
    "75": [
        ["அரண் / The Fortification", "Build a Fort!"],
        [
            "What is the primary benefit of building a strong foundation in modern times?",
            [
                "Ensures security",
                "Strengthens organizational structure",
                "Supports long-term success",
                "Enhances resilience",
            ],
            1,
        ],
    ],
    "76": [
        ["பொருள்செயல்வகை / Way of Accumulating Wealth", "Honestly accumulate wealth 💰"],
        [
            "What is the primary benefit of honestly accumulating wealth?",
            [
                "Builds a positive reputation",
                "Ensures sustainable growth",
                "Promotes financial stability",
                "Enhances personal integrity",
            ],
            1,
        ],
    ],
    "77": [
        ["படைமாட்சி / The Excellence of an Army", "Maintain Peace 🕊"],
        [
            "What is the primary benefit of maintaining peace?",
            [
                "Ensures societal stability",
                "Promotes economic development",
                "Enhances quality of life",
                "Fosters international cooperation",
            ],
            1,
        ],
    ],
    "78": [
        ["படைச்செருக்கு / Military Spirit", "Build your robot 🤖"],
        [
            "What is the primary benefit of building a robot?",
            [
                "Increases efficiency",
                "Promotes innovation",
                "Supports complex tasks",
                "Enhances productivity",
            ],
            1,
        ],
    ],
    "79": [
        ["நட்பு / Friendship", "Cultivate Friendship 🤗"],
        [
            "What is the primary benefit of cultivating friendship?",
            [
                "Provides emotional support",
                "Enhances well-being",
                "Promotes a sense of belonging",
                "Builds a strong social network",
            ],
            2,
        ],
    ],
    "80": [
        ["நட்பாராய்தல் / Investigation in forming Friendships", "Reform your friends 📝"],
        [
            "What is the primary benefit of reforming friendships?",
            [
                "Creates deeper connections",
                "Promotes mutual respect",
                "Builds a trustworthy network",
                "Enhances social harmony",
            ],
            1,
        ],
    ],
    "81": [
        ["பழைமை / Familiarity", "Protect your friendship 🔒"],
        [
            "What is the primary benefit of protecting your friendship?",
            [
                "Strengthens trust",
                "Enhances emotional support",
                "Maintains long-term bonds",
                "Promotes mutual understanding",
            ],
            3,
        ],
    ],
    "82": [
        ["தீ நட்பு / Evil Friendship", "Prefer solitude over harmful companionship!"],
        [
            "What is the primary benefit of preferring solitude over harmful companionship?",
            [
                "Protects mental health",
                "Promotes personal growth",
                "Avoids negative influences",
                "Enhances self-awareness",
            ],
            3,
        ],
    ],
    "83": [
        [
            "கூடாநட்பு / Unreal Friendship",
            "Side effects of not following [chapter 80](/80)",
        ],
        [
            "What is the primary side effect of not reforming friendships?",
            [
                "Leads to betrayal",
                "Causes emotional distress",
                "Involves false support",
                "Results in trust issues",
            ],
            2,
        ],
    ],
    "84": [
        ["பேதைமை / Folly", "Use [ChatGPT](https://chatgpt.com)!"],
        [
            "What is the primary benefit of using ChatGPT?",
            [
                "Provides accurate information",
                "Enhances learning",
                "Offers quick assistance",
                "Supports decision-making",
            ],
            3,
        ],
    ],
    "85": [
        [
            "புல்லறிவாண்மை / Ignorance",
            "Side effects of not following [the previous chapter](/84)",
        ],
        [
            "What is the primary side effect of not using ChatGPT for assistance?",
            [
                "Leads to misinformation",
                "Slows down learning",
                "Reduces problem-solving efficiency",
                "Increases decision-making errors",
            ],
            3,
        ],
    ],
    "86": [
        ["இகல் / Hostility", "Never hate!"],
        [
            "What is the primary benefit of avoiding hostility?",
            [
                "Promotes peace",
                "Improves mental health",
                "Strengthens relationships",
                "Enhances community harmony",
            ],
            1,
        ],
    ],
    "87": [
        ["பகைமாட்சி / The Might of Hatred", "Be Vigilant!"],
        [
            "What is the primary benefit of being vigilant?",
            [
                "Prevents conflicts",
                "Enhances security",
                "Promotes awareness",
                "Strengthens defense",
            ],
            2,
        ],
    ],
    "88": [
        ["பகைத்திறந்தெரிதல் / Knowing the Quality of Hate", "Befriend Your Enemy!"],
        [
            "What is the primary benefit of befriending your enemy?",
            [
                "Promotes peace",
                "Builds mutual respect",
                "Transforms hostility into friendship",
                "Encourages understanding",
            ],
            3,
        ],
    ],
    "89": [
        [
            "உட்பகை / Enmity within",
            "Side effects of not following [chapter 53](/53)",
        ],
        [
            "What is the primary side effect of not cultivating friendship?",
            [
                "Leads to distrust",
                "Causes isolation",
                "Breeds resentment",
                "Increases conflicts",
            ],
            4,
        ],
    ],
    "90": [
        ["பெரியாரைப் பிழையாமை / Not Offending the Great", "Show respect to the Great!"],
        [
            "What is the primary benefit of showing respect to the great?",
            [
                "Builds positive relationships",
                "Gains valuable mentorship",
                "Earns respect in return",
                "Promotes social harmony",
            ],
            4,
        ],
    ],
    "91": [
        ["பெண்வழிச்சேறல் / Being led by Women", "Avoid dominance in your relationship!"],
        [
            "What is the primary benefit of avoiding dominance in your relationship?",
            [
                "Promotes equality",
                "Enhances mutual respect",
                "Strengthens partnership",
                "Fosters open communication",
            ],
            1,
        ],
    ],
    "92": [
        [
            "வரைவின்மகளிர் / Wanton Women",
            "1️⃣ Avoid Harmful Relationships!\n2️⃣ Prioritize Love over Material Desires",
        ],
        [
            "What is the primary benefit of avoiding harmful relationships?",
            [
                "Protects emotional well-being",
                "Promotes healthy connections",
                "Reduces stress",
                "Encourages personal growth",
            ],
            2,
        ],
    ],
    "93": [
        ["கள்ளுண்ணாமை / Not Drinking Palm-Wine", "Be a teetotaler!"],
        [
            "What is the primary benefit of being a teetotaler?",
            [
                "Improves self-discipline",
                "Promotes self-control",
                "Reduces risk of addiction",
                "Enhances overall well-being",
            ],
            4,
        ],
    ],
    "94": [
        ["சூது / Gambling", "Never gamble!"],
        [
            "What is the primary benefit of not gambling?",
            [
                "Ensures financial stability",
                "Reduces stress",
                "Promotes responsible behavior",
                "Enhances personal well-being",
            ],
            1,
        ],
    ],
    "95": [
        [
            "மருந்து / Medicine",
            "1️⃣ Eat Only When Hungry!\n2️⃣ Take treatment for the root cause!",
        ],
        [
            "What is the primary benefit of eating only when hungry?",
            [
                "Reduces the need for medicine",
                "Prevents disease",
                "Maintains optimal body weight",
                "Enhances overall well-being",
            ],
            2,
        ],
    ],
    "96": [
        ["குடிமை / Nobility", "Be generous!"],
        [
            "What is the primary benefit of being generous?",
            [
                "Builds strong relationships",
                "Enhances personal happiness",
                "Promotes social harmony",
                "Inspires others to give",
            ],
            2,
        ],
    ],
    "97": [
        ["மானம் / Honour", "Hold Honor High!"],
        [
            "What is the primary benefit of holding honor high?",
            [
                "Builds a positive reputation",
                "Earns respect from others",
                "Enhances self-esteem",
                "Promotes ethical behavior",
            ],
            3,
        ],
    ],
    "98": [
        ["பெருமை / Greatness", "Do the Greatest Things!"],
        [
            "What is the primary benefit of striving for greatness?",
            [
                "Achieves significant impact",
                "Inspires others",
                "Builds a lasting legacy",
                "Enhances personal fulfillment",
            ],
            1,
        ],
    ],
    "99": [
        ["சான்றாண்மை / Perfectness", "Strive for Perfection!"],
        [
            "What is the primary benefit of striving for perfection?",
            [
                "Sets high standards",
                "Encourages continuous improvement",
                "Enhances quality of work",
                "Builds a strong reputation",
            ],
            3,
        ],
    ],
    "100": [
        ["பண்புடைமை / Courtesy", "Show Courtesy!"],
        [
            "What is the primary benefit of showing courtesy?",
            [
                "Builds positive relationships",
                "Promotes respect and kindness",
                "Enhances social interactions",
                "Creates a pleasant environment",
            ],
            1,
        ],
    ],
    "101": [
        ["நன்றியில்செல்வம் / Wealth without Benefaction", "Utilize your Wealth!"],
        [
            "What is the primary benefit of utilizing your wealth?",
            [
                "Supports charitable causes",
                "Promotes social good",
                "Enhances personal satisfaction",
                "Contributes to community development",
            ],
            3,
        ],
    ],
    "102": [
        ["நாணுடைமை / Shame", "The action to do when not following [Chapter 4](/4)"],
        [
            "What is the next action to take when not doing good deeds?",
            [
                "Acknowledge your mistakes",
                "Seek forgiveness",
                "Commit to doing good deeds",
                "Reflect on your actions",
            ],
            3,
        ],
    ],
    "103": [
        ["குடிசெயல்வகை / The Way of Maintaining the Family", "Work Smart, Not Hard!"],
        [
            "What is the primary benefit of working smart instead of hard?",
            [
                "Increases efficiency",
                "Reduces stress",
                "Optimizes time management",
                "Enhances work-life balance",
            ],
            2,
        ],
    ],
    "104": [
        ["உழவு / Farming", "Automate the Farming!"],
        [
            "What is the primary benefit of automating farming?",
            [
                "Increases productivity",
                "Reduces labor costs",
                "Enhances efficiency",
                "Promotes sustainable practices",
            ],
            1,
        ],
    ],
    "105": [
        ["நல்குரவு / Poverty", "Live in harmony with nature!"],
        [
            "What is the primary benefit of living in harmony with nature?",
            [
                "Reduces environmental impact",
                "Promotes sustainability",
                "Enhances well-being",
                "Fosters community resilience",
            ],
            2,
        ],
    ],
    "106": [
        [
            "இரவு / Mendicancy",
            "[Join](https://beggarscorporation.com/join-us.html) [Beggar's Corporation!](https://beggarscorporation.com/)",
        ],
        [
            "What is the primary benefit of joining Beggar's Corporation?",
            [
                "Reduces poverty and creates responsibility",
                "Provides support and resources",
                "Promotes dignity and respect",
                "Creates a sense of community",
            ],
            1,
        ],
    ],
    "107": [
        [
            "இரவச்சம் / The Dread of Mendicancy",
            "Side effects of not following [the previous chapter](/106)",
        ],
        [
            "What is the primary side effect of not reducing poverty and creating responsibility?",
            [
                "Increases dependence on charity",
                "Promotes long-term poverty",
                "Reduces self-sufficiency",
                "Fails to create accountability",
            ],
            2,
        ],
    ],
    "108": [
        [
            "கயமை / Baseness",
            "Side effects of not following [chapter 4](/4)",
        ],
        [
            "What is the primary side effect of not doing good deeds?",
            [
                "Decreases moral integrity",
                "Promotes selfish behavior",
                "Damages reputation",
                "Reduces trust from others",
            ],
            1,
        ],
    ],
    # பால்: காமத்துப்பால்
    "109": [
        ["தகையணங்குறுத்தல் / The Pre-marital Love", "Cherish heartfelt connection 🫶"],
        [
            "What is the primary benefit of cherishing heartfelt connections?",
            [
                "Strengthens emotional bonds",
                "Ensures mutual respect",
                "Fosters trust and understanding",
                "Enhances emotional well-being",
            ],
            1,
        ],
    ],
    "110": [
        ["குறிப்பறிதல் / Recognition of the Signs", "Speak with eyes 😍"],
        [
            "What is the primary benefit of recognizing signs in love?",
            [
                "Enhances emotional connection",
                "Strengthens silent communication",
                "Enhances relationship dynamics",
                "Encourages empathy",
            ],
            1,
        ],
    ],
    "111": [
        ["புணர்ச்சிமகிழ்தல் / Rejoicing in the Embrace", "Embrace your partner 🤗"],
        [
            "What is the primary benefit of rejoicing in the embrace?",
            [
                "Deepens physical intimacy",
                "Strengthens emotional bonds",
                "Fosters a sense of security",
                "Enhances mutual affection",
            ],
            2,
        ],
    ],
    "112": [
        ["நலம்புனைந்துரைத்தல் / The Praise of her Beauty", "Admire natural beauty 🌹"],
        [
            "What is the primary benefit of admiring natural beauty?",
            [
                "Boosts self-esteem",
                "Strengthens emotional connection",
                "Enhances appreciation for partner",
                "Fosters mutual respect",
            ],
            3,
        ],
    ],
    "113": [
        [
            "காதற்சிறப்புரைத்தல் / Declaration of Love's special Excellence",
            "Embrace oneness 💞",
        ],
        [
            "What is the primary benefit of embracing oneness in love?",
            [
                "Deepens mutual commitment",
                "Strengthens emotional unity",
                "Fosters a sense of belonging",
                "Encourages unwavering support",
            ],
            2,
        ],
    ],
    "114": [
        ["நாணுத்துறவுரைத்தல் / The Abandonment of Reserve", "Build Love Guru Bot 🤖"],
        [
            "What is the primary benefit of building Love Guru Bot?",
            [
                "Provides relationship advice",
                "Facilitates better communication",
                "Encourages emotional expression",
                "Offers personalized tips",
            ],
            2,
        ],
    ],
    "115": [
        [
            "அலரறிவுறுத்தல் / The Announcement of the Rumour",
            "Side effects of not following [the previous chapter](/114)",
        ],
        [
            "What is the primary side effect of rumors spreading?",
            [
                "Damages reputation",
                "Creates mistrust",
                "Leads to misunderstandings",
                "Weakens relationships",
            ],
            1,
        ],
    ],
    "116": [
        ["பிரிவாற்றாமை / Separation unendurable", "Create your AR Avatar 🌐"],
        [
            "What is the primary benefit of creating your AR Avatar?",
            [
                "Bridges emotional distance",
                "Provides a personalized digital presence",
                "Facilitates virtual interaction",
                "Helps maintain emotional connection",
            ],
            1,
        ],
    ],
    "117": [
        [
            "படர்மெலிந்திரங்கல் / Complainings",
            "Side effects of not following [the previous chapter](/116)",
        ],
        [
            "What is the primary consequence of self-complaining?",
            [
                "Deepens emotional suffering",
                "Leads to self-pity",
                "Weakens self-resolve",
                "Increases feelings of helplessness",
            ],
            1,
        ],
    ],
    "118": [
        [
            "கண்விதுப்பழிதல் / Eyes consumed with Grief",
            "Side effects of not seeing [the previous chapter](/117)",
        ],
        [
            "What is the primary side effect of eyes consumed with grief?",
            [
                "Leads to overwhelming sorrow",
                "Causes emotional exhaustion",
                "Deepens feelings of despair",
                "Weakens emotional resilience",
            ],
            3,
        ],
    ],
    "119": [
        [
            "பசப்புறுபருவரல் / The Pallid Hue",
            "Side effects of not following [the previous chapter](/118)",
        ],
        [
            "What is the primary emotional impact of the pallid hue caused by grief?",
            [
                "Intensifies feelings of despair",
                "Reflects deep emotional pain",
                "Leads to social withdrawal",
                "Triggers self-reflection",
            ],
            1,
        ],
    ],
    "120": [
        ["தனிப்படர்மிகுதி / The Solitary Anguish", "Join in your partner's journey 💑"],
        [
            "What is the primary benefit of joining in your partner's journey?",
            [
                "Strengthens emotional bonds",
                "Fosters mutual understanding",
                "Reduces feelings of isolation",
                "Enhances relationship resilience",
            ],
            3,
        ],
    ],
    "121": [
        [
            "நினைந்தவர்புலம்பல் / Sad Memories",
            "Side effects of not following [the previous chapter](/120)",
        ],
        [
            "What is the primary side effect of dwelling on sad memories?",
            [
                "Increases emotional pain",
                "Prolongs feelings of loneliness",
                "Hinders emotional healing",
                "Deepens feelings of regret",
            ],
            3,
        ],
    ],
    "122": [
        [
            "கனவுநிலையுரைத்தல் / The Visions of the Night",
            "Side effects of not dreaming [the previous chapter](/121)",
        ],
        [
            "What is the primary side effect of disturbing dreams?",
            [
                "Disrupts emotional stability",
                "Leads to emotional exhaustion",
                "Affects overall well-being",
                "Causes persistent anxiety",
            ],
            1,
        ],
    ],
    "123": [
        [
            "பொழுதுகண்டிரங்கல் / Lamentations at Eventide",
            "Side effects of not following [the previous chapter](/122)",
        ],
        [
            "What is the primary side effect of lamenting at eventide?",
            [
                "Prolongs emotional distress",
                "Disrupts evening routines",
                "Deepens feelings of loneliness",
                "Hinders emotional recovery",
            ],
            3,
        ],
    ],
    "124": [
        [
            "உறுப்புநலனழிதல் / Wasting Away",
            "Side effects of not addressing [the previous chapter](/123)",
        ],
        [
            "What is the primary side effect of wasting away?",
            [
                "Causes both physical and mental deterioration",
                "Leads to chronic fatigue",
                "Accelerates overall decline",
                "Triggers severe physical exhaustion",
            ],
            3,
        ],
    ],
    "125": [
        [
            "நெஞ்சொடுகிளத்தல் / Soliloquy",
            "Side effects of not following [the previous chapter](/124)",
        ],
        [
            "What is the primary side effect of engaging in a soliloquy?",
            [
                "Intensifies feelings of isolation",
                "Increases emotional turmoil",
                "Deepens self-reflection",
                "Weakens social connections",
            ],
            2,
        ],
    ],
    "126": [
        [
            "நிறையழிதல் / Reserve Overcome",
            "Side effects of ignoring [the previous chapter](/125)",
        ],
        [
            "What is the primary side effect of overcoming reserve?",
            [
                "Leads to emotional vulnerability",
                "Breaks down personal boundaries",
                "Increases the risk of regret",
                "Weakens self-control",
            ],
            1,
        ],
    ],
    "127": [
        [
            "அவர்வயின்விதும்பல் / Mutual Desire",
            "Side effects of not following [the previous chapter](/126)",
        ],
        [
            "What is the primary side effect of unfulfilled mutual desire?",
            [
                "Leads to emotional frustration",
                "Creates a sense of longing",
                "Weakens the bond between partners",
                "Increases emotional distance",
            ],
            1,
        ],
    ],
    "128": [
        ["குறிப்பறிவுறுத்தல் / The Reading of the Signs", "Decipher subtle signals 🧐"],
        [
            "What is the primary benefit of deciphering subtle signals in a relationship?",
            [
                "Enhances communication",
                "Deepens emotional understanding",
                "Prevents misunderstandings",
                "Strengthens the bond between partners",
            ],
            2,
        ],
    ],
    "129": [
        ["புணர்ச்சிவிதும்பல் / Desire for Reunion", "Celebrate togetherness always 💑"],
        [
            "What is the primary benefit of celebrating togetherness in a relationship?",
            [
                "Reinforces shared values",
                "Creates lasting memories",
                "Increases emotional intimacy",
                "Builds a strong foundation of trust",
            ],
            3,
        ],
    ],
    "130": [
        [
            "நெஞ்சொடுபுலத்தல் / Expostulation with Oneself",
            "Side effects of not following [the previous chapter](/129)",
        ],
        [
            "What is the primary side effect of expostulating with oneself?",
            [
                "Increases self-doubt",
                "Amplifies emotional turmoil",
                "Weakens mental clarity",
                "Leads to indecision",
            ],
            2,
        ],
    ],
    "131": [
        ["புலவி / Pouting", "Respect emotional expressions 💖"],
        [
            "What is the primary benefit of respecting emotional expressions in a relationship?",
            [
                "Strengthens emotional intimacy",
                "Fosters mutual understanding",
                "Encourages open communication",
                "Builds trust and respect",
            ],
            2,
        ],
    ],
    "132": [
        ["புலவி நுணுக்கம் / Feigned Anger", "Cultivate understanding playfulness 💑"],
        [
            "What is the primary benefit of cultivating understanding playfulness in a relationship?",
            [
                "Strengthens emotional bonds",
                "Enhances mutual trust",
                "Encourages open communication",
                "Fosters a joyful connection",
            ],
            4,
        ],
    ],
    "133": [
        ["ஊடலுவகை / The Pleasures of Temporary Variance", "Create life 💞"],
        [
            "What is the primary benefit of creating life in a relationship?",
            [
                "Deepens emotional intimacy",
                "Fosters a sense of shared purpose",
                "Strengthens the relationship foundation",
                "Adds excitement and passion",
            ],
            2,
        ],
    ],
}


@app.route('/<int:page>')
@app.route('/c<int:page>')
def page(page):
    max_quiz = len(tks)
    if page>max_quiz:
        return 'Check back tomorrow for more quizzes!'
    page = str(page)
    tk,quiz = tks[page]
    if '\n' in tk[1]:
        tk[1] = tk[1].replace('\n', '<br>')
        tk[1] = '<br>'+tk[1]
    tk[1] = markdown.markdown(tk[1])[3:-4]
    # shuffle the options
    import random
    correct_answer = quiz[1][quiz[2]-1]
    quiz[1] = random.sample(quiz[1], len(quiz[1]))
    quiz[2] = quiz[1].index(correct_answer)+1
    img_extension = ''
    if os.path.exists(f'static/imgs/{page}.jpeg'):
        img_extension = '.jpeg'
    elif os.path.exists(f'static/imgs/{page}.png'):
        img_extension = '.png'

    return render_template('h.html', page = page, tk = tk, quiz = quiz, max_quiz = max_quiz, img_extension = img_extension)

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
