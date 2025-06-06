import random
import string
import json
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
shortner_urls = {}

def get_shortened_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = get_shortened_url()
        while short_url in shortner_urls:
            short_url = get_shortened_url()

        shortner_urls[short_url] = long_url
        with open("urls.json", "w") as f:
            json.dump(shortner_urls, f)
        return f"Shortened URL:{request.url_root}{short_url}"
    return render_template("index.html")

@app.route("/<short_url>")

def redirect_url(short_url):    
    long_url = shortner_urls.get(short_url)
    if long_url: 
        return redirect(long_url)
    else:
        return "URL not found", 404



if __name__ == "__main__":
    app.run(debug=True)
