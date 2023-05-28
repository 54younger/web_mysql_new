# index_test.py
import time
import pymysql
import matplotlib.pyplot as plt
from poprogress import simple_progress

# 连接数据库
db = pymysql.connect(host='127.0.0.1',
                     user='root',
                     password='20021110wcy',
                     db='test_temp',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

# 创建游标对象
cursor = db.cursor()

search_times_with_index = [] # 记录查询时间（有索引）
search_times_without_index = [] # 记录查询时间（无索引）
insert_times = [] # 记录插入时间


def data_insert(times):
    # 插入数据
    for i in simple_progress(range(times,10*times)):
        topic_id = (i+1)%3+1
        user_id = (i+1)%3+1
        title = f"Title {i+1}"
        content = f"Content {i+1}"
        sql = f"INSERT INTO post (title, content, topic_id, user_id) VALUES ('{title}', '{content}',{topic_id}, {user_id})"
        cursor.execute(sql)
    db.commit()


def data_query_time(user_id):
    start_time = time.time()
    sql = f"SELECT * FROM post WHERE user_id = {user_id}"
    cursor.execute(sql)
    search_time = time.time() - start_time
    return search_time

# 将操作详情、结果和耗时写入文件
def write_to_file(operation, details, elapsed_time):
    with open("index_time.txt", "a") as file:
        file.write(f"Operation: {operation}\n")
        file.write(f"Details: {details}\n")
        file.write(f"Elapsed time: {elapsed_time:.6f} seconds\n")
        file.write("------------------------------\n")


# 删除外键约束
cursor.execute("ALTER TABLE post DROP FOREIGN KEY post_ibfk_1")

#记录不同数量级的数据的时间
for i in simple_progress(range(7)):
    times=10**i
    user_id = (i % 3) + 1

    insert_start_time = time.time()
    data_insert(times)
    insert_times.append(time.time() - insert_start_time)

    cursor.execute("ALTER TABLE post ADD INDEX (user_id)")
    # 测试查询时间（有索引）
    search_times_with_index.append(data_query_time(user_id))

    cursor.execute("ALTER TABLE post DROP INDEX user_id")
    # 测试查询时间（无索引）
    search_times_without_index.append(data_query_time(user_id))

    # 将操作详情、结果和耗时写入文件
    write_to_file("Insert", f"Insert {times} rows of data", insert_times[i])
    write_to_file("Query with index", f"Query data with user_id = {user_id}", search_times_with_index[i])
    write_to_file("Query without index", f"Query data with user_id = {user_id}", search_times_without_index[i])



# 绘制折线图
plt.plot(search_times_with_index, label="Query with index")
plt.plot(search_times_without_index, label="Query without index")
plt.xlabel("Number of data")
plt.ylabel("Time (seconds)")
plt.legend()
plt.show()
# 将折线图保存为图片
plt.savefig("index_time.png")

# 关闭数据库连接
db.close()
