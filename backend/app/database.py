import pymysql


# 数据库连接配置
def get_db_connection():
    connection = pymysql.connect(
        # host='mysql',
        host='127.0.0.1',
        user='root',
        password='root',
        db='myDatabase',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
