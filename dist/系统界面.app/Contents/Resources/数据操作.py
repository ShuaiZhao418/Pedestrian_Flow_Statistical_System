import pymysql

# ----------------------------------------------------插入数据-----------------------------------------------------------
def datainsert(date, time, place, peoplecount):
    db = pymysql.connect(host='localhost', user='root', password='594300', port=3306, db='peopledetect', charset='utf8')
    # 创建一个游标对象cursor()
    cursor = db.cursor ()
    # 设置增加数据的sql语句
    # 需要注意的是，values中每一个都需要加引号，引号中符号表示其类型，并且%号应该在'''号之外，而并不是在它的里面。
    # 插入数据
    sql = '''
    	INSERT INTO people(date,time,place,peoplecount)
    	VALUES('%s','%s','%s','%d')
    	''' %(date,time,place,int(peoplecount))
    # 执行sql语句，记清楚是cursor
    cursor.execute(sql)
    # 因为是增加，需要提交一下，记清楚是db
    db.commit()
    db.close()


# ----------------------------------------------------删除数据-----------------------------------------------------------
def datadelete(date):
    db = pymysql.connect(host='localhost', user='root', password='594300', port=3306, db='peopledetect', charset='utf8')
    # 创建一个游标对象cursor()
    cursor = db.cursor()
    # 删除数据
    sql='''DELETE FROM people
	    WHERE date='%s'
	    '''%date
    # 执行sql语句，记清楚是cursor
    cursor.execute(sql)
    # 因为是增加，需要提交一下，记清楚是db
    db.commit()
    db.close()


# ----------------------------------------------------修改数据-----------------------------------------------------------
def dataupdate(date, time, place, peoplecount):
    db = pymysql.connect(host='localhost', user='root', password='594300', port=3306, db='peopledetect', charset='utf8')
    # 创建一个游标对象cursor()
    cursor = db.cursor()
    # 更新数据
    sql = '''UPDATE people SET time='%s',place='%s',peoplecount='%d'
        	    WHERE date='%s'
          ''' %(time, place, int(peoplecount), date)
    cursor.execute(sql)  # 执行语句
    db.commit()  # 提交
    db.close()  # 关闭连接


# ----------------------------------------------------查询数据-----------------------------------------------------------
def dataquery():
    db = pymysql.connect(host='localhost', user='root', password='594300', port=3306, db='peopledetect', charset='utf8')
    # 创建一个游标对象cursor()
    cursor = db.cursor()
    # 查询数据
    sql = 'SELECT * FROM people'
    # 注意此处的等于后面的内容根据其数据类型而判断是否加引号
    # 执行sql语句
    cursor.execute(sql)
    data = cursor.fetchall()  # 这个函数可以获取所有满足要求的内容，是元组类型
    db.close()
    return data