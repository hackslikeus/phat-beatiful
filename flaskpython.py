from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

def run_mpc(*args):
    """Run an mpc command and return its output."""
    result = subprocess.run(["mpc", *args], capture_output=True, text=True)
    return result.stdout.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "fast_forward":
            run_mpc("seek", "+10%")
        elif action == "rewind":
            run_mpc("seek", "-10%")
        elif action == "volume_up":
            run_mpc("volume", "+5")
        elif action == "volume_down":
            run_mpc("volume", "-5")
        elif action == "play_pause":
            run_mpc("toggle")

    # Fetch current status to display on the page
    status = run_mpc("status")
    return render_template("index.html", status=status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)   
