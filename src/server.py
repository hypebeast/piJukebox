from bottle import route, run, debug, template, request, validate, error, static_file, get
from mpg123_controller import Mpg123Controller

# MPG123 controller object
mpg123Controller = Mpg123Controller()

####
# Web Page
####

@route('/')
def index():
	return template('index')

@route('/start')
def start():
	mpg123Controller.play('http://mp3stream1.apasf.apa.at:8000/listen.pls', isPlaylist=True)

@route('/stop')
def stop():
	mpg123Controller.stop()

@route('/about')
def about():
	return template('about')


####
# Mobile Web Page
####

@route('/mobile')
def index_mobile():
	return template('index_mobile')

####
# API
####

@route('/api/v1/start_playback')
def start_playback():
	pass

@route('/api/v1/stop_playback')
def stop_playback():
	pass

# Static
@route('/public/:path#.+#', name='static')
def static(path):
    return static_file(path, root='public')


run(host='0.0.0.0', port=8080, reloader=True)


def run_server(host, port):
	#run(host='0.0.0.0', port=8080, reloader=True)
	pass