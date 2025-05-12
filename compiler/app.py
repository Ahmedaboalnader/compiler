from flask import Flask, render_template, request

app = Flask(__name__)

# أنواع الـ Tokens
keywords = ["if", "else", "while", "for", "return"]
operators = ["=", "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="]
special_chars = [";", "(", ")", "{", "}"]

def lexical_analyzer(code):
    tokens = []
    position = 1
    temp = ""
    for char in code:
        if char.isalpha():
            temp += char
        else:
            if temp:
                token_type = "Keyword" if temp in keywords else "Identifier"
                tokens.append((temp, token_type, position))
                position += len(temp)
                temp = ""
            if char in operators:
                tokens.append((char, "Operator", position))
                position += 1
            elif char in special_chars:
                tokens.append((char, "Special Character", position))
                position += 1
            elif char.isspace():
                position += 1
    if temp:
        token_type = "Keyword" if temp in keywords else "Identifier"
        tokens.append((temp, token_type, position))
    return tokens


def syntax_analyzer(code):
    state = "q0"
    for char in code:
        if state == "q0" and char.isalpha():
            state = "q1"
        elif state == "q1" and char == "=":
            state = "q3"
        elif state == "q3" and (char.isalpha() or char.isdigit()):
            state = "q3"
        elif char in "+-*/":
            state = "q3"
        elif char == ";":
            return "Yes"
        else:
            return "No"
    return "No"


def predictive_parser(code):
    output = []
    tokens = lexical_analyzer(code)
    for token in tokens:
        output.append(f"Matched {token[1]}: {token[0]}")
    output.append("Parsing completed successfully!" if syntax_analyzer(code) == "Yes" else "Parsing failed!")
    return output

@app.route("/", methods=["GET", "POST"])
def index():
    lexical_result = []
    syntax_result = ""
    predictive_result = []
    if request.method == "POST":
        code = request.form["code"]
        lexical_result = lexical_analyzer(code)
        syntax_result = syntax_analyzer(code)
        predictive_result = predictive_parser(code)
    return render_template("index.html", lexical_result=lexical_result,
                           syntax_result=syntax_result,
                           predictive_result=predictive_result)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)

