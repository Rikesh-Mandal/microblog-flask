from app import db
from app.api import bp
from app.api.auth import token_auth
from app.models import Message
from flask import request, url_for
import sqlalchemy as sa

#get sent messages by a user
@bp.route('/messages/sent', methods=['GET'])
@token_auth.login_required
def get_sent_messages():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Message.to_collection_dict(sa.select(Message).where(Message.sender_id == token_auth.current_user().id),
                                       page, per_page, 'api.get_sent_messages')


#get messages received by a user
@bp.route('/messages/received', methods=['GET'])
@token_auth.login_required
def get_received_messages():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Message.to_collection_dict(sa.select(Message).where(Message.recipient_id == token_auth.current_user().id),
                                       page, per_page, 'api.get_received_messages')