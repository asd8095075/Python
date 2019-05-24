from App.exts import db


# 模型 => 分类
class Classification(db.Model):
    __tablename__ = 'classification'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    alias = db.Column(db.String(20))
    keyword = db.Column(db.String(20))
    content = db.Column(db.String(1000))
    parentnode = db.Column(db.String(20))
    num = db.Column(db.Integer,default=0)
    articles = db.relationship('Article',backref='article', lazy='dynamic')




#文章类
class Article(db.Model):
    __tablename__ = 'article'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    content = db.Column(db.String(1000),default='无')
    imgsrc = db.Column(db.String(50),default='无')
    label = db.Column(db.String(50),default='无')
    comment = db.Column(db.Integer,default=0)
    data = db.Column(db.Date)
    keyword = db.Column(db.String(20))
    classification = db.Column(db.Integer, db.ForeignKey(Classification.id))


#用户
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    passwd = db.Column(db.String(20))
    username = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(30))