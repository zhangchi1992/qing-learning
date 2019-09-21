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
            "name": "Qing Xiaoyun",
            "avatar": "https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png",
            "userid": "00000001",
            "email": "antdesign@alipay.com",
            "signature": "海纳百川，有容乃大",
            "title": "交互专家",
            "group": "蚂蚁金服－某某某事业群－某某平台部－某某技术部－UED",
            "tags": [{
                "key": "0",
                "label": "很有想法的"
            }, {
                "key": "1",
                "label": "专注设计"
            }, {
                "key": "2",
                "label": "辣~"
            }, {
                "key": "3",
                "label": "大长腿"
            }, {
                "key": "4",
                "label": "川妹子"
            }, {
                "key": "5",
                "label": "海纳百川"
            }],
            "notifyCount": 12,
            "unreadCount": 11,
            "country": "China",
            "geographic": {
                "province": {
                    "label": "浙江省",
                    "key": "330000"
                },
                "city": {
                    "label": "杭州市",
                    "key": "330100"
                }
            },
            "address": "西湖区工专路 77 号",
            "phone": "0752-268888888"
        }
        return res


class GetList(Resource):
    def get(self):
        res = [{
            "id": "fake-list-0",
            "owner": "付小小",
            "title": "青云sdwan产品培训--part1",
            "avatar": "https://gw.alipayobjects.com/zos/rmsportal/zOsKZmFRdUtvpqCImOVY.png",
            "cover": "https://gw.alipayobjects.com/zos/rmsportal/uMfMFlvUuceEyPpotzlq.png",
            "status": "active",
            "percent": 84,
            "logo": "https://gw.alipayobjects.com/zos/rmsportal/zOsKZmFRdUtvpqCImOVY.png",
            "href": "/",
            "updatedAt": 1569046638349,
            "createdAt": 1569046638349,
            "type": "CI / CD",
            "count": 43,
            "description": "在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。",
            "activeUser": 198666,
            "newUser": 1139,
            "star": 147,
            "like": 105,
            "message": 14,
            "content": "Continuous Integration，为持续集成。即在代码构建过程中持续地进行代码的集成、构建、以及自动化测试等；有了 CI 工具，我们可以在代码提交的过程中通过单元测试等尽早地发现引入的错误。",
            "members": [{
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/ZiESqWwCXBRQoaPONSJe.png",
                "name": "曲丽丽",
                "id": "member1"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/tBOxZPlITHqwlGjsJWaF.png",
                "name": "王昭君",
                "id": "member2"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/sBxjgqiuHMGRkIjqlQCd.png",
                "name": "董娜娜",
                "id": "member3"
            }]
        }, {
            "id": "fake-list-1",
            "owner": "曲丽丽",
            "title": "青云KubeSphere培训--part1",
            "avatar": "https://gw.alipayobjects.com/zos/rmsportal/siCrBXXhmvTQGWPNLBow.png",
            "cover": "https://gw.alipayobjects.com/zos/rmsportal/iZBVOIhGJiAnhplqjvZW.png",
            "status": "exception",
            "percent": 59,
            "logo": "https://gw.alipayobjects.com/zos/rmsportal/siCrBXXhmvTQGWPNLBow.png",
            "href": "/",
            "updatedAt": 1569039438349,
            "createdAt": 1569039438349,
            "type": "k8s",
            "count": 101,
            "description": "在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。",
            "activeUser": 117704,
            "newUser": 1473,
            "star": 192,
            "like": 117,
            "message": 17,
            "content": "Kubernetes（简称K8S） 是Google开源的分布式的容器管理平台，方便我们在服务器集群中管理我们容器化应用。",
            "members": [{
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/ZiESqWwCXBRQoaPONSJe.png",
                "name": "曲丽丽",
                "id": "member1"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/tBOxZPlITHqwlGjsJWaF.png",
                "name": "王昭君",
                "id": "member2"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/sBxjgqiuHMGRkIjqlQCd.png",
                "name": "董娜娜",
                "id": "member3"
            }]
        }, {
            "id": "fake-list-2",
            "owner": "林东东",
            "title": "青云sdn培训--part1",
            "avatar": "https://gw.alipayobjects.com/zos/rmsportal/kZzEzemZyKLKFsojXItE.png",
            "cover": "https://gw.alipayobjects.com/zos/rmsportal/iXjVmWVHbCJAyqvDxdtx.png",
            "status": "normal",
            "percent": 73,
            "logo": "https://gw.alipayobjects.com/zos/rmsportal/kZzEzemZyKLKFsojXItE.png",
            "href": "/",
            "updatedAt": 1569032238349,
            "createdAt": 1569032238349,
            "type": "DevOps",
            "count": 159,
            "description": "在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。",
            "activeUser": 130817,
            "newUser": 1502,
            "star": 188,
            "like": 125,
            "message": 20,
            "content": "根据devopsdotcom做的\"2017年DevOps使用情况和趋势\"的报告，DevOps的使用在过去几年一直持续增长，尤其是2016年以来。唯一的问题是小团队发现开始启用devops颇有难度。",
            "members": [{
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/ZiESqWwCXBRQoaPONSJe.png",
                "name": "曲丽丽",
                "id": "member1"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/tBOxZPlITHqwlGjsJWaF.png",
                "name": "王昭君",
                "id": "member2"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/sBxjgqiuHMGRkIjqlQCd.png",
                "name": "董娜娜",
                "id": "member3"
            }]
        }, {
            "id": "fake-list-3",
            "owner": "周星星",
            "title": "青云桌面云培训--part1",
            "avatar": "https://gw.alipayobjects.com/zos/rmsportal/ComBAopevLwENQdKWiIn.png",
            "cover": "https://gw.alipayobjects.com/zos/rmsportal/gLaIAoVWTtLbBWZNYEMg.png",
            "status": "active",
            "percent": 99,
            "logo": "https://gw.alipayobjects.com/zos/rmsportal/ComBAopevLwENQdKWiIn.png",
            "href": "/",
            "updatedAt": 1569025038349,
            "createdAt": 1569025038349,
            "type": "GitOps",
            "count": 217,
            "description": "在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。",
            "activeUser": 132751,
            "newUser": 1349,
            "star": 104,
            "like": 180,
            "message": 13,
            "content": "GitOps 的概念最初来源于 Weaveworks 的联合创始人 Alexis 在 2017 年 8 月发表的一篇博客 GitOps - Operations by Pull Request。文章介绍了 Weaveworks 的工程师如何以 Git 作为事实的唯一真实来源，部署、管理和监控基于 Kubernetes 的 SaaS 应用。",
            "members": [{
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/ZiESqWwCXBRQoaPONSJe.png",
                "name": "曲丽丽",
                "id": "member1"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/tBOxZPlITHqwlGjsJWaF.png",
                "name": "王昭君",
                "id": "member2"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/sBxjgqiuHMGRkIjqlQCd.png",
                "name": "董娜娜",
                "id": "member3"
            }]
        }, {
            "id": "fake-list-4",
            "owner": "吴加好",
            "title": "青云sdwan产品培训--part2",
            "avatar": "https://gw.alipayobjects.com/zos/rmsportal/nxkuOJlFJuAUhzlMTCEe.png",
            "cover": "https://gw.alipayobjects.com/zos/rmsportal/gLaIAoVWTtLbBWZNYEMg.png",
            "status": "exception",
            "percent": 89,
            "logo": "https://gw.alipayobjects.com/zos/rmsportal/nxkuOJlFJuAUhzlMTCEe.png",
            "href": "/",
            "updatedAt": 1569017838349,
            "createdAt": 1569017838349,
            "type": "Istio",
            "count": 275,
            "description": "在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。",
            "activeUser": 114628,
            "newUser": 1702,
            "star": 124,
            "like": 165,
            "message": 13,
            "content": "在持续集成环境中，开发人员将会频繁的提交代码到主干。这些新提交在最终合并到主线之前，都需要通过编译和自动化测试流进行验证。这样做是基于之前持续集成过程中很重视自动化测试验证结果，以保障所有的提交在合并主线之后的质量问题，对可能出现的一些问题进行预警",
            "members": [{
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/ZiESqWwCXBRQoaPONSJe.png",
                "name": "曲丽丽",
                "id": "member1"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/tBOxZPlITHqwlGjsJWaF.png",
                "name": "王昭君",
                "id": "member2"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/sBxjgqiuHMGRkIjqlQCd.png",
                "name": "董娜娜",
                "id": "member3"
            }]
        }, {
            "id": "fake-list-5",
            "owner": "朱偏右",
            "title": "青云KubeSphere培训--part2",
            "avatar": "https://gw.alipayobjects.com/zos/rmsportal/zOsKZmFRdUtvpqCImOVY.png",
            "cover": "https://gw.alipayobjects.com/zos/rmsportal/iXjVmWVHbCJAyqvDxdtx.png",
            "status": "normal",
            "percent": 83,
            "logo": "https://gw.alipayobjects.com/zos/rmsportal/zOsKZmFRdUtvpqCImOVY.png",
            "href": "/",
            "updatedAt": 1569010638349,
            "createdAt": 1569010638349,
            "type": "CI / CD",
            "count": 333,
            "description": "在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。",
            "activeUser": 137947,
            "newUser": 1273,
            "star": 157,
            "like": 156,
            "message": 16,
            "content": "Continuous Integration，为持续集成。即在代码构建过程中持续地进行代码的集成、构建、以及自动化测试等；有了 CI 工具，我们可以在代码提交的过程中通过单元测试等尽早地发现引入的错误。",
            "members": [{
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/ZiESqWwCXBRQoaPONSJe.png",
                "name": "曲丽丽",
                "id": "member1"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/tBOxZPlITHqwlGjsJWaF.png",
                "name": "王昭君",
                "id": "member2"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/sBxjgqiuHMGRkIjqlQCd.png",
                "name": "董娜娜",
                "id": "member3"
            }]
        }, {
            "id": "fake-list-6",
            "owner": "鱼酱",
            "title": "青云sdn培训--part2",
            "avatar": "https://gw.alipayobjects.com/zos/rmsportal/kZzEzemZyKLKFsojXItE.png",
            "cover": "https://gw.alipayobjects.com/zos/rmsportal/iZBVOIhGJiAnhplqjvZW.png",
            "status": "active",
            "percent": 56,
            "logo": "https://gw.alipayobjects.com/zos/rmsportal/kZzEzemZyKLKFsojXItE.png",
            "href": "/",
            "updatedAt": 1569003438349,
            "createdAt": 1569003438349,
            "type": "k8s",
            "count": 391,
            "description": "在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。",
            "activeUser": 155125,
            "newUser": 1426,
            "star": 192,
            "like": 154,
            "message": 18,
            "content": "Kubernetes（简称K8S） 是Google开源的分布式的容器管理平台，方便我们在服务器集群中管理我们容器化应用。",
            "members": [{
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/ZiESqWwCXBRQoaPONSJe.png",
                "name": "曲丽丽",
                "id": "member1"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/tBOxZPlITHqwlGjsJWaF.png",
                "name": "王昭君",
                "id": "member2"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/sBxjgqiuHMGRkIjqlQCd.png",
                "name": "董娜娜",
                "id": "member3"
            }]
        }, {
            "id": "fake-list-7",
            "owner": "乐哥",
            "title": "青云桌面云培训--part2",
            "avatar": "https://gw.alipayobjects.com/zos/rmsportal/siCrBXXhmvTQGWPNLBow.png",
            "cover": "https://gw.alipayobjects.com/zos/rmsportal/uMfMFlvUuceEyPpotzlq.png",
            "status": "exception",
            "percent": 86,
            "logo": "https://gw.alipayobjects.com/zos/rmsportal/siCrBXXhmvTQGWPNLBow.png",
            "href": "/",
            "updatedAt": 1568996238349,
            "createdAt": 1568996238349,
            "type": "DevOps",
            "count": 449,
            "description": "在中台产品的研发过程中，会出现不同的设计规范和实现方式，但其中往往存在很多类似的页面和组件，这些类似的组件会被抽离成一套标准规范。",
            "activeUser": 188813,
            "newUser": 1708,
            "star": 177,
            "like": 145,
            "message": 20,
            "content": "根据devopsdotcom做的\"2017年DevOps使用情况和趋势\"的报告，DevOps的使用在过去几年一直持续增长，尤其是2016年以来。唯一的问题是小团队发现开始启用devops颇有难度。",
            "members": [{
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/ZiESqWwCXBRQoaPONSJe.png",
                "name": "曲丽丽",
                "id": "member1"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/tBOxZPlITHqwlGjsJWaF.png",
                "name": "王昭君",
                "id": "member2"
            }, {
                "avatar": "https://gw.alipayobjects.com/zos/rmsportal/sBxjgqiuHMGRkIjqlQCd.png",
                "name": "董娜娜",
                "id": "member3"
            }]
        }]
        return res


