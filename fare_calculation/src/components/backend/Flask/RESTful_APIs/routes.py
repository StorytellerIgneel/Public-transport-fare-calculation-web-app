from flask import Blueprint, request, jsonify
from db_scripts.database import fetch_one, fetch_all, get_db_connection   # ✅ make sure this exists

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

def load_stations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, station, Latitude, Longitude, Line FROM stations")
    rows = cursor.fetchall()
    conn.close()

    stations = []
    for row in rows:
        stations.append({
            "id": row[0],
            "name": row[1],
            "lat": row[2],
            "lng": row[3],
            "line": row[4]
        })
    return stations

from collections import defaultdict
import re

def build_graph(stations):
    graph = defaultdict(list)

    # Group by line
    line_groups = defaultdict(list)
    for s in stations:
        line_groups[s["line"]].append(s)
    
    # Sort each line by station id (assumes id order follows route)
    for line, nodes in line_groups.items():
        nodes.sort(key=lambda x: x["id"])
        for i in range(len(nodes) - 1):
            a = f"{nodes[i]['name']} ({line})"
            b = f"{nodes[i+1]['name']} ({line})"
            graph[a].append(b)
            graph[b].append(a)

    # Add interchange links
    name_groups = defaultdict(list)
    for s in stations:
        normalized_name = re.sub(r'\s*\([^)]+\)$', '', s["name"]).strip()
        name_groups[normalized_name].append(s)

    for same_name, nodes in name_groups.items():
        if len(nodes) > 1:  # Interchange
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    a = f"{nodes[i]['name']} ({nodes[i]['line']})"
                    b = f"{nodes[j]['name']} ({nodes[j]['line']})"
                    graph[a].append(b)
                    graph[b].append(a)

    return graph

from collections import deque
def bfs_shortest_path(graph, start, goal):
    visited = set()
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
            visited.add(node)
    return None

@routes_bp.route("/route", methods=["GET"])
def get_route():
    from_id = request.args.get("from", type=int)
    to_id = request.args.get("to", type=int)

    if from_id is None or to_id is None:
        return jsonify({"error": "Missing 'from' or 'to' parameter"}), 400

    stations = load_stations()
    graph = build_graph(stations)

    from_station = next((s for s in stations if s["id"] == from_id), None)
    to_station = next((s for s in stations if s["id"] == to_id), None)

    if not from_station or not to_station:
        return jsonify({"error": "Invalid station IDs"}), 404

    start = f"{from_station['name']} ({from_station['line']})"
    goal = f"{to_station['name']} ({to_station['line']})"

    # BFS traversal for shortest hops
    path = bfs_shortest_path(graph, start, goal)
    if not path:
        return jsonify({"error": "No path found"}), 404

    return jsonify({
        "path": path,
        "total_hops": len(path) - 1
    }), 200

