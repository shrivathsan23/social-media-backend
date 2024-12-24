from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Post, Interaction, InteractType

bp = Blueprint('posts', __name__)

@bp.route('/', methods = ['POST'])
@jwt_required()
def create_post():
    data = request.json
    user_id = get_jwt_identity()
    post = Post(content = data['content'], user_id = user_id)

    db.session.add(post)
    db.session.commit()

    return jsonify({
        'message': 'Post created succesfully'
    }), 201

@bp.route('/', methods = ['GET'])
def get_posts():
    page = request.args.get('page', 1, type = int)
    size = request.args.get('size', 10, type = int)
    
    posts_query = Post.query.order_by(Post.timestamp.desc())
    posts = posts_query.paginate(page = page, per_page = size, error_out = False).items

    return jsonify({
        'page': page,
        'size': size,
        'posts': [{
            'id': post.id,
            'content': post.content,
            'author': post.author.username,
            'timestamp': post.timestamp
        } for post in posts]
    }), 200

@bp.route('/<int:post_id>', methods = ['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({
            'error': 'Post not found'
        }), 404
    
    likes = Interaction.query.filter_by(post_id = post_id, interaction_type = InteractType.LIKE).count()
    comments = Interaction.query.filter_by(post_id = post_id, interaction_type = InteractType.COMMENT).all()

    return jsonify({
        'id': post.id,
        'content': post.content,
        'author': post.author.username,
        'timestamp': post.timestamp,
        'likes': likes,
        'comments': [{
            'id': comment.id,
            'comment': comment.content,
            'commenter': comment.user.username,
            'timestamp': comment.timestamp
        } for comment in comments]
    }), 200