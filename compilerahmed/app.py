from flask import Flask, render_template, request

app = Flask(__name__)

keywords = {"if", "else", "while", "return"}
operators = {'+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>='}
special_chars = {';', '(', ')', '{', '}'}


def lexical_analyzer(code):
    tokens = []
    current = ''
    pos = 0

    for char in code:
        pos += 1
        if char.isspace():
            continue
        elif char in operators:
            tokens.append((char, "Operator", pos))
        elif char in special_chars:
            tokens.append((char, "Special Character", pos))
        elif char.isalpha():
            tokens.append((char, "Keyword" if char in keywords else "Identifier", pos))
        else:
            tokens.append((char, "Unknown", pos))
    return tokens


@app.route("/", methods=["GET", "POST"])
def index():
    result = []
    code = ''
    if request.method == "POST":
        code = request.form["code"]
        result = lexical_analyzer(code)
    return render_template("index.html", tokens=result, code=code)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
