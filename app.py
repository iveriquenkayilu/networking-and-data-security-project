from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Sample data - you can replace this with your own data source
posts = [
    {"id": 1, "title": "First Post", "content": "This is the content of the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the content of the second post."},
    # Add more posts as needed
]


# Endpoint to get one post by ID
@app.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return jsonify(post), 200
    else:
        return jsonify({"error": "Post not found"}), 404


# Endpoint to create a new post
@app.route('/post', methods=['POST'])
def create_post():
    data = request.get_json()
    if 'title' in data and 'content' in data:
        new_post = {
            "id": len(posts) + 1,
            "title": data['title'],
            "content": data['content']
        }
        posts.append(new_post)
        return jsonify(new_post), 201
    else:
        return jsonify({"error": "Title and content are required"}), 400


# Endpoint to serve HTML page
@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
