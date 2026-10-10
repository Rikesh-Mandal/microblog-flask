from app.api import bp
from app.api.auth import token_auth
from app import db
from app.models import Post, User
from flask import request, url_for
import sqlalchemy as sa
from flask import abort
from app.api.errors import bad_request, error_response
from datetime import datetime, timezone

#get post by id
@bp.route('/posts/<int:id>', methods = ['GET'])
@token_auth.login_required
def get_post(id):
    return db.get_or_404(Post, id).to_dict()


#get all posts
@bp.route('/posts', methods=['GET'])
@token_auth.login_required
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Post.to_collection_dict(sa.select(Post), page, per_page, 'api.get_posts')


#get post by a certain user using user id
@bp.route('/users/<int:user_id>/posts', methods=['GET'])
@token_auth.login_required
def get_user_posts(user_id):
    db.get_or_404(User, user_id)
    if token_auth.current_user().id != user_id:
        abort(403)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Post.to_collection_dict(sa.select(Post).where(Post.user_id == user_id), page, per_page, 'api.get_user_posts', user_id = user_id)


@bp.route('/posts/<int:id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers_posts():
    pass


@bp.route('/posts/<int:id>/following', methods=['GET'])
@token_auth.login_required
def get_following_posts():
    pass


#create a post
@bp.route('/posts', methods=['POST'])
@token_auth.login_required
def create_post():
    if not request.is_json:
        return error_response(415,'Content-Type must be application/json')
    data = request.get_json()
    if not data or 'body' not in data:
        return bad_request('Body is required')
    post = Post()
    post.author = token_auth.current_user()
    post.from_dict(data)
    db.session.add(post)
    db.session.commit()
    return post.to_dict(), 201, {'Location': url_for('api.get_post', id=post.id)}


#update a post
@bp.route('/posts/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_post(id):
    post = db.get_or_404(Post, id)
    if token_auth.current_user().id != post.user_id:
        abort(403)
    if not request.is_json:
        return error_response(415,'Content-Type must be application/json')
    data = request.get_json()
    if not data or 'body' not in data:
        return bad_request('Body is required')
    post.from_dict(data)
    post.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return post.to_dict()


#delete a post
@bp.route('/posts/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_post(id):
    post = db.get_or_404(Post, id)
    if token_auth.current_user().id != post.user_id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return '', 204

