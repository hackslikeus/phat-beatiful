import subprocess
from flask import Flask, jsonify, redirect, render_template_string, request, url_for
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

app = Flask(__name__)

# Name of the stored playlist currently loaded in the MPD queue by this app
loaded_playlist = None

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<title>PhatBeast</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/x-icon" href="/images/favicon.ico">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/6/w3.css">
<link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-black.css">
<link href='https://fonts.googleapis.com/css?family=Bungee Shade' rel='stylesheet'>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.3.0/css/font-awesome.min.css">
</head>
<body>

<!-- Slide-in Sidebar Navigation (Hidden in Hamburger by default) -->
<nav class="w3-sidebar w3-bar-block w3-card w3-top w3-xlarge w3-animate-left w3-theme-d2" style="display:none;z-index:4;width:280px;max-width:80%;" id="mySidebar">
  <button onclick="w3_close()" class="w3-bar-item w3-button w3-large w3-theme-l1 w3-right-align">Close &times;</button>
  
  <div class="w3-container w3-padding-12">
    <h4><i class="fa fa-power-off"></i> System Power</h4>
    <p class="w3-small">Select an action for audio playing Pi:</p>
    
    <!-- Shutdown Option -->
    <form action="/control/shutdown" method="post" class="w3-margin-bottom">
      <button type="submit" class="w3-button w3-block w3-red w3-round w3-padding-large">
        <i class="fa fa-power-off"></i> Shutdown
      </button>
    </form>
    
    <!-- Reboot Option -->
    <form action="/control/reboot" method="post" class="w3-margin-bottom">
      <button type="submit" class="w3-button w3-block w3-amber w3-round w3-padding-large">
        <i class="fa fa-refresh"></i> Reboot
      </button>
    </form>
    
    <!-- Cancel Option -->
    <button type="button" onclick="w3_close()" class="w3-button w3-block w3-grey w3-round w3-padding-large">
      Cancel
    </button>
  </div>
</nav>

<!-- Dark Background Overlay when Sidebar is Open -->
<div class="w3-overlay w3-animate-opacity" onclick="w3_close()" style="cursor:pointer" id="myOverlay"></div>

<!-- Header -->
<header class="w3-container w3-theme w3-padding" id="myHeader">
  <i onclick="w3_open()" class="fa fa-bars w3-xlarge w3-button w3-theme"></i> 
  <div class="w3-center">
    <h2><font face="Bungee Shade">PHATBEAsT></font</h2>
    <h6 class="w3-large w3-animate-bottom">A PHATBEAST PLAYLIST PLAYER</h6>
      <div class="w3-padding-32">
      <div class="w3-row w3-border">
        <div class="w3-half w3-container-fluid w3-light-gray">
          <!-- Playlist and Item Pickers -->
          <div class="picker-area">
            <div class="picker-box">
              <label for="playlistBox">Playlists</label>
              <select id="playlistBox" size="8">
                {% for pl in playlists %}
                <option value="{{ pl }}">{{ pl }}</option>
                {% endfor %}
              </select>
            </div>
            </div>
          </div>
               <!--Item Pickers -->
            <div class="w3-half w3-container-fluid w3-dark-gray">
       <div class="picker-box">
            <label for="itemBox">Playlist Items</label>
            <select id="itemBox" size="8"></select>
             </div>
      </div>
        </div>
        
      </div>
            
      <br>
      <button class="w3-btn w3-large w3-light-grey w3-hover-dark-grey" onclick="loadSelection()">📂 Clear &amp; Load Playlist</button>
      <button class="w3-btn w3-large w3-dark-grey w3-hover-light-grey" onclick="playSelection()" style="font-weight:900;">▶ PLAY SELECTION</button>
    </div>
  </header>

<div class="w3-grid w3-center w3-margin-top w3-padding" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px">
  <div>
    <div class="w3-card w3-container" style="min-height:250px">
      <h4>Player Controls</h4><br>
      <i class="fa fa-desktop w3-margin-bottom w3-text-theme" style="font-size:120px"></i><br>
      <a class="w3-button w3-theme w3-hover-light-grey" onclick="control('prev')">⏪PREV</a>
      <a class="w3-button w3-theme w3-hover-light-grey"" onclick="control('toggle')">PLAY>⏯PAUSE</a>
      <a class="w3-button w3-theme w3-hover-light-gray"" onclick="control('next')">⏩NEXT</a>
    </div>
  </div>

  <div>
    <div class="w3-card w3-container" style="min-height:250px">
      <h4>Volume Controls</h4><br>
      <i class="fa fa-volume-up w3-margin-bottom w3-text-theme" style="font-size:120px"></i><br>
      <a class="w3-button w3-theme w3-hover-dark-gray"" onclick="control('vol_down')">🔉 Volume -10</a>
      <a class="w3-button w3-theme w3-hover-light-gray"" onclick="control('vol_up')">🔊 Volume +10</a>
    </div>
  </div>
