from flask import Flask, request, jsonify

app = Flask(__name__)


def rv(s: str) -> str:
    r = ""
    for ch in s:
        if ch == ')':
            r = '(' + r
        elif ch == '(':
            r = ')' + r
        else:
            r = ch + r
    return r

def give_precedence(a: str) -> int:
    if a == '^':
        return 4
    elif a == '/':
        return 3
    elif a == '*':
        return 2
    else:
        return 1

def check_precedence(top: str, a: str) -> bool:
    x = give_precedence(top)
    y = give_precedence(a)
    return y > x or (top == '^' and a == '^')

def is_push(stack, a: str) -> bool:
    return (not stack) or stack[-1] == '(' or a == '(' or check_precedence(stack[-1], a)

# -----------------------
#   INFIX → POSTFIX
# -----------------------
def infix_to_postfix(expr: str) -> str:
    s = expr
    o = ""
    stack = []

    for ch in s:
        if ch.isalpha():
            o += ch
        else:
            if ch == ')':
                while stack[-1] != '(':
                    o += stack.pop()
                stack.pop()
            else:
                while not is_push(stack, ch):
                    o += stack.pop()
                stack.append(ch)

    while stack:
        o += stack.pop()

    return "Postfix(" + o + ")"

# -----------------------
#   INFIX → PREFIX
# -----------------------
def infix_to_prefix(expr: str) -> str:
    s = rv(expr)
    o = ""
    stack = []

    for ch in s:
        if ch.isalpha():
            o += ch
        else:
            if ch == ')':
                while stack[-1] != '(':
                    o += stack.pop()
                stack.pop()
            else:
                while not is_push(stack, ch):
                    o += stack.pop()
                stack.append(ch)

    while stack:
        o += stack.pop()

    o = o[::-1]
    return "Prefix(" + o + ")"

# -----------------------
#   PREFIX → INFIX
# -----------------------
def prefix_to_infix(expr: str) -> str:
    s = expr[::-1]
    stack = []

    for ch in s:
        if ch.isalpha():
            stack.append(ch)
        else:
            va = stack.pop()
            vb = stack.pop()
            b = f"({vb}{ch}{va})"
            stack.append(b)

    s1 = stack[-1]
    s1 = rv(s1)
    return "InfixFromPrefix(" + s1 + ")"

# -----------------------
#   POSTFIX → INFIX
# -----------------------
def postfix_to_infix(expr: str) -> str:
    stack = []

    for ch in expr:
        if ch.isalpha():
            stack.append(ch)
        else:
            va = stack.pop()
            vb = stack.pop()
            b = f"({vb}{ch}{va})"
            stack.append(b)

    return "InfixFromPostfix(" + stack[-1] + ")"

# -----------------------
# API ROUTE
# -----------------------

@app.route("/convert", methods=["GET", "POST"])
def convert():

    # Handle GET request
    if request.method == "GET":
        expr = request.args.get("expression")
        op = request.args.get("operation")

        if not expr or not op:
            return jsonify({"error": "Missing parameters"}), 400

    # Handle POST request
    else:
        data = request.get_json(silent=True)

        if not data or "expression" not in data or "operation" not in data:
            return jsonify({"error": "Missing parameters"}), 400

        expr = data["expression"]
        op = data["operation"]

    # Perform conversion
    if op == "infix_postfix":
        result = infix_to_postfix(expr)
    elif op == "infix_prefix":
        result = infix_to_prefix(expr)
    elif op == "prefix_infix":
        result = prefix_to_infix(expr)
    elif op == "postfix_infix":
        result = postfix_to_infix(expr)
    else:
        return jsonify({"error": "Unknown operation"}), 400

    return jsonify({"result": result})


@app.route("/", methods=["GET"])
def home():
    return "Backend Running Successfully"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
