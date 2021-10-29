from flask import Flask, abort, request, redirect
import os

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 512

GHAT_IMAGE = "data:image/jpeg;base64,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uoNNROqrS9zA2P8AJDG08LYg5oAL2SOdsclzX9/dWRgva73Q74dvULWU4Q8UdQ8GeJFj4jaXl/z2x10NV4BOI6pjJGvdA/8A5D+gNdjfBWcG88+fDS0co0PMtBVUtXNJRQUbbLGZW4vr6cPdbi8syA1/VmXHT0sJBQXn4zceOFfAXTD9ZcT9TRWqia14hzE+SWd7O7I42AlzskbbDcb+mI7m29qRxH40/TdG8KWVGjdHVTH0lWOqGarucOSA5zzF1QAgghrHdQ8yV5W438b9f8wOv67iNxJura+61LfBi6I2xx09OHOc2CNrQAGN6iATknOSSrdnug+qsrpq+slrKqplllneXyySOLnyEnJJJ3JK+ZxGTg7dh8lBEAoiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAgxkZ7IiDl8QBgGc4OenHb45XcaS1tqXQ14Zf9K3irtlwiLXMnp5MO6mvDxkHIcOprTg7bLokQZVeU/wBrcx7KHRnM7HMZpCGDV9PEzB7BoqKWGMYGckyMzjzBWTbSuqtP6usNJqLTd2huNtrGGWCqhJcyRoOCRnBG/kQCtXmJ4a4OG3SO69N8kfOlrLlW1lBQPm+m6EvFdH+W7U/A6OotY6rieGucJI2tB6Rs4DBG+UGf978xiVhGPtDO2fh8FhE9qXzTDjFxen4W6XqphpnQlTLQ1MMjRiW8wSzxTzNd0h3SGlsY3LT0lw7r3B7QXnS07wq4GU1Fw4vlJcdQ8R7cx9vAY9r4bRV00v8A6RYXNwCD4bWxuw7LwcYBWESuqpq2Z1VPK6V7yXOe7uSSSc/eSUHDI5jhhoO22SpERAREQEREBERAREQEREEW7uGTjyz6L7Pp9c23PtQq5RRSSNqHQCU+G6UNID+nt1Yc4Z74JXxJk4xk4QEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQFOwEjBO3ftnspEBI7EoPqr6+tr3RurauecwxMhj8WQv6I2DpawZOzQBgDsAvlQknuUQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQf/Z"

@app.route("/", methods=["GET"])
def root():
    request.environ['wsgi.input_terminated'] = True
    return "<body bgcolor=\"black\"><img width=\"200px\" style=\"display: block;margin-left: auto;margin-right: auto;\" src=\""+GHAT_IMAGE+"\" /><h1 style=\"color:white;text-align:center\">We are the golden hat club!</h1><h2 style=\"color:white;text-align:center\">Only people authorized on our VPN can access the secret! It is stored on /golden.secret</h2></body>", 200

@app.route("/golden.secret", methods=["GET"])
def secret():
    request.environ['wsgi.input_terminated'] = True
    return "<body bgcolor=\"black\"><img width=\"200px\" style=\"display: block;margin-left: auto;margin-right: auto;\" src=\""+GHAT_IMAGE+"\" /><h1 style=\"color:white;text-align:center\">You made it to the club!</h1><h2 style=\"color:white;text-align:center\">Here is the password to enter: chicken nugget</h2></body>", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
