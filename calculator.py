import ast
import math
import operator
import re
import html
import streamlit as st

st.set_page_config(page_title="Scientific Calculator | Ali Jamil", page_icon="🧮", layout="centered")

# -------------------- Session state --------------------
DEFAULTS = {
    "expression": "", "result": "", "calculator_on": True, "mode": "DEG",
    "second_function": False, "answer": 0.0, "memory": 0.0, "history": [],
    "keyboard_expression": "",
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------- Safe scientific calculation engine --------------------
def trig(fn, x):
    return fn(math.radians(x)) if st.session_state.mode == "DEG" else fn(x)

def inv_trig(fn, x):
    result = fn(x)
    return math.degrees(result) if st.session_state.mode == "DEG" else result

def factorial_value(x):
    if x < 0 or not float(x).is_integer():
        raise ValueError("Factorial requires a non-negative integer")
    return math.factorial(int(x))

FUNCTIONS = {
    "sin": lambda x: trig(math.sin, x),
    "cos": lambda x: trig(math.cos, x),
    "tan": lambda x: trig(math.tan, x),
    "asin": lambda x: inv_trig(math.asin, x),
    "acos": lambda x: inv_trig(math.acos, x),
    "atan": lambda x: inv_trig(math.atan, x),
    "sqrt": math.sqrt, "log": math.log10, "ln": math.log,
    "abs": abs, "factorial": factorial_value,
}
BINARY_OPERATORS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
}
UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}

