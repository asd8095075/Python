from flask import Blueprint, render_template, request, redirect, url_for, session


from App.models import *


blue = Blueprint('blue', __name__)

# 首页
@blue.route('/')
def index():
    article = Article.query.all()
    classifi = Classification.query.all()
    for i in classifi:
        art = Article.query.filter_by(classification=i.id).count()
        i.num = art
    return render_template('web/index.html',article=article,classifi=classifi)

@blue.route('/classification/<cid>/')
def classification(cid):
    classifi = Classification.query.all()
    for i in classifi:
        art = Article.query.filter_by(classification=i.id).count()
        i.num = art
    article = Article.query.filter_by(classification=cid)
    return render_template('web/index.html',article=article,classifi=classifi)

@blue.route('/articledetails/<name>')
def article_details(name):
    article = Article.query.filter_by(name = name)
    classifi = Classification.query.all()
    for i in classifi:
        art = Article.query.filter_by(classification=i.id).count()
        i.num = art
    return render_template('web/info.html',article=article,classifi=classifi)


#关于我
@blue.route('/about/')
def about():
    classifi = Classification.query.all()
    for i in classifi:
        art = Article.query.filter_by(classification=i.id).count()
        print(art)
        i.num = art
    return render_template('web/about.html',classifi=classifi)

