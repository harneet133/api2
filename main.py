from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/video-info', methods=['GET'])
def get_video_info():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'Missing video URL parameter.'}), 400

    # Make a GET request to the YouTube video page and parse the HTML with Beautiful Soup.
    response = requests.get(video_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the video title, description, upload date, view count, and thumbnail URL.
    title = soup.find('meta', property='og:title')['content']
    description = soup.find('meta', property='og:description')['content']
    upload_date = soup.find('meta', itemprop='uploadDate')['content']
    view_count = soup.find('meta', itemprop='interactionCount')['content']
    thumbnail_url = soup.find('link', itemprop='thumbnailUrl')['href']
    videoinfo = [title, description, upload_date, view_count, thumbnail_url]
    # Return the video information as a JSON response.
    return render_template("index.html", rates=videoinfo)


if __name__ == '__main__':
    app.run()
