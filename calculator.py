import ast, html, math, operator, re
import streamlit as st

st.set_page_config(page_title="Ali Jamil | Scientific Calculator", page_icon="🧮", layout="centered")

DEFAULTS = {
    "expr": "", "result": "", "power": True, "angle": "DEG",
    "second": False, "answer": 0.0, "memory": 0.0, "history": [],
    "keyboard_expr": "",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def trig(fn, x):
    return fn(math.radians(x)) if st.session_state.angle == "DEG" else fn(x)

def invtrig(fn, x):
    y = fn(x)
    return math.degrees(y) if st.session_state.angle == "DEG" else y

def fact(x):
    if x < 0 or not float(x).is_integer():
        raise ValueError("Factorial requires a non-negative integer")
    return math.factorial(int(x))

FUNCS = {
    "sin": lambda x: trig(math.sin, x), "cos": lambda x: trig(math.cos, x),
    "tan": lambda x: trig(math.tan, x), "asin": lambda x: invtrig(math.asin, x),
    "acos": lambda x: invtrig(math.acos, x), "atan": lambda x: invtrig(math.atan, x),
    "sqrt": math.sqrt, "log": math.log10, "ln": math.log, "abs": abs, "factorial": fact,
}
BINARY = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
          ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod}
UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}

def eval_node(n):
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
        return n.value
    if isinstance(n, ast.BinOp) and type(n.op) in BINARY:
        return BINARY[type(n.op)](eval_node(n.left), eval_node(n.right))
    if isinstance(n, ast.UnaryOp) and type(n.op) in UNARY:
        return UNARY[type(n.op)](eval_node(n.operand))
    if isinstance(n, ast.Name):
        if n.id == "pi": return math.pi
        if n.id == "e": return math.e
        raise ValueError(f"Unknown constant: {n.id}")
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in FUNCS:
        return FUNCS[n.func.id](*(eval_node(a) for a in n.args))
    raise ValueError("Invalid expression or unsupported function")

def evaluate(s):
    s = s.strip().replace("×", "*").replace("÷", "/").replace("−", "-")
    s = s.replace("π", "pi").replace("^", "**").replace("√", "sqrt")
    s = s.replace("sin⁻¹", "asin").replace("cos⁻¹", "acos").replace("tan⁻¹", "atan")
    s = re.sub(r'(\b\d+(?:\.\d+)?|\bpi|\be|\))!', r'factorial(\1)', s)
    s = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', s)
    value = eval_node(ast.parse(s, mode="eval").body)
    if isinstance(value, complex) or not math.isfinite(float(value)):
        raise ValueError("Result is not a finite real number")
    return value

def fmt(x):
    if isinstance(x, float):
        return str(int(x)) if x.is_integer() else f"{x:.12g}"
    return str(x)

def add(x):
    if st.session_state.power:
        st.session_state.expr += str(x)
        st.session_state.result = ""

def clear():
    st.session_state.expr = ""
    st.session_state.result = ""

def delete():
    st.session_state.expr = st.session_state.expr[:-1]
    st.session_state.result = ""

def calculate():
    if not st.session_state.power or not st.session_state.expr.strip():
        return
    original = st.session_state.expr
    try:
        value = evaluate(original)
        result = fmt(value)
        st.session_state.answer = value
        st.session_state.result = result
        st.session_state.history.insert(0, (original, result, st.session_state.angle))
        st.session_state.history = st.session_state.history[:30]
        st.session_state.expr = result
    except ZeroDivisionError:
        st.session_state.result = "Cannot divide by zero"
    except (ValueError, SyntaxError, TypeError, OverflowError) as e:
        st.session_state.result = f"Error: {e}"
    except Exception:
        st.session_state.result = "Calculation error"

