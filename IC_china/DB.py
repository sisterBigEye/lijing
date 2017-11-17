#-*-coding:utf-8 -*-
import MySQLdb

DATABASE_NAME = 'test1'

class HeroDB:
    # init class and create a database
    def __init__(self, dbname, conn, cur):
        self.dbname = dbname
        self.conn = conn
        self.cur = cur

        try:
            #数据库若不存在就创建
            cur.execute('create database if not exists ' + dbname)
            #切换到新建数据库中
            conn.select_db(dbname)
            conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    #字典参数形式的粘合函数，例：使{'a':'22sd','b':'sdf'}，成为一个字符串a='22sd',b='sdf'
    def bestr(do_dict):
        result=""
        if(isinstance(do_dict,dict)):
            for key in do_dict.keys():
                result=result+key+"="+"\'"+str(do_dict[key])+"\'"+','
            result=result[:-1]
            # print result
        return result
    # create a tablem
    #param=info
    #建表
    def createTable_k(self,name, value):
        param=""
        param1=""
        try:
            ex = self.cur.execute
            #判断value是不是dict类型，也就要插入的一个企业信息数据的字典，然后取出key作为表的字段名称，然后建表
            if(isinstance(value,dict)):
                print value
                for key in value.keys():
                    param=param+key+" VARCHAR(225)"+","
                param=param[:-1]
                print param
                param1=param.rstrip(',')

            sql="create table  %s (%s) " %(name,param1)
            print sql
            ex(sql)
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def createTable_v(self,name, value):
        param=""
        param1=""
        try:
            ex = self.cur.execute
            #判断value是不是dict类型，也就要插入的一个企业信息数据的字典，然后取出key作为表的字段名称，然后建表
            if(isinstance(value,dict)):
                print value
                for val in value.values():
                    param=param+val+" VARCHAR(225)"+","
                param=param[:-1]
                print param
                param1=param.rstrip(',')

            sql="create table  %s (%s) " %(name,param1)
            print sql
            ex(sql)
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    # insert more records
    def insertMore(self, tname, values):
        try:

            #传值语句转化
            #(%s,%s,%s..)=chs
            chs=('%s,'*len(values[0])).rstrip(',')
            sql='insert into ' + tname + ' values '+ '('+ chs +')'
            print sql
            self.cur.executemany(sql,values)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def update(self,name,setstr,values):
        try:
            #sql='update ' + name + ' set name=%s, sex=%s, age=%s, info=%s where id=%s;
            #setstr=' name=%s, sex=%s, age=%s, info=%s where id=%s;'
            #手动输入涌现两句，在程序中设置好，就要传参数
            # print "请输入更新的字段名称，格式为name=%s，sex=%s where id=%s;"
            # setstr=raw_input()
            sql='update ' + name + ' set '+ setstr
            self.cur.executemany(sql,values)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])



    # get record count from db table
    def getCount(self, name):
        try:
            count = self.cur.execute('select * from ' + name)
            return count
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    # select first record from database
    def selectFirst(self, name):
        try:
            self.cur.execute('select * from ' + name + ';')
            result = self.cur.fetchone()
            return result
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    # select last record from database
    def selectLast(self, name):
        try:
            self.cur.execute('SELECT * FROM ' + name + ' ORDER BY id DESC;')
            result = self.cur.fetchone()
            return result
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    # select next n records from database
    def selectNRecord(self, name, n):
        try:
            self.cur.execute('select * from ' + name + ';')
            results = self.cur.fetchmany(n)
            return results
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    # select all records
    def selectAll(self, name):
        try:
            self.cur.execute('select * from ' + name + ';')
            self.cur.scroll(0, mode='absolute') # reset cursor location (mode = absolute | relative)
            results = self.cur.fetchall()
            return results
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    # delete  record by condition，condition is a str
    def deleteByID(self, name, condition):
        try:

            self.cur.execute('delete from ' + name + ' where '+condition)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


    #选择几个字段的数据
    def select_p(self,name, param):
        try:
            Sparam=""
            if isinstance(param,list) or isinstance(param,tuple):
                for i in range(len(param)):
                    Sparam=Sparam+param[i]+','
            Sparam=Sparam[:-1]
            Sparam=Sparam.rstrip(',')
            sql='select distinct '+Sparam+ ' from '+name
            self.cur.execute(sql)
            results=self.cur.fetchall()
            #返回查到的所有数据
            print results
            return results
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#使用度高的SQL语句可以抽象出来，使用度自有的，下面重新定义，要求是每次程序里自己写sql语句
    #更新
    def S_update(self, sql, *param):
        try:
            self.cur.executemany(sql,*param)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    #选择
    def S_select(self, sql, *param):
        try:
            self.cur.execute(sql,*param)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

     #删除
    def S_delete(self, sql):
        try:
            self.cur.execute(sql)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


    # drop the table
    def dropTable(self, name):
        try:
            self.cur.execute('drop table ' + name + ';')
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def __del__(self):
        if self.cur != None:
            self.cur.close()
        if self.conn != None:
            self.conn.close()
