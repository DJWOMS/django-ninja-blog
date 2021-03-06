from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from . import models, schemas
from auth.jwt import AuthBearer

blog = Router()


@blog.get("/category", response=List[schemas.CategoryParent])
def gat_category(request):
    return models.Category.objects.filter(published=True)


@blog.get("/post", response=List[schemas.Post])
def gat_list_post(request):
    return models.Post.objects.filter(published=True)


@blog.get("/post/{post_pk}", response=schemas.Post)
def gat_single_post(request, post_pk: int):
    return get_object_or_404(models.Post, id=post_pk, published=True)


@blog.post("/comment", response=schemas.Comment, auth=AuthBearer())
def create_comment(request, comment: schemas.CreateComment):
    return models.Comment.objects.create(user=request.auth, **comment.dict())


@blog.put("/comment/{comment_id}", response=schemas.Comment, auth=AuthBearer())
def create_comment(request, comment_id: int, comment: schemas.CreateComment):
    _comment = get_object_or_404(models.Comment, id=comment_id, user=request.auth)
    _comment.post_id = comment.post_id
    _comment.text = comment.text
    _comment.parent_id = comment.parent_id
    _comment.save()
    return _comment


@blog.delete("/comment/{comment_id}", auth=AuthBearer())
def create_comment(request, comment_id: int):
    _comment = get_object_or_404(models.Comment, id=comment_id, user=request.auth)
    _comment.delete()
    return {"success": 204}


@blog.get("/{post_id}/comment", response=List[schemas.Comment])
def get_comments(request, post_id: int):
    return models.Comment.objects.filter(post_id=post_id)
