# encoding: utf-8

from flask import Flask
from exts import db
import flask
import config
from forms import RegistForm
from models import UserModel,QuestionModel,AnswerModel,CommentModel,ResourceModel
from decorators import login_required
from sqlalchemy import or_
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.config.from_object(config)
api = Api(app)
db.init_app(app)

parser = reqparse.RequestParser()
parser.add_argument('type', type=str)
parser.add_argument('tag', type=str)
parser.add_argument('name', type=str)
parser.add_argument('stage', type=str)
parser.add_argument('userName', type=str)
parser.add_argument('password', type=str)


class Res(Resource):
    def get(self, res_id):
        info = {}
        res = ResourceModel.query.get(res_id)
        if not res:
            return {}
        author_id = res.author_id
        author = UserModel.query.get(author_id).username
        create_time = str(res.create_time.now())
        info[res.id] = {
            'id': res.id,
            'author': author,
            'create_time': create_time,
            'pageviews': res.pageviews,
            'name': res.name,
            'type': res.type,
            'tag': res.tag,
            'stage': res.stage,
        }
        return info

    def delete(self, res_id):
        res = ResourceModel.query.get(res_id)
        db.session.delete(res)
        db.session.commit()
        return 'ok', 200


class ResList(Resource):
    def get(self):
        all_res = ResourceModel.query.all()
        info = {}
        for res in all_res:
            author_id = res.author_id
            author = UserModel.query.get(author_id).username
            create_time = str(res.create_time)
            info[res.id] = {
                'id': res.id,
                'author': author,
                'create_time': create_time,
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
        res = ResourceModel(name=name, tag=tag, type=type, stage=stage)
        res.author = UserModel.query.filter_by(username='zhangchi').first()
        db.session.add(res)
        db.session.commit()
        return 'ok', 200


class Com(Resource):
    def delete(self, com_id):
        com = CommentModel.query.get(com_id)
        db.session.delete(com)
        db.session.commit()
        return 'ok', 200


class ComList(Resource):
    def get(self):
        all_res = ""
        args = parser.parse_args()
        resource_id = args.get("resource_id")
        if resource_id:
            all_res = CommentModel.query.filter_by(resource_id=resource_id).all()
        if not all_res:
            all_res = CommentModel.query.all()
        info = {}
        for res in all_res:
            author_id = res.author_id
            author = UserModel.query.get(author_id).username
            info[res.id] = {
                'id': res.id,
                'content': res.content,
                'create_time': str(res.create_time),
                'resource_id': res.resource_id,
                'author': author
            }
        return info

    def post(self):
        args = parser.parse_args()
        content = args['content']
        resource_id = args['resource_id']
        username = args['author_id']
        comment_model = CommentModel(content=content, resource_id=resource_id)
        comment_model.author = UserModel.query.filter_by(username=username).first()
        db.session.add(comment_model)
        db.session.commit()
        return 'ok', 200


class QingLogin(Resource):
    def post(self):
        args = parser.parse_args()
        password = args['password']
        username = args['userName']
        user = UserModel.query.filter_by(username=username).first()
        if user and user.check_password(password):
            res = {
                'status': 'ok',
                'type': 'ok',
                'currentAuthority': 'admin',

            }
            return res
        else:
            res = {
                'status': 'error',
                'type': 'ok',
                'currentAuthority': 'guest',
            }
            return res


class CurrentUser(Resource):
    def get(self):
        res = {
            'name': 'Serati Ma',
            'avatar': 'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
            'userid': '00000001',
            'email': 'antdesign@alipay.com',
            'signature': '海纳百川，有容乃大',
            'title': '交互专家',
            'group': '蚂蚁金服－某某某事业群－某某平台部－某某技术部－UED',
            'tags': [
                      {
                          'key': '0',
                          'label': '很有想法的',
                      },
                      {
                          'key': '1',
                          'label': '专注设计',
                      },
                      {
                          'key': '2',
                          'label': '辣~',
                      },
                      {
                          'key': '3',
                          'label': '大长腿',
                      },
                      {
                          'key': '4',
                          'label': '川妹子',
                      },
                      {
                          'key': '5',
                          'label': '海纳百川',
                      },
                  ],
            'notifyCount': 12,
            'unreadCount': 11,
            'country': 'China',
            'geographic': {
                            'province': {
                                'label': '浙江省',
                                'key': '330000',
                            },
                            'city': {
                                'label': '杭州市',
                                'key': '330100',
                            },
                        },
            'address': '西湖区工专路 77 号',
            'phone': '0752-268888888',

        }
        return res


api.add_resource(ResList, '/api/res')
api.add_resource(Res, '/api/res/<res_id>')

api.add_resource(ComList, '/api/coms')
api.add_resource(Com, '/api/com/<com_id>')

api.add_resource(QingLogin, '/api/login/account')
api.add_resource(CurrentUser, '/api/currentUser')


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
            user = UserModel(telephone=telephone, username=username, password=password)
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