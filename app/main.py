from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title : str
    content: str

@app.post("/createposts")
def post_test(new_post: Post):
    print(f"title: {new_post.title}, content: {new_post.content}")
    return {"message" : "Post created"}
