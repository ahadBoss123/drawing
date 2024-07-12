from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/draw', methods=['POST'])
def draw():
    data = request.json
    shapes = data.get('shapes', [])

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    for shape in shapes:
        view = shape['view']
        coords = shape['coords']
        x, y = zip(*coords)

        if view == 'front':
            ax = axs[0]
            ax.set_title("Front View")
        elif view == 'top':
            ax = axs[1]
            ax.set_title("Partial Top View")
        elif view == 'aux':
            ax = axs[2]
            ax.set_title("Auxiliary View")

        ax.plot(x, y, marker='o')
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 5)
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True)

    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return jsonify({'image': img_base64})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
