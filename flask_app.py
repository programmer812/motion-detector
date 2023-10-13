from flask import Flask

app = Flask(__name__, static_url_path="/home/anish/camera", static_folder="/home/anish/camera")

previous_line_count = 0

@app.route("/")
def index():
	return "<h1>Hello</h1>"
	
@app.route("/check-movement")
def check_movement():
	global previous_line_count
	try:
		with open("photo_logs.txt", "r") as f:
			files = f.readlines()
			filename_total = files[-1]
			filename = filename_total[0:len(filename_total) - 1]
			photo_update = f"{len(files) - previous_line_count} photo(s) were taken since you last checked."
			previous_line_count = len(files)
			return f"""
			{photo_update}
			<br />
			<br />
			Last Photo: {filename}
			<br />
			<img src={filename} />
			"""
	except:
		return "<h1>No Photos Taken</h1>"
		
app.run(host="0.0.0.0")
