from flask import Flask, request
import psycopg2

app=Flask(__name__)
# database details
hostname= 'localhost'
database='mydatabase'
username='postgres'
pwd='kunal@191105'
port_id=5432


#I am using psql so establishing connection
def get_db():
    conn=psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    return conn

@app.route('/register',methods=["POST"])
def register():
    conn=get_db()
    curr=conn.cursor()
    curr.execute('''SELECT * FROM users''')

    alldata=curr.fetchall()
    
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    contact = data.get('contact')
    pwd = data.get('pwd')
    register_values=(name,email,contact,pwd)

    if not name or not email or not contact:
        return {"message": "Name, email, and contact are required"}, 400
    
    for i in alldata:
        if i[2]==email:
            curr.close()
            conn.close()
            return {"message": "email is already occupied"}, 400
        if str(i[3])==contact:
            curr.close()
            conn.close()
            return {"message": "mobile number is already occupied"}, 400
    
    curr.execute('''INSERT INTO database (s_name,s_email,s_isAdmin,s_contact,pwd) VALUES(%s,%s,%s,%s)''',register_values)            
    conn.commit()
    curr.close()
    conn.close()
    return {"message":f"ho gaya register ab login karo {register_values[0]}"}

@app.route('/login',methods=["POST"])
def login():
    conn=get_db()
    curr=conn.cursor()
    curr.execute('''SELECT * FROM users''')

    alldata=curr.fetchall()

    data = request.get_json()
    email = data.get('email')
    pwd = data.get('pwd')
    curr.close()
    conn.close()
    for i in alldata:
        if i[2]==email:
            if i[4]==pwd:
                curr.close()
                conn.close()
                return {"message": f"{i[1]} login in successfully!"}, 200
            else:
                curr.close()
                conn.close()
                return {"message": "You have entered wrong password"}, 400
    
            
    curr.close()
    conn.close()
    return {"message": "incorrect information"}, 400


#CRUD for blog

#getting all database at once and creating a new blog
@app.route('/blog',methods=["GET","POST"])
def blog():
    if request.method=="GET":
        conn=get_db()
        curr=conn.cursor()
        curr.execute('''SELECT * FROM blogs''')

        alldata=curr.fetchall()
        return alldata
    if request.method=="POST":
        conn=get_db()
        curr=conn.cursor()
        curr.execute('''SELECT * FROM blogs''')

        alldata=curr.fetchall()

        data = request.get_json()
        blog_id = data.get('blog_id')
        blog_title = data.get('blog_title')
        blog_content = data.get('blog_content')
        blog_author = data.get('blog_author')
        blog_timestamps = data.get('blog_timestamps')
        register_values=(blog_id,blog_title,blog_content,blog_author,blog_timestamps)

        for i in alldata:
            if i[0]==blog_id:
                curr.close()
                conn.close()
                return {"message": "blog already exists please update existing blog"}, 200
            
        curr.execute('''INSERT INTO blogs (blog_id,blog_title,blog_content,blog_author,blog_timestamps) VALUES(%s,%s,%s,%s,%s)''',register_values)            
        conn.commit()
        curr.close()
        conn.close()
        return {"message": "blog has been added"}, 200
        

