from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app and OpenAI client
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/generate-workout", methods=["POST"])
def generate_workout():
    # Get JSON data from the request
    data = request.get_json()

    # Validate input data
    required_fields = ["age", "fitness_level", "goal", "equipment"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    age = data["age"]
    fitness_level = data["fitness_level"]
    goal = data["goal"]
    equipment = data["equipment"]

    # Create a prompt for the OpenAI API
    prompt = f"""
    Create a personalized 7-day workout plan for someone who is:
    - Age: {age}
    - Fitness Level: {fitness_level}
    - Goal: {goal}
    - Available Equipment: {equipment}

    Include warm-up, workout, and cool-down details. Use a motivating tone.
    """

    try:
        # Call the OpenAI API to generate the workout plan
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        workout_plan = response.choices[0].message.content.strip()
        return jsonify({"workout_plan": workout_plan})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)