from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.db import get_session
from app.models.post import Post, PostCreate, PostPublic, PostUpdate

router = APIRouter()

# CREATE POST
@router.post(
    "/posts/",
    response_model=PostPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create a post",
    response_description="The created post",
)
async def create_post(post_create: PostCreate, session: Session = Depends(get_session)):
    """
    Create a post with all the information:

    - **title**: each post must have a title
    - **content**: a long content
    - **published**: default is False
    """
    post = Post.model_validate(post_create)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

# GET ALL POSTS
@router.get(
    "/posts/",
    response_model=list[PostPublic],
    summary="Get all posts",
    response_description="The list of posts",
)
async def read_posts(session: Session = Depends(get_session)):
    """
    Retrieve posts.
    """
    posts = session.exec(select(Post)).all()
    return posts

# GET ONE POST
@router.get(
    "/posts/{post_id}",
    response_model=PostPublic,
    summary="Get one post",
    response_description="The one post",
)
async def read_post(post_id: int, session: Session = Depends(get_session)):
    """
    Get a post by ID.
    """
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# UPDATE A POST
@router.patch(
    "/posts/{post_id}",
    response_model=PostPublic,
    summary="Update one post",
    response_description="The updated one post",
)
async def update_post(post_id: int, post_update: PostUpdate, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_data = post_update.model_dump(exclude_unset=True)
    post.sqlmodel_update(post_data)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

# DELETE A POST
@router.delete(
    "/posts/{post_id}",
    response_model=PostPublic,
    summary="Delete a post",
    response_description="The deleted post",
)
async def delete_post(post_id: int, session: Session = Depends(get_session)):
    """
    Delete a post by ID.
    """
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return post