import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

posts = {
    0: {
        "id": 0,
        "upvotes": 1,
        "title": "My cat is the cutest!",
        "link": "https://i.imgur.com/jseZqNK.jpg",
        "username": "alicia98",
        "comments": {
            0: {
                "id": 0,
                "upvotes": 8,
                "text": "Wow, my first Reddit gold!",
                "username": "alicia98",
            }

        }

    },
    1: {
        "id": 1,
        "upvotes": 3,
        "title": "Cat loaf",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "alicia98",
        "comments": {
            1: {
                "id": 1,
                "upvotes": 8,
                "text": "Wow, my second Reddit gold!",
                "username": "alicia98",
            }

        }
    }

}

post_id_counter = 2
comment_id_counter = 2


@app.route("/")
def hello_world():
    return "Hello, World!"

# your routes here

# Get all posts


@app.route("/api/posts/")
def get_all_posts():
    res = {
        "posts": list(posts.values())
    }
    return json.dumps(res), 200

# Create a post


@app.route("/api/posts/", methods=['POST'])
def create_post():
    global post_id_counter
    body = json.loads(request.data)
    title = body.get("title", "No Title")
    link = body.get("link", "No Link")
    username = body.get("username", "No Username")

    res = {
        "id": post_id_counter,
        "upvotes": 1,
        "title": title,
        "link": link,
        "username": username
    }
    posts[post_id_counter] = res
    post_id_counter += 1

    return json.dumps(res), 201

# Get a specific post


@app.route("/api/posts/<int:post_id>/")
def get_specific_post(post_id):
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found"}), 404
    return json.dumps(post), 200

# Delete specific post


@app.route("/api/posts/<int:post_id>/", methods=['DELETE'])
def delete_post(post_id):
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Task not found"}), 404
    del posts[post_id]
    return json.dumps(post), 200

# Get comments for a post


@app.route("/api/posts/<int:post_id>/comments/")
def get_post_comments(post_id):
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found"}), 404
    res = {
        "comments": list(post["comments"].values())
    }
    return json.dumps(res), 200

# Post a comment for a post


@ app.route("/api/posts/<int:post_id>/comments/", methods=['POST'])
def post_a_comment(post_id):
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found"}), 404
    if not "comments" in post:
        posts[post_id]["comments"] = {}
    global comment_id_counter
    body = json.loads(request.data)
    text = body.get("text")
    username = body.get("username")

    res = {
        "id": comment_id_counter,
        "upvotes": 1,
        "text": text,
        "username": username
    }

    posts[post_id]["comments"][comment_id_counter] = res
    comment_id_counter += 1

    return json.dumps(res), 201

# edit a comment for a post


@ app.route("/api/posts/<int:post_id>/comments/<int:comment_id>/", methods=['POST'])
def edit_comment(post_id, comment_id):
    post = posts.get(post_id)
    comments = post.get("comments")
    if not post:
        return json.dumps({"error": "Post not found"}), 404
    if not comments:
        return json.dumps({"err": "Comment section not found"}), 404
    if not comment_id in comments:
        return json.dumps({"err": "Comment not found"}), 404
    '''
    for x in comments:
        if x["id"] == comment_id:
            comment = x
            break
        else:
            return json.dumps({"err": "Comment not found"}), 404
    '''

    body = json.loads(request.data)

    text = body.get("text")

    comments[comment_id]["text"] = text
    '''
    upvotes = comment["upvotes"]
    username = comment["username"]

    res = {
        "id": comment_id,
        "upvotes": upvotes,
        "text": text,
        "username": username,
    }
    '''

    return json.dumps(comments[comment_id]), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
