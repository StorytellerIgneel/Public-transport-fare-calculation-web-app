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
    from_id = request.args.get("from", type=int)
    to_id = request.args.get("to", type=int)

    if from_id is None or to_id is None:
        return jsonify({"error": "Missing 'from' or 'to' parameter"}), 400

    # --- Fetch stations in path (simple linear traversal) ---
    if from_id < to_id:
        station_query = """
            SELECT id, station, line FROM stations
            WHERE id BETWEEN ? AND ?
            ORDER BY id ASC
        """
        params = (from_id, to_id)
    else:
        station_query = """
            SELECT id, station, line FROM stations
            WHERE id BETWEEN ? AND ?
            ORDER BY id DESC
        """
        params = (to_id, from_id)

    station_rows = fetch_all(station_query, params)

    if not station_rows:
        return jsonify({"error": "No stations found for given IDs"}), 404

    path = []
    last_line = station_rows[0][2]  # starting line

    for station_id, station_name, line_name in station_rows:
        display_name = station_name

        # Detect interchange: same station name exists with multiple lines
        dup_query = "SELECT COUNT(*) FROM stations WHERE station = ?"
        dup_count = fetch_one(dup_query, (station_name,))[0]

        if dup_count > 1:  # it's an interchange station
            display_name = f"{station_name} ({line_name})"
            if line_name != last_line:
                path.append(f"<-- switched from {last_line} to {line_name} -->")

        # Detect line switch (moving to new line after interchange)
        elif last_line != line_name and station_id != station_rows[0][0]:
            display_name = f"{station_name} ({line_name})"

        path.append(display_name)
        last_line = line_name

    # --- Get fare using IDs ---
    fare_query = """
        SELECT fare FROM fares
        WHERE origin_id = ? AND destination_id = ?
    """
    fare = fetch_one(fare_query, (from_id, to_id))
    total_fare = float(fare[0]) if fare else None

    return jsonify({
        "path": path,
        "total_hops": len(path) - 1,
        "total_fare": total_fare
    }), 200
