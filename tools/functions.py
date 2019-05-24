from flask import session, render_template


def login_required(fn):
    def inner(*args, **kwargs):

        # 判断是否已登录
        userid = session.get('userid', '')
        if userid:  # 已登录
            return fn(*args, **kwargs)

        # 未登录,则进入登录页面
        return render_template('admin/login.html')

    return inner