# CRUD for individual blog
@app.route("/blog/<blog_id>",methods=["GET","PUT","DELETE"])
def blogs(blog_id):
    if request.method=="GET":
        conn=get_db()
        curr=conn.cursor()
        curr.execute('''SELECT * FROM blogs''')

        alldata=curr.fetchall()

        for i in alldata:
            if i[0]==blog_id:
                return i
                
        return {"message": "blog is not present in database"}, 400
    

    if request.method=="PUT":
        conn=get_db()
        curr=conn.cursor()
        curr.execute('''SELECT * FROM blogs''')

        alldata=curr.fetchall()

        data = request.get_json()
        blog_title = data.get('blog_title')
        blog_content = data.get('blog_content')
        blog_author = data.get('blog_author')
        blog_timestamps = data.get('blog_timestamps')
        for i in alldata:
            if i[0]==blog_id:

                curr.execute('''UPDATE blogs SET blog_title=%s, blog_content=%s, blog_author=%s, blog_timestamps=%s WHERE blog_id=%s''', (blog_title, blog_content, blog_author, blog_timestamps, blog_id))
                conn.commit()
                curr.close()
                conn.close()
                return {"message": "blog is updated"}, 200
        curr.close()
        conn.close()
        return {"message": "blog is not present in database"}, 400
    
    if request.method=="DELETE":
        conn=get_db()
        curr=conn.cursor()
        curr.execute('''SELECT * FROM blogs''')

        alldata=curr.fetchall()
        for i in alldata:
            if i[0]==blog_id:
                curr.execute('''DELETE FROM blogs WHERE blog_id=%s''', (blog_id,))
                conn.commit()
                curr.close()
                conn.close()
                return {"message": "blog is deleted"}, 200
        curr.close()
        conn.close()
        return {"message": "blog is not present in database"}, 400
        
    
#CRUD for comments


#getting all database at once and creating a new comment
@app.route('/comments',methods=["GET","POST"])
def comment():
    if request.method=="GET":
        conn=get_db()
        curr=conn.cursor()
        curr.execute('''SELECT * FROM comments''')

        alldata=curr.fetchall()
        return alldata
    if request.method=="POST":
        conn=get_db()
        curr=conn.cursor()
        curr.execute('''SELECT * FROM comments''')

        alldata=curr.fetchall()

        data = request.get_json()
        comment_id = data.get('comment_id')
        comment_content = data.get('comment_content')
        comment_author = data.get('comment_author')
        comment_timestamps = data.get('comment_timestamps')
        register_values=(comment_id,comment_content,comment_author,comment_timestamps)

        for i in alldata:
            if i[0]==comment_id:
                curr.close()
                conn.close()
                return {"message": "comment already exists please update existing comment"}, 200
            
        curr.execute('''INSERT INTO comments (comment_id,comment_content,comment_author,comment_timestamps) VALUES(%s,%s,%s,%s)''',register_values)            
        conn.commit()
        curr.close()
        conn.close()
        return {"message": "comment has been added"}, 200
      

# CRUD for individual blog
@app.route("/comment/<comment_id>",methods=["GET","PUT","DELETE"])
def blogs(comment_id):
    if request.method=="GET":
        conn=get_db()
        curr=conn.cursor()
        curr.execute('''SELECT * FROM comments''')

        alldata=curr.fetchall()

        for i in alldata:
            if i[0]==comment_id:
                return i
                
        return {"message": "comment is not present in database"}, 400
    

    if request.method=="PUT":
        conn=get_db()
        curr=conn.cursor()
        curr.execute('''SELECT * FROM comments''')

        alldata=curr.fetchall()

        data = request.get_json()
        comment_content = data.get('comment_content')
        comment_author = data.get('comment_author')
        comment_timestamps = data.get('comment_timestamps')
        for i in alldata:
            if i[0]==comment_id:

                curr.execute('''UPDATE comments SET comment_content=%s, comment_author=%s, comment_timestamps=%s WHERE comment_id=%s''', (comment_content, comment_author, comment_timestamps, comment_id))
                conn.commit()
                curr.close()
                conn.close()
                return {"message": "comment is updated"}, 200
        curr.close()
        conn.close()
        return {"message": "comment is not present in database"}, 400
    
    if request.method=="DELETE":
        conn=get_db()
        curr=conn.cursor()
        curr.execute('''SELECT * FROM comment''')

        alldata=curr.fetchall()
        for i in alldata:
            if i[0]==comment_id:
                curr.execute('''DELETE FROM blogs WHERE blog_id=%s''', (comment_id,))
                conn.commit()
                curr.close()
                conn.close()
                return {"message": "comment is deleted"}, 200
        curr.close()
        conn.close()
        return {"message": "comment is not present in database"}, 400

if __name__=="__main__":
    app.run(debug=True)