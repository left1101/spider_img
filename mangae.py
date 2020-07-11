from flask_script import Manager, Server
from flask import Flask
from app import app

manager = Manager(app)

# @manager.command
# def hello():
#     print("hello")

manager.add_command("runserver", Server(use_debugger=True))

if __name__ == "__main__":
    manager.run()