</div>

<!-- Footer (Power Modal Removed) -->
<hr>
<footer class="w3-container w3-theme-dark w3-padding-12">
    <div class="w3-center">
    <div id="status"></div>
    <!-- Live MPD status (refreshed every 15 seconds) -->
    <div id="mpdStatus">Checking MPD status...</div>
   </div>

  <p>Powered by <a href="https://www.w3schools.com/w3css/default.asp" target="_blank">w3.css</a></p>
  <div style="position:relative;bottom:55px;" class="w3-tooltip w3-right">
    <span class="w3-text w3-theme-light w3-padding">Go To Top</span>   
    <a class="w3-text-white" href="#myHeader"><span class="w3-xlarge">
    <i class="fa fa-chevron-circle-up"></i></span></a>
  </div>
</footer>

<script>
    // Sidebar Open/Close Functions for Hamburger Menu
    function w3_open() {
        document.getElementById("mySidebar").style.display = "block";
        document.getElementById("myOverlay").style.display = "block";
    }

    function w3_close() {
        document.getElementById("mySidebar").style.display = "none";
        document.getElementById("myOverlay").style.display = "none";
    }

    var playlistBox = document.getElementById('playlistBox');
    var itemBox = document.getElementById('itemBox');
    var statusLine = document.getElementById('status');

    function setStatus(msg) { statusLine.textContent = msg; }

    function post(url, body) {
        return fetch(url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json', 'X-Requested-With': 'fetch'},
            body: JSON.stringify(body || {})
        }).then(function(r) { return r.json(); });
    }

    function control(action) {
        post('/control/' + action).then(function(d) {
            setStatus(d.ok ? '' : d.message);
            refreshStatusSoon();
        }).catch(function() { setStatus('Could not reach the server.'); });
    }

    playlistBox.addEventListener('change', function() {
        var name = playlistBox.value;
        itemBox.innerHTML = '';
        setStatus('Loading items...');
        fetch('/api/playlist_items?name=' + encodeURIComponent(name))
            .then(function(r) { return r.json(); })
            .then(function(d) {
                if (!d.ok) { setStatus(d.message); return; }
                d.items.forEach(function(text, i) {
                    var opt = document.createElement('option');
                    opt.value = i + 1;
                    opt.textContent = text;
                    itemBox.appendChild(opt);
                });
                if (itemBox.options.length > 0) { itemBox.selectedIndex = 0; }
                setStatus(d.items.length + ' item(s) in "' + name + '"');
            })
            .catch(function() { setStatus('Could not read playlist items.'); });
    });

    function loadSelection() {
        if (!playlistBox.value) { setStatus('Select a playlist first.'); return; }
        post('/control/load', {playlist: playlistBox.value}).then(function(d) {
            setStatus(d.message);
            refreshStatusSoon();
        }).catch(function() { setStatus('Could not reach the server.'); });
    }

    function playSelection() {
        if (!playlistBox.value) { setStatus('Select a playlist first.'); return; }
        if (!itemBox.value) { setStatus('Select a playlist item first.'); return; }
        post('/control/play', {playlist: playlistBox.value, position: itemBox.value}).then(function(d) {
            setStatus(d.message);
            refreshStatusSoon();
        }).catch(function() { setStatus('Could not reach the server.'); });
    }

    var mpdStatusBox = document.getElementById('mpdStatus');
    var statusTimer = null;
    function refreshStatus() {
        clearTimeout(statusTimer);
        fetch('/api/status')
            .then(function(r) { return r.json(); })
            .then(function(d) { mpdStatusBox.textContent = d.status; })
            .catch(function() { mpdStatusBox.textContent = 'Could not reach the server.'; })
            .finally(function() { statusTimer = setTimeout(refreshStatus, 15000); });
    }

    function refreshStatusSoon() {
        clearTimeout(statusTimer);
        statusTimer = setTimeout(refreshStatus, 700);
    }

    // Start status loop on page load
    refreshStatus();
