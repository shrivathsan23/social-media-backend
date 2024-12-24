from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Interaction, InteractType

bp = Blueprint('interactions', __name__)

@bp.route('/liked', methods = ['GET'])
@jwt_required()
def get_liked_posts():
    page = request.args.get('page', 1, type = int)
    size = request.args.get('size', 10, type = int)
    
    user_id = get_jwt_identity()
    liked_posts_query = Interaction.query.filter_by(user_id = user_id, interaction_type = InteractType.LIKE)
    liked_posts = liked_posts_query.paginate(page = page, per_page = size, error_out = False).items
    
    return jsonify({
        'posts': [{
            'id': interaction.post.id,
            'content': interaction.post.content,
            'author': interaction.post.author.username,
            'timestamp': interaction.post.timestamp
        } for interaction in liked_posts]
    }), 200

@bp.route('/commented', methods = ['GET'])
@jwt_required()
def get_commented_posts():
    page = request.args.get('page', 1, type = int)
    size = request.args.get('size', 10, type = int)
    
    user_id = get_jwt_identity()
    commented_posts_query = Interaction.query.filter_by(user_id = user_id, interaction_type = InteractType.COMMENT)
    commented_posts = commented_posts_query.paginate(page = page, per_page = size, error_out = False).items
    
    return jsonify({
        'posts': [{
            'id': interaction.post.id,
            'content': interaction.post.content,
            'author': interaction.post.author.username,
            'timestamp': interaction.post.timestamp,
            'comment': interaction.content
        } for interaction in commented_posts]
    }), 200

@bp.route('/like/<int:post_id>', methods = ['POST'])
@jwt_required()
def like_post(post_id):
    user_id = get_jwt_identity()
    interaction = Interaction.query.filter_by(user_id = user_id, post_id = post_id, interaction_type = InteractType.LIKE).first()

    if interaction:
        db.session.delete(interaction)
        message = 'Like Removed'
    
    else:
        interaction = Interaction(user_id = user_id, post_id = post_id, interaction_type = InteractType.LIKE)
        db.session.add(interaction)
        message = 'Post Liked'
    
    db.session.commit()
    return jsonify({
        'message': message
    }), 200

@bp.route('/comment/<int:post_id>', methods = ['POST'])
@jwt_required()
def comment_on_post(post_id):
    data = request.json
    user_id = get_jwt_identity()
    interaction = Interaction(user_id = user_id, post_id = post_id, interaction_type = InteractType.COMMENT, content = data['content'])

    db.session.add(interaction)
    db.session.commit()

    return jsonify({
        'message': 'Comment added'
    }), 200