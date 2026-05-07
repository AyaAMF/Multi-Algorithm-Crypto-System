from flask import Flask, render_template, request, redirect, url_for
import webbrowser

app = Flask(__name__)

# ================= LOGIN =================

USERNAME = "admin"
PASSWORD = "1234"

# ================= Caesar Cipher =================

def caesar_encrypt(text, shift):

    result = ""

    for char in text:

        if char.isalpha():

            shift_base = 65 if char.isupper() else 97

            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)

        else:

            result += char

    return result


def caesar_decrypt(text, shift):

    return caesar_encrypt(text, -shift)


# ================= Atbash Cipher =================

def atbash_cipher(text):

    result = ""

    for char in text.upper():

        if char.isalpha():

            result += chr(90 - (ord(char) - 65))

        else:

            result += char

    return result


# ================= Monoalphabetic Cipher =================

def mono_encrypt(text, key):

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    key = key.upper()

    cipher = ""

    for char in key:

        if char not in cipher and char.isalpha():

            cipher += char

    for char in alphabet:

        if char not in cipher:

            cipher += char

    result = ""

    for char in text.upper():

        if char in alphabet:

            index = alphabet.index(char)

            result += cipher[index]

        else:

            result += char

    return result


def mono_decrypt(text, key):

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    key = key.upper()

    cipher = ""

    for char in key:

        if char not in cipher and char.isalpha():

            cipher += char

    for char in alphabet:

        if char not in cipher:

            cipher += char

    result = ""

    for char in text.upper():

        if char in cipher:

            index = cipher.index(char)

            result += alphabet[index]

        else:

            result += char

    return result


# ================= Row Column Cipher =================

def row_encrypt(text):

    text = text.replace(" ", "").upper()

    even = text[::2]

    odd = text[1::2]

    return even + odd


def row_decrypt(text):

    half = (len(text) + 1) // 2

    even = text[:half]

    odd = text[half:]

    result = ""

    for i in range(half):

        result += even[i]

        if i < len(odd):

            result += odd[i]

    return result


# ================= Playfair Cipher =================

def generate_playfair_matrix(key):

    key = key.upper().replace("J", "I")

    matrix = []

    used = []

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    for char in key:

        if char not in used and char.isalpha():

            used.append(char)

    for char in alphabet:

        if char not in used:

            used.append(char)

    for i in range(0, 25, 5):

        matrix.append(used[i:i+5])

    return matrix


def find_position(matrix, char):

    for row in range(5):

        for col in range(5):

            if matrix[row][col] == char:

                return row, col


def playfair_encrypt(text, key):

    matrix = generate_playfair_matrix(key)

    text = text.upper().replace("J", "I").replace(" ", "")

    pairs = []

    i = 0

    while i < len(text):

        a = text[i]

        if i + 1 < len(text):

            b = text[i + 1]

            if a == b:

                b = "X"

                i += 1

            else:

                i += 2

        else:

            b = "X"

            i += 1

        pairs.append((a, b))

    result = ""

    for a, b in pairs:

        row1, col1 = find_position(matrix, a)

        row2, col2 = find_position(matrix, b)

        if row1 == row2:

            result += matrix[row1][(col1 + 1) % 5]

            result += matrix[row2][(col2 + 1) % 5]

        elif col1 == col2:

            result += matrix[(row1 + 1) % 5][col1]

            result += matrix[(row2 + 1) % 5][col2]

        else:

            result += matrix[row1][col2]

            result += matrix[row2][col1]

    return result


def playfair_decrypt(text, key):

    matrix = generate_playfair_matrix(key)

    text = text.upper().replace(" ", "")

    result = ""

    for i in range(0, len(text), 2):

        a = text[i]

        b = text[i + 1]

        row1, col1 = find_position(matrix, a)

        row2, col2 = find_position(matrix, b)

        if row1 == row2:

            result += matrix[row1][(col1 - 1) % 5]

            result += matrix[row2][(col2 - 1) % 5]

        elif col1 == col2:

            result += matrix[(row1 - 1) % 5][col1]

            result += matrix[(row2 - 1) % 5][col2]

        else:

            result += matrix[row1][col2]

            result += matrix[row2][col1]

    return result


# ================= LOGIN ROUTE =================

@app.route("/", methods=["GET", "POST"])

def login():

    error = ""

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:

            return redirect(url_for("home"))

        else:

            error = "Invalid Username or Password"

    return render_template("login.html", error=error)


# ================= HOME ROUTE =================

@app.route("/home", methods=["GET", "POST"])

def home():

    result = ""

    if request.method == "POST":

        text = request.form["text"]

        algorithm = request.form["algorithm"]

        key = request.form["key"]

        action = request.form["action"]

        # ================= Caesar =================

        if algorithm == "caesar":

            if key == "":

                result = "Enter Shift Number"

            elif not key.isdigit():

                result = "Shift Must Be Number"

            else:

                shift = int(key)

                if action == "encrypt":

                    result = caesar_encrypt(text, shift)

                else:

                    result = caesar_decrypt(text, shift)

        # ================= Atbash =================

        elif algorithm == "atbash":

            result = atbash_cipher(text)

        # ================= Mono =================

        elif algorithm == "mono":

            if key == "":

                result = "Enter Key"

            else:

                if action == "encrypt":

                    result = mono_encrypt(text, key)

                else:

                    result = mono_decrypt(text, key)

        # ================= Row Column =================

        elif algorithm == "row":

            if action == "encrypt":

                result = row_encrypt(text)

            else:

                result = row_decrypt(text)

        # ================= Playfair =================

        elif algorithm == "playfair":

            if key == "":

                result = "Enter Key"

            else:

                if action == "encrypt":

                    result = playfair_encrypt(text, key)

                else:

                    result = playfair_decrypt(text, key)

    return render_template("index.html", result=result)


if __name__ == "__main__":

    webbrowser.open("http://127.0.0.1:5000")

    app.run(debug=True)