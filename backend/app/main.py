from flask import Blueprint, render_template
from app.utils import get_fields

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html', industries=get_fields())
