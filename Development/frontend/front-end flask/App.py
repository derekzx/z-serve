from flask import Flask
from app import app


if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port=int("8000"))
