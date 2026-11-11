import subprocess
from flask import Flask, redirect, render_template_string, url_for
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

app = Flask(__name__)

# HTML template with Button Group and Shutdown Modal
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>DietPi MPD Remote</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            text-align: center; 
            margin-top: 50px; 
            background-color: #f4f4f9; 
        }
        h1 { color: #333; }
        
        /* Button Group Styling */
        .btn-group {
            display: inline-flex;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
            margin: 20px 0;
        }
        .btn-group button {
            background-color: #007BFF;
            color: white;
            border: none;
            padding: 15px 20px;
            font-size: 16px;
            cursor: pointer;
            border-right: 1px solid rgba(255,255,255,0.2);
            transition: background-color 0.2s;
        }
        .btn-group button:last-child {
            border-right: none;
        }
        .btn-group button:hover { background-color: #0056b3; }
        .btn-group button.action-btn { background-color: #28a745; }
        .btn-group button.action-btn:hover { background-color: #218838; }

        /* Secondary Row (Volume & Power) */
        .secondary-controls {
            margin-top: 15px;
        }
        button.vol-btn { background-color: #ffc107; color: black; }
        button.vol-btn:hover { background-color: #e0a800; }
        button.power-btn { background-color: #dc3545; color: white; }
        button.power-btn:hover { background-color: #bd2130; }

        .btn-general {
            font-size: 16px;
            padding: 12px 20px;
            margin: 5px;
            cursor: pointer;
            border: none;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        /* Modal / Dialog Styling */
        .modal {
            display: none; 
            position: fixed; 
            z-index: 1000; 
            left: 0;
            top: 0;
            width: 100%; 
            height: 100%; 
            background-color: rgba(0,0,0,0.5); 
            align-items: center;
            justify-content: center;
        }
        .modal-content {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            width: 320px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        .modal-content h3 { margin-top: 0; color: #333; }
        .modal-buttons { margin-top: 20px; display: flex; justify-content: space-around; }
    </style>
</head>
<body>
    <h1>DietPi MPD Web Control</h1>
    <p>Loaded Playlist: <b>radio.m3u</b></p>
    
    <!-- Grouped Playback Controls -->
    <div class="btn-group">
        <form action="/control/previous" method="post" style="margin:0;">
            <button type="submit" title="Previous">⏮ Previous</button>
        </form>
        <form action="/control/toggle" method="post" style="margin:0;">
            <button type="submit" class="action-btn" title="Play / Pause">⏯ Play / Pause</button>
        </form>
        <form action="/control/next" method="post" style="margin:0;">
            <button type="submit" title="Fast Forward">⏩ Fast Forward</button>
        </form>
    </div>
    
    <br>

    <!-- Volume Controls -->
    <div class="secondary-controls">
        <form action="/control/vol_down" method="post" style="display:inline;">
            <button type="submit" class="btn-general vol-btn">🔉 Volume -10</button>
        </form>
        <form action="/control/vol_up" method="post" style="display:inline;">
            <button type="submit" class="btn-general vol-btn">🔊 Volume +10</button>
        </form>
    </div>

    <br><br>

    <!-- Shutdown Button (Triggers Modal) -->
    <div>
        <button type="button" class="btn-general power-btn" onclick="openModal()">⏻ Shutdown</button>
    </div>

    <!-- Power Management Modal -->
    <div id="shutdownModal" class="modal">
        <div class="modal-content">
            <h3>System Power Options</h3>
            <p>Select an action for your DietPi system:</p>
            <div class="modal-buttons">
                <!-- Shutdown Option -->
                <form action="/control/shutdown" method="post">
                    <button type="submit" class="btn-general power-btn" style="padding: 10px 15px;">Shutdown</button>
                </form>
                <!-- Reboot Option -->
                <form action="/control/reboot" method="post">
                    <button type="submit" class="btn-general vol-btn" style="padding: 10px 15px;">Reboot</button>
                </form>
                <!-- Cancel Option -->
                <button type="button" class="btn-general" style="background-color: #6c757d; color: white; padding: 10px 15px;" onclick="closeModal()">Cancel</button>
            </div>
        </div>
    </div>

    <script>
        function openModal() {
            document.getElementById('shutdownModal').style.display = 'flex';
        }
        function closeModal() {
            document.getElementById('shutdownModal').style.display = 'none';
        }
        
        // Close modal if user clicks outside of the modal box
        window.onclick = function(event) {
            var modal = document.getElementById('shutdownModal');
            if (event.target == modal) {
                closeModal();
            }
        }
    </script>
</body>
</html>
"""


@app.route("/")
def index():
  return render_template_string(HTML_PAGE)


@app.route("/control/<action>", methods=["POST"])
def control(action):
  cmd = []
  if action == "previous":
    cmd = ["mpc", "previous"]
  elif action == "next":
    cmd = ["mpc", "next"]
  elif action == "toggle":
    cmd = ["mpc", "toggle"]
  elif action == "vol_up":
    cmd = ["mpc", "volume", "+10"]
  elif action == "vol_down":
    cmd = ["mpc", "volume", "-10"]
  elif action == "shutdown":
    cmd = ["sudo", "shutdown", "-h", "now"]
  elif action == "reboot":
    cmd = ["sudo", "reboot", "now"]

  if cmd:
    try:
      subprocess.run(cmd, check=True)
    except Exception as e:
      print(f"Error executing command {action}: {e}")

  return redirect(url_for("index"))


def initialize_mpd():
  """Loads the playlist and starts playback on startup"""
  try:
    print("Loading playlist: radio.m3u")
    subprocess.run(["mpc", "load", "radio.m3u"], check=True)
    subprocess.run(["mpc", "play"], check=True)
  except Exception as e:
    print(f"Note: Could not automatically load playlist on startup: {e}")


if __name__ == "__main__":
  # Load the playlist when the script starts
  initialize_mpd()

  # Start Flask wrapped in Tornado WSGI container
  http_server = HTTPServer(WSGIContainer(app))
  http_server.listen(5000)
  print("Tornado server started. Access via http://<dietpi-ip>:5000")
  IOLoop.instance().start()
