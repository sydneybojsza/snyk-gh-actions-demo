
import subprocess
import re

import sqlite3

"""
This file contains snippets of insecure code which are never intended to be executed.
These are here strictly for SAST code security testing using Snyk.
"""

def path_traversal_example(message: str) -> None:
    """ 
    This insecure as we are allowing users to open any path specified in the string below
    without sanitising it first. This could lead to an attacker accessing something like /etc/passwd
    """
    user_input = input(f"{message} ")
    if re.match("^[a-zA-Z0-9_\-/]+\.txt$", user_input):
        with open(user_input, "r") as file:
            content = file.read()
    else:
        print("Invalid file format")


def command_injection_example(message: str) -> None:
    """
    Here we are not sanitising input either, meaning we are allowing a potential attacker
    to execute arbitrary malicious commands.
    """
    directory = input(f"{message} ")
    command = "ls" 
    subprocess.run([command, directory])


def sql_injection_example() -> None:
    """
    Similar to the above example except instead of being open to commands on the host system,
    we are open to commands on the database.
    A potential attacker could maliciously remove entries or gain access they should not 
    normally have.
    """
    with sqlite3.connect("demo.db") as conn:
        cursor = conn.cursor()
        user_input = input("Enter your username: ")
        query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query, (user_input,))