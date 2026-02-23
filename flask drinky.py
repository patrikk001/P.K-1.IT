from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    response = requests.get("https://boozeapi.com/api/v1/cocktails")

    if response.status_code == 200:
        raw = response.json()
        cocktails = raw["data"]

        resp = """
        <html>
        <head>
            <title>Svet Drinkov</title>
            <style>
                body {
                    margin: 0;
                    padding: 40px;
                    font-family: 'Segoe UI', sans-serif;
                    background: linear-gradient(-45deg, #0f9b0f, #00c6ff, #f9d423, #1e3c72);
                    background-size: 400% 400%;
                    animation: gradientMove 12s ease infinite;
                    color: white;
                }

                @keyframes gradientMove {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }

                h1 {
                    text-align: center;
                    font-size: 65px;
                    margin-bottom: 10px;
                    font-weight: 900;
                    letter-spacing: 4px;
                    background: linear-gradient(90deg, gold, yellow, white);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    text-shadow: 0 0 30px rgba(255,215,0,0.8);
                    animation: glowPulse 2s infinite alternate;
                }

                @keyframes glowPulse {
                    from { text-shadow: 0 0 15px gold; }
                    to { text-shadow: 0 0 40px yellow, 0 0 60px white; }
                }

                .subtitle {
                    text-align: center;
                    margin-bottom: 50px;
                    font-size: 18px;
                    letter-spacing: 3px;
                    opacity: 0.9;
                }

                .container {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 30px;
                }

                .card {
                    background: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(15px);
                    border-radius: 25px;
                    overflow: hidden;
                    transition: all 0.4s ease;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                }

                .card:hover {
                    transform: translateY(-12px) scale(1.05);
                    box-shadow: 0 0 40px rgba(255,255,0,0.9);
                }

                .card img {
                    width: 100%;
                    height: 260px;
                    object-fit: cover;
                }

                .card h3 {
                    text-align: center;
                    padding: 20px;
                    font-size: 20px;
                    color: yellow;
                    letter-spacing: 1px;
                }

                footer {
                    text-align: center;
                    margin-top: 60px;
                    opacity: 0.8;
                    font-size: 14px;
                }

            </style>
        </head>
        <body>

            <h1>🍹 Svet Drinkov</h1>
            <div class="subtitle">Objav svet luxusných koktejlov ✨</div>

            <div class="container">
        """

        for drink in cocktails:
            name = drink.get("name", "Unknown drink")
            image = drink.get("image")

            if image:
                resp += f"""
                <div class="card">
                    <img src="{image}">
                    <h3>{name}</h3>
                </div>
                """

        resp += """
            </div>

            <footer>
                Svet Drinkov 🍸 | Flask Edition
            </footer>

        </body>
        </html>
        """

        return resp

    return "Error loading cocktails"

if __name__ == "__main__":
    app.run(debug=True)