from flask import Flask, render_template, request
from collections import deque
import heapq
import json

app = Flask(__name__)

def bfs_path(graph, start, end):

    queue = deque()

    queue.append((start, [start]))

    visited = set()

    while queue:

        current_city, path = queue.popleft()

        if current_city == end:
            return path

        visited.add(current_city)

        for neighbor in graph[current_city]:

            if neighbor not in visited:

                queue.append(
                    (
                        neighbor,
                        path + [neighbor]
                    )
                )

    return None

def calculate_distance(graph, path):

    total_distance = 0

    for i in range(len(path) - 1):

        current_city = path[i]
        next_city = path[i + 1]

        total_distance += graph[current_city][next_city]

    return total_distance

def dijkstra(graph, start, end):

    pq = []

    heapq.heappush(
        pq,
        (0, start, [start])
    )

    visited = set()

    while pq:

        distance, current_city, path = heapq.heappop(pq)

        if current_city == end:
            return path, distance

        if current_city in visited:
            continue

        visited.add(current_city)

        for neighbor, weight in graph[current_city].items():

            if neighbor not in visited:

                heapq.heappush(
                    pq,
                    (
                        distance + weight,
                        neighbor,
                        path + [neighbor]
                    )
                )

    return None, None

def estimate_time(distance, speed):

    hours = distance / speed
    h = int(hours)
    minutes = int((hours-h)*60)
    return f"{h} hr {minutes} min"

@app.route("/")
def home():

    with open("data/routes.json") as file:
        routes = json.load(file)

    cities = list(routes.keys())

    return render_template(
        "index.html",
        cities=cities,
        selected_speed=60,
        result=None
    )

@app.route("/route", methods=["POST"])
def route():

    source = request.form["source"]
    destination = request.form["destination"]
    speed = int(request.form["speed"])

    with open("data/routes.json") as file:
        routes = json.load(file)

    cities = list(routes.keys())

    result = None

    path, total_distance = dijkstra(
        routes,
        source,
        destination
    )

    if path:

        route_text = " → ".join(path)

        travel_time = estimate_time(total_distance, speed)

        result = {
            "path": route_text,
            "distance": total_distance,
            "time":travel_time,
            "speed":speed
        }

    else:


        result = {
            "path": "No Route Found",
            "distance": "-"
        }

    return render_template(
        "index.html",
        cities=cities,
        result=result,
        selected_source=source,
        selected_destination=destination,
        selected_speed=speed
        )

if __name__ == "__main__":
    app.run(debug=True)