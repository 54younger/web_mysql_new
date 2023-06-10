from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)
sql_user = ''
sql_password = ''

@app.route('/login', methods=['GET', 'POST'])
def login():
    global sql_user
    global sql_password
    if request.method == 'POST':
        sql_user = request.form['user']
        sql_password = request.form['password']
    return render_template('index.html')

# Database configuration
db = pymysql.connect(host='127.0.0.1',
                     user=sql_user,
                     password=sql_password,
                     db='test_temp',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

# Index page


@app.route('/')
def index():
    if sql_user == '' and sql_password == '':
        return redirect(url_for('login'))
    else:
        return render_template('index.html')

# User page


@app.route('/user')
def user():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user')
    users = cursor.fetchall()
    return render_template('user.html', users=users)


# Post page
@app.route('/post')
def post():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM post')
    posts = cursor.fetchall()
    return render_template('post.html', posts=posts)

# Comment page


@app.route('/comment')
def comment():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM comment')
    comments = cursor.fetchall()
    return render_template('comment.html', comments=comments)


# Topic page
@app.route('/topic')
def topic():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM topic')
    topics = cursor.fetchall()
    return render_template('topic.html', topics=topics)


# View post page查询某个ID的帖子和其下的所有评论
@app.route('/view_post', methods=['GET', 'POST'])
def view_post():
    if request.method == 'POST':
        cursor = db.cursor()
        post_id = request.form['post_id']
        cursor.execute('SELECT * FROM post WHERE post_id = %s', post_id)
        post = cursor.fetchone()
        cursor.execute('SELECT * FROM comment WHERE post_id = %s', post_id)
        comments = cursor.fetchall()
        return render_template('view_post.html', post=post, comments=comments)

# Add users
def insert_user(username, email, password):
    cursor = db.cursor()
    sql = "INSERT INTO user (username, email, password) VALUES (%s, %s, %s)"
    cursor.execute(sql, (username, email, password))
    db.commit()


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        insert_user(user_id, username, email, password)
        return user()


# Delete post
@app.route('/del_post', methods=['POST'])
def del_post():
    post_id = request.form['post_id']
    cursor = db.cursor()
    cursor.execute('DELETE FROM post WHERE post_id = %s', post_id)
    db.commit()
    return post()


# rename username
@app.route('/rename_username', methods=['POST'])
def recheck_username():
    user_id = request.form['user_id']
    newname = request.form['newname']
    cursor = db.cursor()
    cursor.execute('UPDATE user set username = %s where user_id = %s', [
                   newname, user_id])
    db.commit()
    return user()


app.run()

# 新添加功能

# 0.在需要自动生成ID的列（例如 user_id、topic_id、post_id 和 comment_id）上使用了 AUTO_INCREMENT 属性。这将使数据库自动为这些列生成唯一的自增整数值，从1开始逐步递增。

# 1.给post新添加外键topic_id

# 2.GetPostsByTopic 并且可以在topic中通过点击查看该topic下的所有post


@app.route('/GetPostsByTopic/<int:topic_id>', methods=['GET'])
def GetPostsByTopic(topic_id):
    cursor = db.cursor()
    cursor.callproc('GetPostsByTopic', (topic_id,))
    db.commit()
    posts = cursor.fetchall()
    return render_template('post.html', posts=posts)

# 3.DeletePost2
@app.route('/delete_post/<int:post_id>', methods=['GET'])
def delete_post(post_id):
    cursor = db.cursor()
    cursor.callproc('DeletePost', (post_id,))
    db.commit()
    return post()

# 4.CreatePost
@app.route('/CreatePost', methods=['POST'])
def CreatePost():
    cursor = db.cursor()
    title = request.form['title']
    content = request.form['content']
    topic_id = request.form['topic_id']
    user_id = request.form['user_id']
    cursor.callproc('CreatePost', (title, content, topic_id, user_id))
    db.commit()
    return post()

# 5.UpdatePost
@app.route('/UpdatePost', methods=['POST'])
def UpdatePost():
    cursor = db.cursor()
    post_id = request.form['post_id']
    content = request.form['content']
    cursor.callproc('UpdatePost', (post_id, content))
    db.commit()
    return post()


if __name__ == '__main__':
    app.run()
