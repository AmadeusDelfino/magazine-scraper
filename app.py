from flask import Flask
from src.magazine.scraper import exec_scraper
from src.magazine.controller import magazine_app

app = Flask(__name__)
app.register_blueprint(magazine_app)


@app.route('/')
def execute_scraper():
    return exec_scraper()


if __name__ == '__main__':
    app.run()
