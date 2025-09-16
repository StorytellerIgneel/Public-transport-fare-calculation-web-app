from flask import Blueprint, request, jsonify
from db_scripts.database import fetch_one, fetch_all   # ✅ make sure this exists

routes_bp = Blueprint("routes", __name__)

@routes_bp.route('/stations', methods=["GET"])
def get_stations():
    
    query = "SELECT * FROM stations"
    
    stations = fetch_all(query)
    
    if stations:
        return jsonify({"station": stations}), 200
    else:
        return jsonify({"error": "Station not found"}), 404

@routes_bp.route("/fares", methods=["GET"])
def get_fare():
    from_station = request.args.get("from")
    to_station = request.args.get("to")

    query = """
        SELECT fare
        FROM fares
        WHERE origin_id = ? AND destination_id = ?
    """

    fare = fetch_one(query, (from_station, to_station))

    if fare:
        return jsonify({"fare": fare[0]}), 200
    else:
        return jsonify({"error": "Fare not found"}), 404

@routes_bp.route("/route", methods=["GET"])
def get_route():
    from_station = request.args.get("from")
    to_station = request.args.get("to")

    # Validate stations
    station_query = "SELECT id, name FROM stations WHERE id = ?"
    origin = fetch_one(station_query, (from_station,))
    destination = fetch_one(station_query, (to_station,))

    if not origin or not destination:
        return jsonify({"error": "Invalid station(s)"}), 404

    # Query all hops between origin and destination
    # ⚠️ This assumes you have a `routes` or `station_order` table
    # with line sequences for the stations.
    path_query = """
        SELECT s.name
        FROM station_order so
        JOIN stations s ON so.station_id = s.id
        WHERE so.line_id = (
            SELECT line_id FROM station_order WHERE station_id = ?
        )
        AND so.order BETWEEN 
            (SELECT order FROM station_order WHERE station_id = ?) 
            AND 
            (SELECT order FROM station_order WHERE station_id = ?)
        ORDER BY so.order
    """

    path = fetch_all(path_query, (from_station, from_station, to_station))

    if not path:
        return jsonify({"error": "No route found"}), 404

    # Flatten path from tuples -> list of names
    path_list = [row[0] for row in path]

    # Count hops
    total_hops = len(path_list) - 1

    # Get fare
    fare_query = """
        SELECT fare FROM fares
        WHERE origin_id = ? AND destination_id = ?
    """
    fare = fetch_one(fare_query, (from_station, to_station))

    if not fare:
        return jsonify({"error": "Fare not found"}), 404

    return jsonify({
        "path": path_list,
        "total_hops": total_hops,
        "total_fare": fare[0]
    }), 200
