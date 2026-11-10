import os
import subprocess
import sys
from gpiozero import Button
from signal import pause

# Map pHAT BEAT physical buttons to BCM Pins
btn_next = Button(5, pull_up=True)
btn_play = Button(6, pull_up=True)
btn_prev = Button(13, pull_up=True)
btn_vol_up = Button(16, pull_up=True)
btn_vol_down = Button(26, pull_up=True)
btn_power = Button(12, pull_up=True)

# Define what happens on a button press
def play_pause():
    print("Play/Pause Pressed -> Toggling")
    os.system("mpc toggle")

def volume_up():
    print("Volume Up Pressed")
    # Adjust ALSA Master volume directly: issue with D16!
    os.system("mpc volume +10")

def volume_down():
    print("Volume Down Pressed")
    os.system("mpc volume -10")

def next_station():
    print("Next Station Pressed")
    os.system("mpc next")

def prev_station():
    print("Previous Station Pressed")
    os.system("mpc prev")

def power_down():
    print ("Good Night Irene!")
    os.system("sudo shutdown -h now")


# Attach functions to events
btn_play.when_pressed = play_pause
btn_vol_up.when_pressed = volume_up
btn_vol_down.when_pressed = volume_down
btn_next.when_pressed = next_station
btn_prev.when_pressed = prev_station
btn_power.when_pressed = power_down

print("pHAT BEAT listening for button presses... Press Ctrl+C to exit.")
pause()

#Now let's load a sample radio station playlist: It will play Gorilla Radio automatically!

def run_mpc_command(command_list):
    """Helper function to execute mpc commands safely."""
    try:
        # Run the command and capture output
        result = subprocess.run(
            ['mpc'] + command_list, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running 'mpc {' '.join(command_list)}': {e.stderr.strip()}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("Error: The 'mpc' command-line tool is not installed or not in PATH.", file=sys.stderr)
        sys.exit(1)

def load_radio_playlist():
    playlist_path = "/mnt/dietpi_userdata/Music/radio.m3u"
    
    # 1. Quick sanity check to ensure the file exists on your DietPi system
    if not os.path.exists(playlist_path):
        print(f"Error: Playlist file not found at {playlist_path}", file=sys.stderr)
        sys.exit(1)

    print("Clearing current mpc queue...")
    run_mpc_command(['clear'])
    
    print(f"Attempting to load {playlist_path}...")
    # Method A: Try loading via standard native mpc load
    # (Works seamlessly if the path is mapped/accessible inside your mpd.conf playlists directory)
    response = run_mpc_command(['load', playlist_path])
    
    # Method B Fallback: If MPD strictly wants names relative to its internal playlist folder, 
    # we pipe the file content directly into 'mpc add' 
    if response is None:
        print("Standard load failed. Attempting to parse and inject playlist tracks directly...")
        try:
            with open(playlist_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and standard M3U metadata headers
                    if line and not line.startswith('#'):
                        run_mpc_command(['add', line])
            print("Direct injection complete.")
        except Exception as e:
            print(f"Failed to read file directly: {e}", file=sys.stderr)
            sys.exit(1)

    # 3. Start playback of the newly loaded radio playlist
    print("Starting playback...")
    run_mpc_command(['play'])
    
    # Print current status to confirm it's playing
    status = run_mpc_command(['status'])
    if status:
        print("\n--- Current MPC Status ---")
        print(status)

if __name__ == "__main__":
    load_radio_playlist()

    
    
    

