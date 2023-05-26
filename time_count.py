from cProfile import run
import time
from flask import Flask, render_template, request, redirect, url_for
import pymysql

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
    start_time = time.time()
    global total_elapsed_time
    # 执行查询语句
    cursor = db.cursor()
    query = "SELECT * FROM post WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()

    # 记录操作详情和耗时
    elapsed_time = time.time() - start_time
    total_elapsed_time += elapsed_time
    operation = f"Data query: user_id={user_id}"
    details = f"Result: {result}"
    write_to_file(operation, details, elapsed_time)

    return result

# 数据插入
def data_insert(title, content, topic_id, user_id):
    start_time = time.time()
    global total_elapsed_time
    # 执行插入语句
    cursor = db.cursor()
    query = "INSERT INTO post (title, content, topic_id, user_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (title, content, topic_id, user_id))
    db.commit()

    # 记录操作详情和耗时
    elapsed_time = time.time() - start_time
    total_elapsed_time += elapsed_time
    operation = f"Data insert: title={title}, content={content}, topic_id={topic_id}, user_id={user_id}"
    details = "Insertion successful"

    write_to_file(operation, details, elapsed_time)

# 将操作详情、结果和耗时写入文件
def write_to_file(operation, details, elapsed_time):
    with open("time.txt", "a") as file:
        file.write(f"Operation: {operation}\n")
        file.write(f"Details: {details}\n")
        file.write(f"Elapsed time: {elapsed_time:.6f} seconds\n")
        file.write("------------------------------\n")





# 进行10次不同的数据插入
for i in range(10):
    title = f"Title {i+1}"
    content = f"Content {i+1}"
    topic_id = i//4+1
    user_id = i//4+1
    data_insert(title, content, topic_id, user_id)

operation = "Total elapsed time"
details = f"Total: {total_elapsed_time:.6f} seconds"
write_to_file(operation, details, total_elapsed_time)
# 进行10次数据查询
for i in range(10):
    user_id = i//4+1
    data_query(user_id)
operation = "Total elapsed time"
details = f"Total: {total_elapsed_time:.6f} seconds"
write_to_file(operation, details, total_elapsed_time)