def evaluate_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Invalid number")
    # ast.Num was removed in some newer Python versions; avoid accessing ast.Num.
    if isinstance(node, ast.BinOp) and type(node.op) in BINARY_OPERATORS:
        return BINARY_OPERATORS[type(node.op)](evaluate_node(node.left), evaluate_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPERATORS:
        return UNARY_OPERATORS[type(node.op)](evaluate_node(node.operand))
    if isinstance(node, ast.Name):
        if node.id == "pi": return math.pi
        if node.id == "e": return math.e
        raise ValueError(f"Unknown constant: {node.id}")
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        function_name = node.func.id
        if function_name not in FUNCTIONS:
            raise ValueError(f"Unsupported function: {function_name}")
        return FUNCTIONS[function_name](*(evaluate_node(arg) for arg in node.args))
    raise ValueError("Invalid expression")

def evaluate_expression(expression):
    text = expression.strip()
    text = text.replace("×", "*").replace("÷", "/").replace("−", "-")
    text = text.replace("π", "pi").replace("^", "**").replace("√", "sqrt")
    text = text.replace("sin⁻¹", "asin").replace("cos⁻¹", "acos").replace("tan⁻¹", "atan")
    # Convert postfix factorial on numbers, constants, or closed parentheses.
    text = re.sub(r'(\b\d+(?:\.\d+)?|\bpi|\be|\))!', r'factorial(\1)', text)
    # Percent on a number: 25% means 25/100.
    text = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', text)
    tree = ast.parse(text, mode="eval")
    value = evaluate_node(tree.body)
    if isinstance(value, complex) or not math.isfinite(float(value)):
        raise ValueError("Result is not a finite real number")
    return value

def format_result(value):
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return f"{value:.12g}"
    return str(value)

def add_value(value):
    if st.session_state.calculator_on:
        st.session_state.expression += str(value)
        st.session_state.result = ""

def clear_all():
    st.session_state.expression = ""
    st.session_state.result = ""

def delete_last():
    st.session_state.expression = st.session_state.expression[:-1]
    st.session_state.result = ""

def calculate():
    if not st.session_state.calculator_on or not st.session_state.expression.strip():
        return
    original = st.session_state.expression
    try:
        value = evaluate_expression(original)
        result = format_result(value)
        st.session_state.answer = value
        st.session_state.result = result
        st.session_state.history.insert(0, (original, result, st.session_state.mode))
        st.session_state.history = st.session_state.history[:40]
        st.session_state.expression = result
    except ZeroDivisionError:
        st.session_state.result = "Cannot divide by zero"
    except (ValueError, SyntaxError, TypeError, OverflowError) as exc:
        st.session_state.result = f"Error: {exc}"
    except Exception:
        st.session_state.result = "Calculation error"

# -------------------- Compact professional styling --------------------
st.markdown("""
<style>
.stApp {background:linear-gradient(135deg,#d9e0eb 0%,#aebbd0 100%);color:#101522}
.block-container {max-width:1040px;padding-top:1.1rem;padding-bottom:1.2rem}
.brand {font-size:12px;letter-spacing:3px;font-weight:800;color:#4d5870}
.title {font-size:30px;line-height:1.15;font-weight:850;color:#141925;margin:2px 0 3px}
.subtitle {font-size:10px;letter-spacing:2.5px;color:#59647a}
.screen {background:linear-gradient(145deg,#030405,#111318 70%,#050607);border:1px solid #414550;border-radius:23px;padding:20px 20px 17px;min-height:120px;text-align:right;box-shadow:0 10px 24px #10152235,inset 0 0 20px #000;margin:10px 0 12px}
.expr {color:#a7adbb;min-height:22px;font-size:14px;overflow-wrap:anywhere}
.output {font-size:clamp(34px,4vw,46px);line-height:1.2;font-weight:500;color:#ff424e;text-shadow:0 0 4px #ff2635,0 0 13px #ed1b3280;overflow-wrap:anywhere}
.panel {background:rgba(244,247,252,.72);border:1px solid #c2cada;border-radius:24px;padding:14px;box-shadow:0 8px 22px #24314a20}
.panel-title {font-size:11px;letter-spacing:1.7px;color:#59647a;font-weight:800;margin:2px 0 9px}
div.stButton>button {min-height:45px;border-radius:15px;font-weight:650;font-size:16px;border:1px solid #c7cfdf;background:linear-gradient(145deg,#f9fbff,#d9dfeb);color:#182033;box-shadow:0 3px 6px #1c294020;transition:all .12s ease}
div.stButton>button:hover {transform:translateY(-1px);border-color:#a8b2c6;box-shadow:0 5px 9px #1c294030}
div.stButton>button:disabled {opacity:.45}
.utility div.stButton>button {background:linear-gradient(145deg,#f8faff,#dce2ee)!important;color:#20283a!important;border-radius:16px!important}
.operator div.stButton>button {background:linear-gradient(145deg,#ffad48,#e87916)!important;color:#fff!important;border-color:#e58a2c!important;border-radius:16px!important;box-shadow:0 3px 7px #b65c2435!important}
.equal div.stButton>button {background:linear-gradient(145deg,#ffad48,#e87916)!important;color:#fff!important;border-color:#e58a2c!important;border-radius:16px!important}
.science div.stButton>button {background:linear-gradient(145deg,#eef2fa,#cdd5e5)!important;color:#20283a!important;min-height:40px;font-size:13px;border-radius:15px!important}
.history-item {background:#f4f6fb;border:1px solid #d2d9e7;border-radius:13px;padding:10px;margin-bottom:8px}
.history-expression {font-size:12px;color:#667085;overflow-wrap:anywhere}
.history-result {font-size:17px;font-weight:800;color:#d94835;overflow-wrap:anywhere}
.status-on {color:#168447;font-size:11px;font-weight:800}
.status-off {color:#c72c3b;font-size:11px;font-weight:800}
@media(max-width:700px) {.block-container{padding:.55rem}.title{font-size:25px}.panel{padding:9px}.screen{padding:15px;min-height:100px}div.stButton>button{min-height:40px;font-size:14px;border-radius:13px}}
</style>
""", unsafe_allow_html=True)

# -------------------- Header --------------------
header_left, header_right = st.columns([5, 1])
with header_left:
    st.markdown(
        '<div class="brand">ALI JAMIL</div><div class="title">Scientific Calculator</div>'
        '<div class="subtitle">ADVANCED CALCULATION SYSTEM</div>',
        unsafe_allow_html=True,
    )
with header_right:
    status_class = "status-on" if st.session_state.calculator_on else "status-off"
    status_text = "● ON" if st.session_state.calculator_on else "● OFF"
    st.markdown(f'<div class="{status_class}">{status_text}</div>', unsafe_allow_html=True)

# Layout: calculator left, history right.
calculator_col, history_col = st.columns([1.7, 0.9], gap="medium")

with calculator_col:
    # Display: escaped user text prevents accidental HTML injection.
    expr_html = html.escape(st.session_state.expression) or "&nbsp;"
    result_html = html.escape(st.session_state.result) or "&nbsp;"
    st.markdown(
        f'<div class="screen"><div class="expr">{expr_html}</div><div class="output">{result_html}</div></div>',
        unsafe_allow_html=True,
    )

    # Tiny power control sits directly below the output screen.
    power_cols = st.columns([4, 1.05])
    with power_cols[0]:
        utility_cols = st.columns(3, gap="small")
        for col, label, fn in zip(utility_cols, ["DEL", "CLR", "AC"], [delete_last, clear_all, clear_all]):
            with col:
                st.markdown('<div class="utility">', unsafe_allow_html=True)
                if st.button(label, key=f"utility_{label}", use_container_width=True, disabled=not st.session_state.calculator_on):
                    fn()
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    with power_cols[1]:
        if st.button("⏻ ON" if not st.session_state.calculator_on else "⏻ OFF",
                     key="power_small", use_container_width=True):
            st.session_state.calculator_on = not st.session_state.calculator_on
            if not st.session_state.calculator_on:
                clear_all()
            st.rerun()

    scientific_col, keypad_col = st.columns([1, 1.12], gap="small")

    with scientific_col:
        
        mode_cols = st.columns(2, gap="small")
        with mode_cols[0]:
            if st.button("DEG", key="mode_deg", use_container_width=True):
                st.session_state.mode = "DEG"
                st.rerun()
        with mode_cols[1]:
            if st.button("RAD", key="mode_rad", use_container_width=True):
                st.session_state.mode = "RAD"
                st.rerun()

        science_rows = [
            [("2nd", "second"), ("sin", "sin("), ("cos", "cos(")],
            [("tan", "tan("), ("sin⁻¹", "sin⁻¹("), ("cos⁻¹", "cos⁻¹(")],
            [("tan⁻¹", "tan⁻¹("), ("√", "√("), ("x²", "^2")],
            [("xʸ", "^"), ("log", "log("), ("ln", "ln(")],
            [("π", "π"), ("e", "e"), ("!", "!")],
            [("(", "("), (")", ")"), ("%", "%")],
            [("ANS", "ans"), ("M+", "mplus"), ("MR", "mr")],
        ]
        for row_index, row in enumerate(science_rows):
            cols = st.columns(3, gap="small")
            for col_index, (label, value) in enumerate(row):
                with cols[col_index]:
                    st.markdown('<div class="science">', unsafe_allow_html=True)
                    if st.button(label, key=f"science_{row_index}_{col_index}",
                                 use_container_width=True, disabled=not st.session_state.calculator_on):
                        if value == "second":
                            st.session_state.second_function = not st.session_state.second_function
                        elif value == "ans":
                            add_value(format_result(st.session_state.answer))
                        elif value == "mplus":
                            try:
                                st.session_state.memory += float(evaluate_expression(st.session_state.expression))
                            except Exception:
                                st.session_state.result = "Enter a valid value first"
                        elif value == "mr":
                            add_value(format_result(st.session_state.memory))
                        elif value in ("sin(", "cos(", "tan(") and st.session_state.second_function:
                            add_value({"sin(": "sin⁻¹(", "cos(": "cos⁻¹(", "tan(": "tan⁻¹("}[value])
                        else:
                            add_value(value)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

    with keypad_col:
        
        keypad_rows = [
            [("7", "7", "n"), ("8", "8", "n"), ("9", "9", "n"), ("+", "+", "op")],
            [("4", "4", "n"), ("5", "5", "n"), ("6", "6", "n"), ("−", "-", "op")],
            [("1", "1", "n"), ("2", "2", "n"), ("3", "3", "n"), ("×", "*", "op")],
            [("0", "0", "n"), (".", ".", "n"), ("(", "(", "n"), ("÷", "/", "op")],
            [(")", ")", "n"), ("^", "^", "n"), ("%", "%", "n"), ("=", "=", "eq")],
        ]
        for row_index, row in enumerate(keypad_rows):
            cols = st.columns(4, gap="small")
            for col_index, (label, value, kind) in enumerate(row):
                with cols[col_index]:
                    css_class = "operator" if kind == "op" else ("equal" if kind == "eq" else "keypad")
                    st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                    if st.button(label, key=f"keypad_{row_index}_{col_index}",
                                 use_container_width=True, disabled=not st.session_state.calculator_on):
                        calculate() if value == "=" else add_value(value)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

with history_col:
    
    if st.session_state.history:
        if st.button("Clear history", key="clear_history", use_container_width=True):
            st.session_state.history = []
            st.rerun()
        for expression, result, mode in st.session_state.history:
            expression_html = html.escape(expression)
            result_html = html.escape(result)
            st.markdown(
                f'<div class="history-item"><div class="history-expression">{expression_html} · {mode}</div>'
                f'<div class="history-result">= {result_html}</div></div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown('<div style="font-size:13px;color:#93a1b6">No calculations yet.</div>', unsafe_allow_html=True)

# Physical keyboard: type a complete expression into this compact field and press Enter.
def keyboard_submit():
    typed = st.session_state.keyboard_expression.strip()
    if not typed:
        return
    if typed.lower() in {"clear", "ac", "esc", "escape"}:
        clear_all()
    elif typed.lower() in {"del", "backspace"}:
        delete_last()
    else:
        st.session_state.expression = typed
        calculate()
    st.session_state.keyboard_expression = ""

st.text_input(
    "Keyboard expression",
    key="keyboard_expression",
    placeholder="Keyboard input",
    label_visibility="collapsed",
    on_change=keyboard_submit,
    disabled=not st.session_state.calculator_on,
)
