# encoding: utf-8

from flask import Flask
from exts import db
import flask
import config
from forms import RegistForm
from models import UserModel,QuestionModel,AnswerModel,CommentModel,ResourceModel
from decorators import login_required
from sqlalchemy import or_
from flask_restful import Api, Resource

app = Flask(__name__)
app.config.from_object(config)
api = Api(app)
db.init_app(app)


class Res(Resource):
    def get(self, res_id):
        info = {}
        res = ResourceModel.query.get(res_id)
        if not res:
            return {}
        info[res.id] = {
            'id': res.id,
            'author_id': res.author_id,
            'create_time': res.create_time,
            'pageviews': res.pageviews,
            'name': res.name,
            'type': res.type,
            'tag': res.tag,
            'stage': res.stage,
        }
        return info

    def delete(self, res_id):
        res = ResourceModel.query.filter(ResourceModel.id == res_id).first()
        db.session.delete(res)
        db.session.commit()
        return 'ok', 200


class ResList(Resource):
    def get(self):
        all_res = ResourceModel.query.all()
        info = {}
        for res in all_res:
            info[res.id] = {
                'id': res.id,
                'author_id': res.author_id,
                'create_time': res.create_time,
                'pageviews': res.pageviews,
                'name': res.name,
                'type': res.type,
                'tag': res.tag,
                'stage': res.stage,
            }
        return info

    def post(self):
        args = parser.parse_args()
        type = args['type']
        tag = args['tag']
        name = args['name']
        stage = args['stage']
        question_model = ResourceModel(name=name, tag=tag, type=type, stage=stage)
        question_model.author = 'admin'
        db.session.add(question_model)
        db.session.commit()
        return 'sucess', 200


class Com(Resource):
    def get(self):
        pass


class ComList(Resource):
    pass


api.add_resource(ResList, '/api/res')
api.add_resource(Res, '/api/res/<res_id>')

api.add_resource(ComList, '/api/coms')
api.add_resource(Com, '/api/com/<com_id>')


@app.route('/')
def index():
    context = {
        'questions': QuestionModel.query.all()
    }
    return flask.render_template('index.html',**context)


@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if flask.request.method == 'GET':
        return flask.render_template('question.html')
    else:
        title = flask.request.form.get('title')
        content = flask.request.form.get('content')
        question_model = QuestionModel(title=title,content=content)
        question_model.author = flask.g.user
        db.session.add(question_model)
        db.session.commit()
        return flask.redirect(flask.url_for('index'))


@app.route('/d/<id>/')
def detail(id):
    question_model = QuestionModel.query.get(id)
    return flask.render_template('detail.html',question=question_model)


@app.route('/comment/',methods=['POST'])
@login_required
def comment():
    question_id = flask.request.form.get('question_id')
    content = flask.request.form.get('content')
    answer_model = AnswerModel(content=content)
    answer_model.author = flask.g.user
    answer_model.question = QuestionModel.query.get(question_id)
    db.session.add(answer_model)
    db.session.commit()
    return flask.redirect(flask.url_for('detail',id=question_id))


@app.route('/search/')
def search():
    q = flask.request.args.get('q')
    questions = QuestionModel.query.filter(or_(QuestionModel.title.contains(q),QuestionModel.content.contains(q)))
    context = {
        'questions': questions
    }
    return flask.render_template('index.html',**context)


@app.route('/login/',methods=['GET','POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    else:
        telephone = flask.request.form.get('telephone')
        password = flask.request.form.get('password')
        user = UserModel.query.filter_by(telephone=telephone).first()
        if user and user.check_password(password):
            flask.session['id'] = user.id
            flask.g.user = user
            return flask.redirect(flask.url_for('index'))
        else:
            return u'用户名或密码错误！'


@app.route('/logout/', methods=['GET'])
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('login'))


@app.route('/regist/', methods=['GET','POST'])
def regist():
    if flask.request.method == 'GET':
        return flask.render_template('regist.html')
    else:
        form = RegistForm(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = UserModel(telephone=telephone,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return flask.redirect(flask.url_for('login'))


@app.before_request
def before_request():
    id = flask.session.get('id')
    if id:
        user = UserModel.query.get(id)
        flask.g.user = user


@app.context_processor
def context_processor():
    if hasattr(flask.g, 'user'):
        return {"user": flask.g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)