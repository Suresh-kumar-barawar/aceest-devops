from flask import jsonify, request

clients = {}

PROGRAMS = {
    "Fat Loss (FL)": {
        "workout": "Mon: Back Squat 5x5 | Tue: EMOM Assault Bike | Wed: Bench Press | Thu: Deadlift | Fri: Cardio",
        "diet": "Breakfast: Egg Whites + Oats | Lunch: Grilled Chicken + Brown Rice | Dinner: Fish Curry + Millet Roti",
        "calorie_factor": 22
    },
    "Muscle Gain (MG)": {
        "workout": "Mon: Squat 5x5 | Tue: Bench 5x5 | Wed: Deadlift 4x6 | Thu: Front Squat | Fri: Rows",
        "diet": "Breakfast: Eggs + PB Oats | Lunch: Chicken Biryani | Dinner: Mutton Curry + Rice",
        "calorie_factor": 35
    },
    "Beginner (BG)": {
        "workout": "Full Body Circuit: Air Squats, Ring Rows, Push-ups | Focus: Technique",
        "diet": "Balanced Meals: Idli / Dosa / Rice + Dal | Protein Target: 120g/day",
        "calorie_factor": 26
    }
}

def register_routes(app):
    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to ACEest Fitness & Gym API", "status": "running"})

    @app.route("/programs", methods=["GET"])
    def get_programs():
        return jsonify({"programs": list(PROGRAMS.keys())})

    @app.route("/program/<name>", methods=["GET"])
    def get_program(name):
        if name not in PROGRAMS:
            return jsonify({"error": "Program not found"}), 404
        return jsonify({"program": name, "details": PROGRAMS[name]})

    @app.route("/calories", methods=["POST"])
    def calculate_calories():
        data = request.get_json()
        weight = data.get("weight")
        program = data.get("program")

        if weight is None or program is None:
            return jsonify({"error": "weight and program are required"}), 400
        if program not in PROGRAMS:
            return jsonify({"error": "Invalid program"}), 404
        if weight <= 0:
            return jsonify({"error": "Weight must be positive"}), 400

        calories = int(weight * PROGRAMS[program]["calorie_factor"])
        return jsonify({"weight": weight, "program": program, "calories": calories})

    @app.route("/clients", methods=["POST"])
    def add_client():
        data = request.get_json()
        name = data.get("name")

        if not name:
            return jsonify({"error": "name is required"}), 400
        if name in clients:
            return jsonify({"error": "Client already exists"}), 409

        clients[name] = {
            "age": data.get("age"),
            "weight": data.get("weight"),
            "program": data.get("program"),
            "adherence": data.get("adherence", 0)
        }
        return jsonify({"message": f"Client {name} added", "client": clients[name]}), 201

    @app.route("/clients", methods=["GET"])
    def get_clients():
        return jsonify({"clients": clients})

    @app.route("/clients/<name>", methods=["GET"])
    def get_client(name):
        if name not in clients:
            return jsonify({"error": "Client not found"}), 404
        return jsonify({"client": clients[name]})
