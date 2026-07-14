import pymysql

try:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root123",
        database="cryptopulse"
    )

    print("Connected Successfully!")

    conn.close()

except Exception as e:
    print("ERROR:", e)