import stat
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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


def find_post(id: int) -> dict:
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
def root():
    return {"message": "Root"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index = find_index_post(id=id)
    if not post_index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    my_posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    my_posts.append(post.model_dump())
    return {"data": post}


@app.get("/posts/{id}")
def get_posts(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return {
        "post": post,
    }


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_index = find_index_post(id=id)
    post_dict = post.model_dump()
    post_dict["id"] = id
    if post_index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    my_posts[post_index] = post_dict
    return {
        "data": post,
    }
