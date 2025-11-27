from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def checkPrecedence(top, a):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    if top == '(' or a == '(':
        return False
    if top in precedence and a in precedence:
        return precedence[top] > precedence[a] or (top == '^' and a == '^')
    return False

def is_push(stack, a):
    if not stack or stack[-1] == '(' or a == '(' or checkPrecedence(stack[-1], a):
        return True
    return False

def reverse_string(s):
    return s[::-1]

def infixToPostfix(expr):
    stack = []
    result = []
    for i in range(len(expr)):
        ch = expr[i]
        if ch.isalnum():
            result.append(ch)
        elif ch == '(':
            stack.append(ch)
        elif ch == ')':
            while stack and stack[-1] != '(':
                result.append(stack.pop())
            if stack: stack.pop()
        elif ch in {'+', '-', '*', '/', '^'}:
            while stack and stack[-1] != '(' and checkPrecedence(stack[-1], ch):
                result.append(stack.pop())
            stack.append(ch)
    while stack:
        result.append(stack.pop())
    return ''.join(result)

def infixToPrefix(expr):
    stack = []
    result = []
    for i in range(len(expr)):
        ch = expr[i]
        if ch.isalnum():
            result.append(ch)
        elif ch == ')':
            stack.append(ch)
        elif ch == '(':
            while stack and stack[-1] != ')':
                result.append(stack.pop())
            if stack: stack.pop()
        elif ch in {'+', '-', '*', '/', '^'}:
            while stack and stack[-1] != ')' and checkPrecedence(ch, stack[-1]):
                result.append(stack.pop())
            stack.append(ch)
    while stack:
        result.append(stack.pop())
    return reverse_string(''.join(result))

def prefixToInfix(expr):
    stack = []
    for i in range(len(expr) - 1, -1, -1):
        ch = expr[i]
        if ch.isalnum():
            stack.append(ch)
        elif ch in {'+', '-', '*', '/', '^'}:
            if len(stack) >= 2:
                op1 = stack.pop()
                op2 = stack.pop()
                new_expr = f"({op1}{ch}{op2})"
                stack.append(new_expr)
    return stack[0] if stack else ""

def postfixToInfix(expr):
    stack = []
    for ch in expr:
        if ch.isalnum():
            stack.append(ch)
        elif ch in {'+', '-', '*', '/', '^'}:
            if len(stack) >= 2:
                op2 = stack.pop()
                op1 = stack.pop()
                new_expr = f"({op1}{ch}{op2})"
                stack.append(new_expr)
    return stack[0] if stack else ""

@app.route('/convert', methods=['POST', 'GET'])
def convert():
    try:
        expression = request.form.get('expression', '').strip()
        operation = request.form.get('operation', '').strip()
        
        if not expression or not operation:
            return "Error: Missing parameters", 400
        
        if operation == 'infix_postfix':
            result = infixToPostfix(expression)
            return f"Postfix({result})"
        elif operation == 'infix_prefix':
            result = infixToPrefix(expression)
            return f"Prefix({result})"
        elif operation == 'prefix_infix':
            result = prefixToInfix(expression)
            return f"Infix({result})"
        elif operation == 'postfix_infix':
            result = postfixToInfix(expression)
            return f"Infix({result})"
        else:
            return "Error: Unknown operation", 400
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/', methods=['GET'])
def home():
    return "Expression Converter API ✅ Ready!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
