from fastapi import HTTPException, status, Depends
from fastapi.routing import APIRouter
from sqlalchemy.sql.expression import label
from sqlalchemy.sql.functions import count
from .. import models, schemas
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm.session import Session
from ..database import get_db
from typing import List, Optional
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


posts = [{"title": "post 1", "content": "post1 content", "id": 1},
         {"title": "post 2", "content": "post2 content", "id": 2}]


def find_post_with_id(id: int):
    for post in posts:
        if post['id'] == id:
            return post


def find_index_for_post(id: int):
    for i, post in enumerate(posts):
        if post['id'] == id:
            return i


@router.get("/", response_model=List[schemas.PostAndVotes])
def get_posts(db: Session = Depends(get_db),   current_user: models.User = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # SELECT posts.*, Count(*) as votes FROM posts LEFT OUTER JOIN votes ON posts.id = votes.post_id group by posts.id
    # above query with Count(*) will count rows from votes table even if the values are null, so for the posts where not vote is there it will give count as 1

    # SELECT posts.*, Count(votes.post_id) as votes FROM posts LEFT OUTER JOIN votes ON posts.id = votes.post_id group by posts.id
    # above query with Count(votes.post_id) will only consider rows where the votes.post_id is not null

    posts_query = db.query(models.Post, count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    posts = posts_query.all()
    return posts


@router.get("/{id}", response_model=schemas.PostAndVotes)
def get_post(id: int, db: Session = Depends(get_db),  current_user: models.User = Depends(get_current_user)):
    # post = find_post_with_id(id)
    # cursor.execute(''' SELECT * from posts WHERE id = (%s) ''', (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    posts_query = db.query(models.Post, count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).where(models.Post.id == id).group_by(models.Post.id)
    post = posts_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"could not find the post with id {id}")

    return post


# this route depends on get_current_user, which ensures that the user is loggedIn
# before performing this action

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # fastapi does auto validation of the post object that we receive, if any of the field is not
    # same as the defined schema it throws an error.

    # id = randrange(3, 10000000)
    # new_post = post.dict()
    # new_post['id'] = id
    # posts.append(new_post)

    # we should not use the f-string to format the sql query, it may cause sql injection
    # cursor.execute(''' INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''',
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # ORM based implementation
    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)

    post_copy = post.dict()
    post_copy.update({'owner_id': current_user.id})
    new_post = models.Post(**post_copy)
    db.add(new_post)
    db.commit()
    # retrive the newly created post and store it in new_post
    db.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),  current_user: models.User = Depends(get_current_user)):
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"could not update the post with id {id}")

    # post_updates = post.dict()
    # post_index = find_index_for_post(id)
    # posts[post_index] = post_updates

    # cursor.execute(
    #     '''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    #    if not updated_post:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                             detail=f"could not update the post with id {id}")

    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_be_updated = post_query.first()
    if not post_to_be_updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"could not find the post with id {id}")

    if post_to_be_updated.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to perform this operation!")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{id}",)
def delete_post(id: int, db: Session = Depends(get_db),  current_user: models.User = Depends(get_current_user)):
    # post_index = find_index_for_post(id)
    # if not post_index:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"could not find the post with id {id}")

    # posts.pop(post_index)
    # cursor.execute(
    #     '''DELETE FROM posts WHERE id = (%s) RETURNING *''', (str(id)))
    # delete_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"could not find the post with id {id}")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You can not perform delete operation for this post")

    post_query.delete(synchronize_session=False)
    db.commit()
    return f"Post with id {id} deleted successfully"
