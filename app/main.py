from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from models.posts import Post
from models.engine.file_storage import FileStorage
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time

load_dotenv()

app = FastAPI()



HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")

while True:
    try:
        conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts")
        print(cursor.fetchall())
        break
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        time.sleep(2)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts/")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}
@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (id, title, content, published) VALUES (%s, %s, %s, %s) RETURNING * """,
                   (post.id, post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}



@app.get("/posts/latest")
async def get_latest_post():
    pass

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (post_id,))
    post = cursor.fetchone()
    if post:
        return {"data": post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (post_id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")



@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, post_id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post:
        return {"data": updated_post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