# 后台
#登录
@blue.route('/login/', methods=['get', 'post'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = User.query.filter_by(username=username, passwd=password)
        if users.count() > 0:
            # 登录成功
            response = redirect(url_for('blue.admin'))
            session['userid'] = users.first().id
            return response
        else:
            return render_template('admin/login.html')
    return render_template('admin/login.html')

#注册
#用户管理界面
@blue.route('/manageuser/', methods=['get', 'post'])
def manage_user():
    userid = session.get('userid', '')
    if userid:
        username = User.query.get(userid).name
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            name = request.form.get('truename')
            phone = request.form.get('usertel')
            new_password = request.form.get('new_password')
            if password!=new_password:
                msg = "两次密码不一致"
                return msg
            else:
                user = User()
                user.username = username
                user.passwd = new_password
                user.name = name
                user.phone = phone
                try:
                    db.session.add(user)
                    db.session.commit()
                except:
                    db.session.rollback()
                    db.session.flush()
                else:
                    return render_template('admin/manage-user.html',name=username)
        return render_template('admin/manage-user.html',name=username)
    return render_template('admin/login.html')

@blue.route('/register/', methods=['post', 'get'])
def register():
    if request.method == 'POST':
        # 实现注册功能
        username = request.form.get('username')
        password = request.form.get('password')

        # 可以在注册前做一些用户名和密码的检测
        if len(username) < 6:
            return render_template('admin/register.html', msg="用户名长度至少为6位")

        # 实现注册：向User表中插入一条数据
        user = User()
        user.username = username
        user.passwd = password
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
            msg = "注册失败"
        else:
            msg = "注册成功"
        return render_template('admin/register.html', msg=msg)

    return render_template('admin/register.html')

#主界面
@blue.route('/admin/')
def admin():
    userid = session.get('userid', '')
    if userid:
        username = User.query.get(userid).name
        return render_template('admin/index.html',name=username)
    return render_template('admin/login.html')

#文章管理界面
@blue.route('/article/')
def article():
    userid = session.get('userid', '')
    if userid:
        username = User.query.get(userid).name
        articles = Article.query.all()
        return render_template('admin/article.html',article=articles,name=username)
    return render_template('admin/login.html')

#后台增加文章
@blue.route('/addarticle/', methods=['post', 'get'])
def add_article():
    userid = session.get('userid', '')
    if userid:
        username = User.query.get(userid).name
        if request.method == 'POST':
            name = request.form.get('title')
            content = request.form.get("describe")
            classification = request.form.get("category")
            imgsrc = request.form.get("titlepic")
            label = request.form.get("tags")
            keyword = request.form.get('keywords')
            data = request.form.get('time')
            arts = Article()
            arts.name = name
            arts.content = content
            arts.classification = classification
            arts.imgsrc = imgsrc
            arts.label = label
            arts.keyword = keyword
            arts.data = data
            try:
                db.session.add(arts)
                db.session.commit()
            except:
                db.session.rollback()
                db.session.flush()
            else:
                articles = Article.query.all()
                return render_template('admin/article.html',article=articles,name=username)
        else:
            classifi = Classification.query.all()
            return render_template('admin/add-article.html',classifi=classifi,name=username)
    return render_template('admin/login.html')

#删除文章
@blue.route('/deletearticle/<title>/')
def delete_article(title):
    a = Article.query.filter_by(name=title).first()
    db.session.delete(a)
    db.session.commit()
    return redirect(url_for('blue.article'))

#修改文章
@blue.route('/updatearticle/<title1>/')
def update_article(title1):
    userid = session.get('userid', '')
    if userid:
        username = User.query.get(userid).name
        b = Article.query.filter_by(name=title1).first()
        classifi = Classification.query.all()
        return render_template('admin/update-article.html', classifi=classifi, b=b,name=username)
    return render_template('admin/login.html')

@blue.route('/updatearticle2/<title2>/', methods=['post', 'get'])
def update_article2(title2):
    if request.method == 'POST':
        name = request.form.get('title')
        content = request.form.get("describe")
        classification = request.form.get("category")
        imgsrc = request.form.get("titlepic")
        label = request.form.get("tags")
        keyword = request.form.get('keywords')
        data = request.form.get('time')
        b = Article.query.filter_by(name=title2).first()
        b.name = name
        b.content = content
        b.classification = classification
        b.imgsrc = imgsrc
        b.label = label
        b.keyword = keyword
        b.data = data
        db.session.commit()
        return redirect(url_for('blue.article'))
    else:
        return redirect(url_for('blue.article'))

#查询
@blue.route('/search/', methods=['post', 'get'])
def search():
    if request.method == 'POST':
        sear = request.form.get('search')
        articles = Article.query.filter_by(keyword=sear)
        return render_template('admin/article.html',article=articles)
    else:
        return redirect(url_for('blue.article'))

#栏目的增删改查
#增加栏目
@blue.route('/category/')
def column():
    userid = session.get('userid', '')
    if userid:
        username = User.query.get(userid).name
        classifi = Classification.query.all()
        for i in classifi:
            art = Article.query.filter_by(classification=i.id).count()
            print(art)
            i.num = art
        return render_template('admin/category.html',classifi=classifi,name=username)
    return render_template('admin/login.html')

@blue.route('/addcategory/', methods=['post', 'get'])
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        alias = request.form.get('alias')
        content = request.form.get('describe')
        keyword = request.form.get('keywords')
        parentnode = request.form.get('fid')
        c = Classification()
        c.name = name
        c.alias = alias
        c.content = content
        c.keyword = keyword
        c.parentnode = parentnode
        try:
            db.session.add(c)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        else:

            return redirect(url_for('blue.column'))
    else:
        return redirect(url_for('blue.column'))

#删除栏目
@blue.route('/deletecategory/<name>/')
def delete_category(name):
    p=Classification.query.filter_by(name=name).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('blue.column'))

#修改栏目
@blue.route('/updatecategory/<name>/')
def update_category(name):
    userid = session.get('userid', '')
    if userid:
        username = User.query.get(userid).name
        p = Classification.query.filter_by(name=name).first()
        classifi = Classification.query.all()
        return render_template('admin/update-category.html',p=p,classifi=classifi,name=username)
    return render_template('admin/login.html')

@blue.route('/updatecategory2/<title>/', methods=['post', 'get'])
def update_category2(title):
    if request.method == 'POST':
        name = request.form.get('name')
        alias = request.form.get('alias')
        content = request.form.get('describe')
        keyword = request.form.get('keywords')
        parentnode = request.form.get('fid')
        p = Classification.query.filter_by(name=title).first()
        p.name = name
        p.alias = alias
        p.content = content
        p.keyword = keyword
        p.parentnode = parentnode
        db.session.commit()
        return redirect(url_for('blue.column'))
    else:
        return redirect(url_for('blue.column'))

#查询栏目
@blue.route('/search2/', methods=['post', 'get'])
def search2():
    userid = session.get('userid', '')
    if userid:
        username = User.query.get(userid).name
        if request.method == 'POST':
            sear = request.form.get('search')
            classifi = Classification.query.filter_by(keyword = sear)
            return render_template('admin/category.html', classifi=classifi,name=username)
        else:
            return redirect(url_for('blue.column'))
    return render_template('admin/login.html')