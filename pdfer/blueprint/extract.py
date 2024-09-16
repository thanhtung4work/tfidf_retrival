import functools

from   flask import (
    Blueprint, flash, g, 
    redirect, render_template, request, 
    session, url_for, jsonify
)

from   ..utils import extract_document

bp = Blueprint('extract', __name__, url_prefix='/extract')


@bp.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('extract.html')
    
    data = request.json
    sim_index = extract_document(
        data.get('query'),
    )
    return jsonify(sim_index), 200