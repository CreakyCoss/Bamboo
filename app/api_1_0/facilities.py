from . import api
from flask import jsonify
from ..models import Facility


@api.route('/facility/<int:id>')
def get_facility(id):
    facility = Facility.query.get_or_404(id)
    return jsonify(facility.to_json())