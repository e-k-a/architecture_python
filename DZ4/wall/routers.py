from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import List
from schemas import PostCreate, PostUpdate, PostInDB
from methods import get_current_user, create_post, get_post, update_post, delete_post

router = APIRouter()

@router.post("/", response_model=PostInDB)
def create_posts(
    post: PostCreate,
    current_user: dict = Depends(get_current_user),
):
    print(post.dict())
    print(current_user["id"])
    return create_post(post.dict(), current_user["id"])

@router.get("/{post_id}", response_model=PostInDB)
def get_posts(
    post_id: str,
    current_user: dict = Depends(get_current_user),
):
    post = get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    if not post.is_public and post.author_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this post"
        )
    
    return post

@router.get("/", response_model=List[PostInDB])
def get_postss(
    skip: int = 0,
    limit: int = 10,
    only_my: bool = False,
    current_user: dict = Depends(get_current_user),
):
    author_id = current_user["id"] if only_my else None
    return get_posts(skip, limit, author_id)

@router.put("/{post_id}", response_model=PostInDB)
async def update_posts(
    post_id: str,
    post_update: PostUpdate,
    current_user: dict = Depends(get_current_user),
):
    post = get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    if post.author_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to modify this post"
        )
    
    update_data = post_update.dict(exclude_unset=True)
    return update_post(post_id, update_data)

@router.delete("/{post_id}")
async def delete_post(
    post_id: str,
    current_user: dict = Depends(get_current_user),
):
    post = get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    if post.author_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this post"
        )
    
    delete_post(post_id)
    return None