class GetChart(Resource):
    def get(self):
        res = {
            "visitData": [{
                "x": "2019-09-21",
                "y": 7
            }, {
                "x": "2019-09-22",
                "y": 5
            }, {
                "x": "2019-09-23",
                "y": 4
            }, {
                "x": "2019-09-24",
                "y": 2
            }, {
                "x": "2019-09-25",
                "y": 4
            }, {
                "x": "2019-09-26",
                "y": 7
            }, {
                "x": "2019-09-27",
                "y": 5
            }, {
                "x": "2019-09-28",
                "y": 6
            }, {
                "x": "2019-09-29",
                "y": 5
            }, {
                "x": "2019-09-30",
                "y": 9
            }, {
                "x": "2019-10-01",
                "y": 6
            }, {
                "x": "2019-10-02",
                "y": 3
            }, {
                "x": "2019-10-03",
                "y": 1
            }, {
                "x": "2019-10-04",
                "y": 5
            }, {
                "x": "2019-10-05",
                "y": 3
            }, {
                "x": "2019-10-06",
                "y": 6
            }, {
                "x": "2019-10-07",
                "y": 5
            }],
            "visitData2": [{
                "x": "2019-09-21",
                "y": 1
            }, {
                "x": "2019-09-22",
                "y": 6
            }, {
                "x": "2019-09-23",
                "y": 4
            }, {
                "x": "2019-09-24",
                "y": 8
            }, {
                "x": "2019-09-25",
                "y": 3
            }, {
                "x": "2019-09-26",
                "y": 7
            }, {
                "x": "2019-09-27",
                "y": 2
            }],
            "salesData": [{
                "x": "1月",
                "y": 1127
            }, {
                "x": "2月",
                "y": 547
            }, {
                "x": "3月",
                "y": 1005
            }, {
                "x": "4月",
                "y": 685
            }, {
                "x": "5月",
                "y": 1038
            }, {
                "x": "6月",
                "y": 407
            }, {
                "x": "7月",
                "y": 413
            }, {
                "x": "8月",
                "y": 698
            }, {
                "x": "9月",
                "y": 1197
            }, {
                "x": "10月",
                "y": 492
            }, {
                "x": "11月",
                "y": 595
            }, {
                "x": "12月",
                "y": 940
            }],
            "searchData": [{
                "index": 1,
                "keyword": "搜索关键词-0",
                "count": 9,
                "range": 54,
                "status": 0
            }, {
                "index": 2,
                "keyword": "搜索关键词-1",
                "count": 896,
                "range": 44,
                "status": 0
            }, {
                "index": 3,
                "keyword": "搜索关键词-2",
                "count": 967,
                "range": 75,
                "status": 1
            }, {
                "index": 4,
                "keyword": "搜索关键词-3",
                "count": 149,
                "range": 11,
                "status": 1
            }, {
                "index": 5,
                "keyword": "搜索关键词-4",
                "count": 582,
                "range": 81,
                "status": 1
            }, {
                "index": 6,
                "keyword": "搜索关键词-5",
                "count": 946,
                "range": 56,
                "status": 1
            }, {
                "index": 7,
                "keyword": "搜索关键词-6",
                "count": 880,
                "range": 96,
                "status": 1
            }, {
                "index": 8,
                "keyword": "搜索关键词-7",
                "count": 115,
                "range": 82,
                "status": 1
            }, {
                "index": 9,
                "keyword": "搜索关键词-8",
                "count": 361,
                "range": 85,
                "status": 1
            }, {
                "index": 10,
                "keyword": "搜索关键词-9",
                "count": 375,
                "range": 52,
                "status": 1
            }, {
                "index": 11,
                "keyword": "搜索关键词-10",
                "count": 487,
                "range": 22,
                "status": 1
            }, {
                "index": 12,
                "keyword": "搜索关键词-11",
                "count": 691,
                "range": 79,
                "status": 0
            }, {
                "index": 13,
                "keyword": "搜索关键词-12",
                "count": 969,
                "range": 67,
                "status": 0
            }, {
                "index": 14,
                "keyword": "搜索关键词-13",
                "count": 144,
                "range": 36,
                "status": 1
            }, {
                "index": 15,
                "keyword": "搜索关键词-14",
                "count": 391,
                "range": 70,
                "status": 0
            }, {
                "index": 16,
                "keyword": "搜索关键词-15",
                "count": 117,
                "range": 74,
                "status": 1
            }, {
                "index": 17,
                "keyword": "搜索关键词-16",
                "count": 547,
                "range": 59,
                "status": 0
            }, {
                "index": 18,
                "keyword": "搜索关键词-17",
                "count": 358,
                "range": 74,
                "status": 1
            }, {
                "index": 19,
                "keyword": "搜索关键词-18",
                "count": 862,
                "range": 6,
                "status": 0
            }, {
                "index": 20,
                "keyword": "搜索关键词-19",
                "count": 983,
                "range": 71,
                "status": 1
            }, {
                "index": 21,
                "keyword": "搜索关键词-20",
                "count": 178,
                "range": 41,
                "status": 1
            }, {
                "index": 22,
                "keyword": "搜索关键词-21",
                "count": 977,
                "range": 7,
                "status": 0
            }, {
                "index": 23,
                "keyword": "搜索关键词-22",
                "count": 602,
                "range": 38,
                "status": 1
            }, {
                "index": 24,
                "keyword": "搜索关键词-23",
                "count": 259,
                "range": 10,
                "status": 0
            }, {
                "index": 25,
                "keyword": "搜索关键词-24",
                "count": 538,
                "range": 58,
                "status": 1
            }, {
                "index": 26,
                "keyword": "搜索关键词-25",
                "count": 576,
                "range": 64,
                "status": 0
            }, {
                "index": 27,
                "keyword": "搜索关键词-26",
                "count": 229,
                "range": 19,
                "status": 0
            }, {
                "index": 28,
                "keyword": "搜索关键词-27",
                "count": 607,
                "range": 35,
                "status": 0
            }, {
                "index": 29,
                "keyword": "搜索关键词-28",
                "count": 171,
                "range": 97,
                "status": 1
            }, {
                "index": 30,
                "keyword": "搜索关键词-29",
                "count": 806,
                "range": 59,
                "status": 1
            }, {
                "index": 31,
                "keyword": "搜索关键词-30",
                "count": 240,
                "range": 51,
                "status": 0
            }, {
                "index": 32,
                "keyword": "搜索关键词-31",
                "count": 270,
                "range": 24,
                "status": 0
            }, {
                "index": 33,
                "keyword": "搜索关键词-32",
                "count": 495,
                "range": 46,
                "status": 1
            }, {
                "index": 34,
                "keyword": "搜索关键词-33",
                "count": 141,
                "range": 16,
                "status": 0
            }, {
                "index": 35,
                "keyword": "搜索关键词-34",
                "count": 320,
                "range": 59,
                "status": 1
            }, {
                "index": 36,
                "keyword": "搜索关键词-35",
                "count": 973,
                "range": 91,
                "status": 0
            }, {
                "index": 37,
                "keyword": "搜索关键词-36",
                "count": 308,
                "range": 76,
                "status": 0
            }, {
                "index": 38,
                "keyword": "搜索关键词-37",
                "count": 732,
                "range": 66,
                "status": 1
            }, {
                "index": 39,
                "keyword": "搜索关键词-38",
                "count": 462,
                "range": 87,
                "status": 0
            }, {
                "index": 40,
                "keyword": "搜索关键词-39",
                "count": 442,
                "range": 13,
                "status": 1
            }, {
                "index": 41,
                "keyword": "搜索关键词-40",
                "count": 34,
                "range": 3,
                "status": 1
            }, {
                "index": 42,
                "keyword": "搜索关键词-41",
                "count": 93,
                "range": 87,
                "status": 1
            }, {
                "index": 43,
                "keyword": "搜索关键词-42",
                "count": 885,
                "range": 77,
                "status": 1
            }, {
                "index": 44,
                "keyword": "搜索关键词-43",
                "count": 785,
                "range": 68,
                "status": 1
            }, {
                "index": 45,
                "keyword": "搜索关键词-44",
                "count": 708,
                "range": 14,
                "status": 0
            }, {
                "index": 46,
                "keyword": "搜索关键词-45",
                "count": 685,
                "range": 5,
                "status": 1
            }, {
                "index": 47,
                "keyword": "搜索关键词-46",
                "count": 28,
                "range": 86,
                "status": 0
            }, {
                "index": 48,
                "keyword": "搜索关键词-47",
                "count": 809,
                "range": 31,
                "status": 0
            }, {
                "index": 49,
                "keyword": "搜索关键词-48",
                "count": 925,
                "range": 93,
                "status": 1
            }, {
                "index": 50,
                "keyword": "搜索关键词-49",
                "count": 482,
                "range": 92,
                "status": 0
            }],
            "offlineData": [{
                "name": "Stores 0",
                "cvr": 0.2
            }, {
                "name": "Stores 1",
                "cvr": 0.6
            }, {
                "name": "Stores 2",
                "cvr": 0.7
            }, {
                "name": "Stores 3",
                "cvr": 0.8
            }, {
                "name": "Stores 4",
                "cvr": 0.9
            }, {
                "name": "Stores 5",
                "cvr": 0.1
            }, {
                "name": "Stores 6",
                "cvr": 0.5
            }, {
                "name": "Stores 7",
                "cvr": 0.7
            }, {
                "name": "Stores 8",
                "cvr": 0.7
            }, {
                "name": "Stores 9",
                "cvr": 0.3
            }],
            "offlineChartData": [{
                "x": 1569037709676,
                "y1": 83,
                "y2": 30
            }, {
                "x": 1569039509676,
                "y1": 108,
                "y2": 49
            }, {
                "x": 1569041309676,
                "y1": 104,
                "y2": 40
            }, {
                "x": 1569043109676,
                "y1": 38,
                "y2": 48
            }, {
                "x": 1569044909676,
                "y1": 12,
                "y2": 43
            }, {
                "x": 1569046709676,
                "y1": 21,
                "y2": 72
            }, {
                "x": 1569048509676,
                "y1": 93,
                "y2": 104
            }, {
                "x": 1569050309676,
                "y1": 62,
                "y2": 87
            }, {
                "x": 1569052109676,
                "y1": 91,
                "y2": 43
            }, {
                "x": 1569053909676,
                "y1": 66,
                "y2": 59
            }, {
                "x": 1569055709676,
                "y1": 10,
                "y2": 45
            }, {
                "x": 1569057509676,
                "y1": 53,
                "y2": 86
            }, {
                "x": 1569059309676,
                "y1": 52,
                "y2": 17
            }, {
                "x": 1569061109676,
                "y1": 13,
                "y2": 92
            }, {
                "x": 1569062909676,
                "y1": 25,
                "y2": 35
            }, {
                "x": 1569064709676,
                "y1": 30,
                "y2": 37
            }, {
                "x": 1569066509676,
                "y1": 59,
                "y2": 53
            }, {
                "x": 1569068309676,
                "y1": 14,
                "y2": 15
            }, {
                "x": 1569070109676,
                "y1": 56,
                "y2": 72
            }, {
                "x": 1569071909676,
                "y1": 48,
                "y2": 15
            }],
            "salesTypeData": [{
                "x": "CI / CD",
                "y": 4544
            }, {
                "x": "k8s",
                "y": 3321
            }, {
                "x": "DevOps",
                "y": 3113
            }, {
                "x": "GitOps",
                "y": 2341
            }, {
                "x": "Istio",
                "y": 1231
            }, {
                "x": "Promethues",
                "y": 1231
            }],
            "salesTypeDataOnline": [{
                "x": "CI / CD",
                "y": 244
            }, {
                "x": "k8s",
                "y": 321
            }, {
                "x": "DevOps",
                "y": 311
            }, {
                "x": "GitOps",
                "y": 41
            }, {
                "x": "Istio",
                "y": 121
            }, {
                "x": "Promethues",
                "y": 111
            }],
            "salesTypeDataOffline": [{
                "x": "CI / CD",
                "y": 99
            }, {
                "x": "k8s",
                "y": 188
            }, {
                "x": "DevOps",
                "y": 344
            }, {
                "x": "GitOps",
                "y": 255
            }, {
                "x": "Promethues",
                "y": 65
            }],
            "radarData": [{
                "name": "个人",
                "label": "引用",
                "value": 10
            }, {
                "name": "个人",
                "label": "口碑",
                "value": 8
            }, {
                "name": "个人",
                "label": "产量",
                "value": 4
            }, {
                "name": "个人",
                "label": "贡献",
                "value": 5
            }, {
                "name": "个人",
                "label": "热度",
                "value": 7
            }, {
                "name": "团队",
                "label": "引用",
                "value": 3
            }, {
                "name": "团队",
                "label": "口碑",
                "value": 9
            }, {
                "name": "团队",
                "label": "产量",
                "value": 6
            }, {
                "name": "团队",
                "label": "贡献",
                "value": 3
            }, {
                "name": "团队",
                "label": "热度",
                "value": 1
            }, {
                "name": "部门",
                "label": "引用",
                "value": 4
            }, {
                "name": "部门",
                "label": "口碑",
                "value": 1
            }, {
                "name": "部门",
                "label": "产量",
                "value": 6
            }, {
                "name": "部门",
                "label": "贡献",
                "value": 5
            }, {
                "name": "部门",
                "label": "热度",
                "value": 7
            }]
        }
        return res


