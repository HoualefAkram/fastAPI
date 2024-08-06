from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

while True:
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="0777910785",
            cursor_factory=RealDictCursor,
        )
        cursor = connection.cursor()
        print("Database connection Done")
        break
    except Exception as error:
        print(f"connecting to db failed: {error}")
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


my_posts: list = [
    {
        "id": 1,
        "title": "title1",
        "content": "content1",
    },
    {
        "id": 2,
        "title": "title2",
        "content": "content2",
    },
    {
        "id": 3,
        "title": "title3",
        "content": "content3",
    },
]


@app.get("/")
def root():
    return {"message": "Root"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found",
        )
    connection.commit()


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts(title, content,published) VALUES(%s, %s, %s) RETURNING *""",
        (
            post.title,
            post.content,
            post.published,
        ),
    )
    new_post = cursor.fetchone()
    connection.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    connection.commit()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found",
        )
    return {"data": post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (
            post.title,
            post.content,
            str(post.published),
            str(id),
        ),
    )

    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found",
        )
    return {
        "data": updated_post,
    }
