from flask import Flask, render_template,redirect,url_for
from flask import request
import psycopg2
import hashlib
from Crypto.Cipher import DES
import numbers
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def home():
    if request.method == 'POST':
        if request.form['submit']=='Submit':
            pass
            name = request.form['username']
            pasword= request.form['psw']
            pasword= encrypt(pasword)
            pasword= unicode(pasword, "ISO-8859-1")
            conn = psycopg2.connect("dbname=project user=postgres password='darjeeling'")
            cur=conn.cursor()
            sql_query = "select id from temp_data where username= '%s' and  paswrd= '%s'; " % (name,pasword)
            print sql_query
            cur.execute(sql_query)
			#conn.commit()
            data = cur.fetchone()
            if data is None:
                return "Not found pls register"
            else:
                return "WELCOME TO THE NEW PAGE"
			#x=cur.fetchone()[0]
			#check=isinstance (x,numbers.Integral)
			#if check:
			#	return "WELCOME TO THE NEW PAGE"
			#else :
			#	return "Not found pls register"
        elif request.form['submit']=='Register':
            pass
            return redirect('sample')
        else :
            return render_template('home.html')
    else:
	    return render_template('home.html')




@app.route('/sample',methods=['POST','GET'])
def sample():
    if request.method == 'POST':
        pass
        emai_id=request.form['emailid']
        fstname=request.form['firstname']
        lastnme=request.form['lastname']
        date=request.form['DOB']
        contact=request.form['contact']
        usrname=request.form['username']
        paswrd=request.form['paswrd']
        paswrd= encrypt(paswrd)
        paswrd= unicode(paswrd, "ISO-8859-1")
        conn = psycopg2.connect("dbname=project user=postgres password='darjeeling'")
        cur=conn.cursor()
        sql_query = "INSERT INTO personal_info VALUES ('%s','%s','%s','%s','%s','%s','%s');" % (emai_id,fstname,lastnme,date,contact,usrname,paswrd)
        print sql_query
        cur.execute(sql_query)
        conn.commit()
        sql_query=  "INSERT INTO temp_data select '%s','%s',idnumber from personal_info where user_name= '%s' and pass_word= '%s';" % (usrname,paswrd,usrname,paswrd)
        print sql_query
        cur.execute(sql_query)
        conn.commit()
        return "New Registration completed"
    else:
        return render_template('sample.html')

def encrypt(sample1):
    hsh1=hashlib.sha224(sample1).hexdigest()
    key1=hsh1[:8]
    key2=hsh1[-8:]
    str=len(sample1)
    str=str%8
    i=0
    while(str!=0):
        sample1=sample1+sample1[i]
        i=i+1
        str=(len(sample1))%8
    des=DES.new(key1,DES.MODE_ECB)
    cp1=des.encrypt(sample1)
    des=DES.new(key2,DES.MODE_ECB)
    cp2=des.encrypt(cp1)
    des=DES.new(key1,DES.MODE_ECB)
    cp3=des.encrypt(cp2)
    return cp3

if __name__ == '__main__':
    app.run(debug=True,port=5001)