</script>
</body>
</html>
"""
# Simple one-shot commands (existing buttons)
SIMPLE_COMMANDS = {
  "prev": ["mpc", "prev"],
  "next": ["mpc", "next"],
  "toggle": ["mpc", "toggle"],
  "vol_up": ["mpc", "volume", "+10"],
  "vol_down": ["mpc", "volume", "-10"],
  "shutdown": ["sudo", "shutdown", "-h", "now"],
  "reboot": ["sudo", "reboot", "now"],
}


def run_mpc(args):
  """Run an mpc command and return its stdout as text."""
  result = subprocess.run(["mpc"] + args, check=True, capture_output=True, text=True)
  return result.stdout


def get_playlists():
  """Returns the list of stored playlists from 'mpc lsplaylists'."""
  try:
    out = run_mpc(["lsplaylists"])
  except Exception as e:
    print(f"Error listing playlists: {e}")
    return []
  return [line.rstrip("\r") for line in out.splitlines() if line.strip()]


def clear_and_load(name):
  """Clears the current MPD queue and loads the named stored playlist."""
  global loaded_playlist
  if name not in get_playlists():
    raise ValueError(f"Unknown playlist: {name}")
  run_mpc(["clear"])
  run_mpc(["load", name])
  loaded_playlist = name


@app.route("/")
def index():
  return render_template_string(HTML_PAGE, playlists=get_playlists())


@app.route("/api/playlist_items")
def playlist_items():
  name = request.args.get("name", "")
  try:
    if name not in get_playlists():
      return jsonify(ok=False, message="Unknown playlist.", items=[])
    out = run_mpc(["playlist", name])
    items = [line.rstrip("\r") for line in out.splitlines() if line.strip()]
    return jsonify(ok=True, items=items)
  except Exception as e:
    print(f"Error reading playlist {name}: {e}")
    return jsonify(ok=False, message="Could not read playlist items.", items=[])


@app.route("/api/status")
def mpd_status():
  """Returns the output of 'mpc status', or a null-status message if not playing."""
  null_status = "mpc not playing - null status"
  try:
    out = run_mpc(["status"]).strip()
  except Exception as e:
    print(f"Error reading mpc status: {e}")
    return jsonify(status=null_status)
  # When stopped, mpc prints only the volume/options line (no [playing] line)
  if "[playing]" in out or "[paused]" in out:
    return jsonify(status=out)
  return jsonify(status=null_status)


@app.route("/control/<action>", methods=["POST"])
def control(action):
  global loaded_playlist
  wants_json = request.headers.get("X-Requested-With") == "fetch"
  data = request.get_json(silent=True) or {}
  ok = True
  message = ""

  try:
    if action in SIMPLE_COMMANDS:
      subprocess.run(SIMPLE_COMMANDS[action], check=True)

    elif action == "load":
      name = data.get("playlist", "")
      clear_and_load(name)
      message = f'Loaded playlist "{name}".'

    elif action == "play":
      name = data.get("playlist", "")
      position = int(data.get("position", 1))
      if position < 1:
        raise ValueError("Invalid position")
      # Make sure the queue holds the chosen playlist before playing an item
      if name != loaded_playlist:
        clear_and_load(name)
      run_mpc(["play", str(position)])
      message = f'Playing item {position} of "{name}".'

    else:
      ok = False
      message = f"Unknown action: {action}"
  except Exception as e:
    print(f"Error executing command {action}: {e}")
    ok = False
    message = f"Error executing {action}."

  if wants_json:
    return jsonify(ok=ok, message=message)
  return redirect(url_for("index"))


# --- Power Control Routes for shutdown---
@app.route('/control/shutdown', methods=['POST'])
def shutdown_pi():
    subprocess.Popen(['sudo', 'shutdown', '-h', 'now'])
    return "Shutting down Raspberry Pi..."

@app.route('/control/reboot', methods=['POST'])
def reboot_pi():
    subprocess.Popen(['sudo', 'reboot', 'now'])
    return "Rebooting Raspberry Pi..."

if __name__ == "__main__":
  # Start Flask wrapped in Tornado WSGI container use port 5000 for testing 8080 otherwise
  http_server = HTTPServer(WSGIContainer(app))
  http_server.listen(5000)
  print("Tornado server started. Access via http://<dietpi-ip>:5000")
  IOLoop.instance().start()