st.markdown("""
<style>
.stApp{background:radial-gradient(ellipse at 50% 0%,#173d2b 0%,#0a1712 43%,#070b09 100%);color:#f7faf8}
.block-container{max-width:850px;padding-top:1.1rem;padding-bottom:1.1rem}
.aj-brand{text-align:center;font-size:13px;font-weight:800;letter-spacing:4px;color:#e8f1eb;margin-bottom:3px}
.aj-title{text-align:center;font-size:31px;font-weight:850;line-height:1.12;color:#fff;margin:0}
.aj-subtitle{text-align:center;font-size:10px;letter-spacing:3px;color:#b2c9bb;margin:7px 0 18px}
.screen{box-sizing:border-box;width:100%;min-height:112px;padding:13px 18px;border:1px solid #254a37;border-radius:17px;text-align:right;background:linear-gradient(145deg,#020704,#071b10 48%,#020504);box-shadow:inset 0 0 25px #000,0 7px 22px #0007;overflow:hidden;margin-bottom:12px}
.expr{min-height:22px;color:#f3f5f4;font-size:14px;line-height:1.5;overflow-wrap:anywhere}
.output{min-height:42px;color:#ff303f;font-size:36px;font-weight:800;line-height:1.2;text-shadow:0 0 5px #ff1429,0 0 13px #ff2639,0 0 26px #b50019;overflow-wrap:anywhere}
div.stButton>button{min-height:39px;border-radius:11px;font-size:15px;font-weight:750;border:1px solid #313a35;transition:all .14s}
div.stButton>button:hover{transform:translateY(-1px);border-color:#8ba497}
.utility div.stButton>button{background:#252e29!important;color:#f7faf8!important;border-color:#48564d!important;min-height:34px;font-size:12px}
.power-on div.stButton>button{background:#167c45!important;color:white!important;border-color:#38e982!important;box-shadow:0 0 10px #20d76b66;min-height:34px;font-size:12px}
.power-off div.stButton>button{background:#9f202b!important;color:white!important;border-color:#ff4a55!important;box-shadow:0 0 10px #ff263955;min-height:34px;font-size:12px}
.operator div.stButton>button{background:#F79422!important;color:#17110a!important;border-color:#ffb65f!important;font-size:18px}
.number-key div.stButton>button{background:#111412!important;color:white!important;border-color:#303a33!important}
.science-key div.stButton>button{background:#18221c!important;color:#f4faf5!important;border-color:#354b3b!important;min-height:36px;font-size:12px}
.equals-key div.stButton>button{background:#F79422!important;color:#17110a!important;border-color:#ffb65f!important}
.history-item{border:1px solid #273e30;background:#0b1510;border-radius:10px;padding:9px 10px;margin-bottom:8px}
.history-expr{color:#c5d3c9;font-size:12px;overflow-wrap:anywhere}
.history-result{color:#ff4a57;font-weight:800;font-size:17px;overflow-wrap:anywhere}
div[data-testid="stTextInput"] input{background:#0b1510;color:white;border:1px solid #365542}
@media(max-width:700px){.block-container{padding:.6rem}.aj-title{font-size:25px}.output{font-size:29px}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="aj-brand">Ali Jamil</div><div class="aj-title">Scientific Calculator</div><div class="aj-subtitle">ADVANCED CALCULATION SYSTEM</div>', unsafe_allow_html=True)

expr_html = html.escape(st.session_state.expr) or "&nbsp;"
result_html = html.escape(st.session_state.result) or "&nbsp;"
st.markdown(f'<div class="screen"><div class="expr">{expr_html}</div><div class="output">{result_html}</div></div>', unsafe_allow_html=True)

controls = st.columns([1, 1, 1, .62], gap="small")
for col, label, key, action in [
    (controls[0], "DEL", "top_del", delete),
    (controls[1], "CLR", "top_clr", clear),
    (controls[2], "AC", "top_ac", clear),
]:
    with col:
        st.markdown('<div class="utility">', unsafe_allow_html=True)
        if st.button(label, key=key, use_container_width=True, disabled=not st.session_state.power):
            action(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
with controls[3]:
    css = "power-on" if st.session_state.power else "power-off"
    label = "● ON" if st.session_state.power else "● OFF"
    st.markdown(f'<div class="{css}">', unsafe_allow_html=True)
    if st.button(label, key="power_switch", use_container_width=True):
        st.session_state.power = not st.session_state.power
        if not st.session_state.power: clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

science_col, keypad_col = st.columns([1, 1.08], gap="medium")
with science_col:
    st.markdown('<div style="font-size:11px;letter-spacing:2px;font-weight:800;color:#a9c2b1;margin:7px 0 10px">SCIENTIFIC FUNCTIONS</div>', unsafe_allow_html=True)
    modes = st.columns(2, gap="small")
    with modes[0]:
        if st.button("DEG", key="deg", use_container_width=True): st.session_state.angle="DEG"; st.rerun()
    with modes[1]:
        if st.button("RAD", key="rad", use_container_width=True): st.session_state.angle="RAD"; st.rerun()
    rows = [
        [("2nd","second"),("sin","sin("),("cos","cos(")],
        [("tan","tan("),("sin⁻¹","sin⁻¹("),("cos⁻¹","cos⁻¹(")],
        [("tan⁻¹","tan⁻¹("),("√","√("),("x²","^2")],
        [("xʸ","^"),("log","log("),("ln","ln(")],
        [("π","π"),("e","e"),("!","!")],
        [("(","("),(")",")"),("%","%")],
        [("ANS","ans"),("M+","mplus"),("MR","mr")],
    ]
    for ri, row in enumerate(rows):
        cols = st.columns(3, gap="small")
        for ci, (label, value) in enumerate(row):
            with cols[ci]:
                st.markdown('<div class="science-key">', unsafe_allow_html=True)
                if st.button(label, key=f"sci_{ri}_{ci}", use_container_width=True, disabled=not st.session_state.power):
                    if value == "second":
                        st.session_state.second = not st.session_state.second
                    elif value == "ans":
                        add(fmt(st.session_state.answer))
                    elif value == "mplus":
                        try: st.session_state.memory += float(evaluate(st.session_state.expr))
                        except Exception: st.session_state.result = "Enter a valid value first"
                    elif value == "mr":
                        add(fmt(st.session_state.memory))
                    elif value in ("sin(","cos(","tan(") and st.session_state.second:
                        add({"sin(":"sin⁻¹(","cos(":"cos⁻¹(","tan(":"tan⁻¹("}[value])
                    else:
                        add(value)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

with keypad_col:
    st.markdown('<div style="font-size:11px;letter-spacing:2px;font-weight:800;color:#a9c2b1;margin:7px 0 10px">KEYPAD</div>', unsafe_allow_html=True)
    rows = [
        [("7","7","n"),("8","8","n"),("9","9","n"),("+","+","op")],
        [("4","4","n"),("5","5","n"),("6","6","n"),("−","-","op")],
        [("1","1","n"),("2","2","n"),("3","3","n"),("×","*","op")],
        [(".",".","n"),("0","0","n"),("=","=","eq"),("÷","/","op")],
    ]
    for ri, row in enumerate(rows):
        cols = st.columns(4, gap="small")
        for ci, (label, value, kind) in enumerate(row):
            with cols[ci]:
                css = "operator" if kind == "op" else ("equals-key" if kind == "eq" else "number-key")
                st.markdown(f'<div class="{css}">', unsafe_allow_html=True)
                if st.button(label, key=f"key_{ri}_{ci}", use_container_width=True, disabled=not st.session_state.power):
                    calculate() if value == "=" else add(value)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# History appears only after at least one successful calculation; no helper text.
if st.session_state.history:
    st.markdown('<div style="font-size:11px;letter-spacing:2px;font-weight:800;color:#a9c2b1;margin:18px 0 9px">CALCULATION HISTORY</div>', unsafe_allow_html=True)
    if st.button("Clear history", key="clear_history"):
        st.session_state.history = []; st.rerun()
    cols = st.columns(3, gap="small")
    for i, (ex, result, mode) in enumerate(st.session_state.history):
        with cols[i % 3]:
            st.markdown(f'<div class="history-item"><div class="history-expr">{html.escape(ex)} · {mode}</div><div class="history-result">= {html.escape(result)}</div></div>', unsafe_allow_html=True)

# Focus this input to use the physical keyboard. Enter evaluates the full typed expression.
def keyboard_submit():
    typed = st.session_state.keyboard_expr.strip()
    if not typed: return
    if typed.lower() in {"clear", "ac", "esc", "escape"}:
        clear()
    elif typed.lower() in {"del", "backspace"}:
        delete()
    else:
        st.session_state.expr = typed
        calculate()
    st.session_state.keyboard_expr = ""

st.text_input("Keyboard expression", key="keyboard_expr", placeholder="Type expression and press Enter", label_visibility="collapsed", on_change=keyboard_submit, disabled=not st.session_state.power)
