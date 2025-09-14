from components.backend.db_scripts import database
from flask import Blueprint, request, jsonify

station_bp = Blueprint('routes', __name__)

@station_bp.route('/fares', methods=['GET'])