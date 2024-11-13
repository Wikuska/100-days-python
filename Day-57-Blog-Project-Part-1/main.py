from flask import Flask, render_template
from post import Post
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Get a JSON response from the API containing all article elements
posts = requests.get(url = os.getenv("POSTS_API")).json()

# Create Post objects for each article from the API response and store them in a list
post_objects = []
for post in posts:
    post_obj = Post(
        post_id = post["id"],
        title = post["title"],
        subtitle = post["subtitle"],
        body = post["body"]
    )
    post_objects.append(post_obj)

@app.route('/')
def home():
    """Home route rendering an index.html template and passing all Post objects there."""
    return render_template("index.html", posts = post_objects)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    """Post route rendering a post.html template and passing Post object with id same as post_id in URL"""
    # Find the Post object that id matches the provided post_id
    post_to_show = None
    for blog_post in post_objects:
        if blog_post.id == post_id:
            post_to_show = blog_post
    # Render the post page with selected Post object
    return render_template("post.html", post_object = post_to_show)



if __name__ == "__main__":
    app.run(debug=True)
