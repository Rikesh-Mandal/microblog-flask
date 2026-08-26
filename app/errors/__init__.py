#blueprint creates a sort of mini app for the defiend directory
from flask import Blueprint

bp = Blueprint('errors',__name__)

#adding the handlers.py so that it is part of the mini app
from app.errors import handlers