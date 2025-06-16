import pymysql

sql_info = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'db': 'myDatabase',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 数据库连接配置


def get_db_connection():
    connection = pymysql.connect(
        # host='mysql',
        host=sql_info['host'],
        user=sql_info['user'],
        password=sql_info['password'],
        db=sql_info['db'],
        charset=sql_info['charset'],
        cursorclass=sql_info['cursorclass']
    )
    return connection