api.add_resource(ResList, '/api/res')
api.add_resource(Res, '/api/res/<res_id>')

api.add_resource(ComList, '/api/coms')
api.add_resource(Com, '/api/com/<com_id>')

api.add_resource(QingLogin, '/api/login/account')
api.add_resource(CurrentUser, '/api/currentUser')
api.add_resource(GetList, '/api/fake_list')
api.add_resource(GetChart, '/api/fake_chart_data')


@app.route('/')
def index():
    context = {
        'questions': QuestionModel.query.all()
    }
    return flask.render_template('index.html',**context)


@app.route('/question/', methods=['GET', 'POST'])
def question():
    if flask.request.method == 'GET':
        return flask.render_template('question.html')
    else:
        title = flask.request.form.get('title')
        content = flask.request.form.get('content')
        question_model = QuestionModel(title=title, content=content)
        question_model.author = UserModel.query.filter_by(username='admin').first()
        db.session.add(question_model)
        db.session.commit()
        return flask.redirect(flask.url_for('index'))


@app.route('/d/<id>/')
def detail(id):
    question_model = QuestionModel.query.get(id)
    return flask.render_template('detail.html',question=question_model)


@app.route('/comment/', methods=['POST'])
def comment():
    question_id = flask.request.form.get('question_id')
    content = flask.request.form.get('content')
    answer_model = AnswerModel(content=content)
    answer_model.author = UserModel.query.filter_by(username='zhangchi').first()
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