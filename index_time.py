from cProfile import run
import time
from flask import Flask, render_template, request, redirect, url_for
import pymysql
from poprogress import simple_progress

app = Flask(__name__)

# Database configuration
db = pymysql.connect(host='127.0.0.1',
                     user='root',
                     password='20021110wcy',
                     db='test_temp',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

total_elapsed_time = 0.0

# 数据查询
def data_query(user_id):
    global total_elapsed_time
    # 执行查询语句
    cursor = db.cursor()
    query = "SELECT * FROM post WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    '''
    # 记录操作详情和耗时
    elapsed_time = time.time() - start_time
    total_elapsed_time += elapsed_time

    operation = f"Data query: user_id={user_id}"
    details = f"Result: {result}"
    write_to_file(operation, details, elapsed_time)
    '''
    return result

# 数据插入
def data_insert(title, content, topic_id, user_id):

    global total_elapsed_time
    # 执行插入语句
    cursor = db.cursor()
    query = "INSERT INTO post (title, content, topic_id, user_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (title, content, topic_id, user_id))
    db.commit()

    '''
    # 记录操作详情和耗时
    elapsed_time = time.time() - start_time
    total_elapsed_time += elapsed_time

    operation = f"Data insert: title={title}, content={content}, topic_id={topic_id}, user_id={user_id}"
    details = "Insertion successful"

    write_to_file(operation, details, elapsed_time)
    '''
# 将操作详情、结果和耗时写入文件
def write_to_file(operation, details, elapsed_time):
    with open("index_time.txt", "a") as file:
        file.write(f"Operation: {operation}\n")
        file.write(f"Details: {details}\n")
        file.write(f"Elapsed time: {elapsed_time:.6f} seconds\n")
        file.write("------------------------------\n")


# 进行1000000次不同的数据插入
start_time=time.time()

for i in simple_progress(range(1000000)):
    title = f"Title {i+1}"
    content = f"Content {i+1}"
    topic_id = (i+1)%3+1
    user_id = (i+1)%3+1
    data_insert(title, content, topic_id, user_id)

total_elapsed_time=time.time()
insert_time=total_elapsed_time-start_time
operation = "insert time"
details = f"Total: {insert_time:.6f} seconds"
write_to_file(operation, details, insert_time)

start_time=time.time()
# 进行(无索引)数据查询
for i in range(1):
    user_id = (i+1)%3+1
    data_query(user_id)

total_elapsed_time=time.time()

search_time=total_elapsed_time-start_time
operation = "serach time(without index)"
details = f"Total: {search_time:.6f} seconds"
write_to_file(operation, details, search_time)


#针对user_id创建索引
cursor = db.cursor()
cursor.execute('ALTER TABLE post ADD INDEX (post_id)')
db.commit()

start_time=time.time()
# 进行(有索引)数据查询
for i in range(1):
    user_id = (i+1)%3+1
    data_query(user_id)

total_elapsed_time=time.time()

search_time_index=total_elapsed_time-start_time
operation = "serach time(with index)"
details = f"Total: {search_time_index:.6f} seconds"
write_to_file(operation, details, search_time_index)
