# phat-beatiful
Don't let the name fool you - a last ditch, bare bones effort using python code to make use of a Pimoroni Phatbeat,<br> ignoring the led's completely and hijacking the buttons to 
navigate an existing playlist consisting of 6 internet radio stations before everything ends in the trash.\
#Pre-requisites:# <br> Install Dietpi OS or Raspbian lite OS, MPD, MPC with a working .conf, GPIO libraries, Python and Utilities, Alsa too. <br> If using the web interface, webserver such as nginx or lightppd is required. <br>
To use Flask web page, you need to install Flask with Pip in a virtual environment, along with Tornado, Sqlalchemy and gpizero.  Barebones web page is included in flask_web.py script. <br>
#You will not see an annoying LED ever again!#. <br>  The web page runs at port 5000 for testing and can be gussied up a bit to your choosing.
Barebuttons1a.py will handle all the physical buttons on the phat itself.<br>  For a web interface, flask_web.py will generate a web equivalent for the physical buttons, using port 5000 or 8080 after testing.<br>
Some PhatBeats have extra small buttons, so the web page option will assist.
