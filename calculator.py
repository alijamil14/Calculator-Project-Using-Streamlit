import ast, math, operator, re
import streamlit as st

st.set_page_config(page_title="Scientific Calculator | Ali Jamil", page_icon="🧮", layout="centered")

for k, v in {
    "expr": "", "result": "", "on": True, "mode": "DEG",
    "second": False, "ans": 0.0, "memory": 0.0, "history": [],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def trig(fn, x):
    return fn(math.radians(x)) if st.session_state.mode == "DEG" else fn(x)

def invtrig(fn, x):
    v = fn(x)
    return math.degrees(v) if st.session_state.mode == "DEG" else v

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
BOPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod}
UOPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}

def nodeval(n):
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
    if isinstance(n, ast.Num): return n.n
    if isinstance(n, ast.BinOp) and type(n.op) in BOPS: return BOPS[type(n.op)](nodeval(n.left), nodeval(n.right))
    if isinstance(n, ast.UnaryOp) and type(n.op) in UOPS: return UOPS[type(n.op)](nodeval(n.operand))
    if isinstance(n, ast.Name) and n.id in {"pi", "e"}: return math.pi if n.id == "pi" else math.e
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in FUNCS:
        return FUNCS[n.func.id](*(nodeval(a) for a in n.args))
    raise ValueError("Invalid expression or unsupported function")

def evaluate(expr):
    s = expr.replace("×", "*").replace("÷", "/").replace("−", "-").replace("π", "pi").replace("^", "**")
    s = s.replace("sin⁻¹", "asin").replace("cos⁻¹", "acos").replace("tan⁻¹", "atan").replace("√", "sqrt")
    s = re.sub(r'(\b\d+(?:\.\d+)?|\bpi|\be|\))!', r'factorial(\1)', s)
    s = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', s)
    value = nodeval(ast.parse(s, mode="eval").body)
    if isinstance(value, complex) or not math.isfinite(float(value)):
        raise ValueError("Result is not a finite real number")
    return value

def fmt(v):
    return str(int(v)) if isinstance(v, float) and v.is_integer() else (f"{v:.12g}" if isinstance(v, float) else str(v))

def add(s):
    if st.session_state.on:
        st.session_state.expr += str(s)
        st.session_state.result = ""

def clear():
    st.session_state.expr = ""
    st.session_state.result = ""

def delete():
    st.session_state.expr = st.session_state.expr[:-1]
    st.session_state.result = ""

def calculate():
    if not st.session_state.on or not st.session_state.expr.strip(): return
    source = st.session_state.expr
    try:
        value = evaluate(source)
        result = fmt(value)
        st.session_state.ans = value
        st.session_state.result = result
        st.session_state.history.insert(0, (source, result, st.session_state.mode))
        st.session_state.history = st.session_state.history[:40]
        st.session_state.expr = result
    except ZeroDivisionError:
        st.session_state.result = "Cannot divide by zero"
    except Exception as e:
        st.session_state.result = f"Error: {e}"

st.markdown("""
<style>
.stApp{background:radial-gradient(ellipse at top left,#202b40 0%,#0a0f1b 62%,#06080e 100%);color:#f8fafc}
.block-container{max-width:960px;padding-top:1rem;padding-bottom:1rem}
.brand{font-size:12px;letter-spacing:4px;font-weight:800;color:#b9c5d8}
.title{font-size:30px;font-weight:850;line-height:1.2;color:#fff;margin:3px 0}
.subtitle{font-size:10px;letter-spacing:2.7px;color:#a6b2c7}
.screen{background:linear-gradient(140deg,#020304,#15121a 65%,#080a0e);border:1px solid #3b3039;border-radius:14px;padding:15px 17px;min-height:100px;text-align:right;box-shadow:inset 0 0 22px #000;margin:12px 0}
.expr{color:#aeb9c9;min-height:20px;font-size:14px;overflow-wrap:anywhere}
.output{font-size:32px;font-weight:800;color:#ff3b49;text-shadow:0 0 5px #ff2635,0 0 17px #ed1b32aa;overflow-wrap:anywhere}
.panel{background:#101725;border:1px solid #2d394d;border-radius:15px;padding:12px}
.panel-title{font-size:11px;letter-spacing:2px;color:#aab7cb;font-weight:800;margin:3px 0 10px}
div.stButton>button{min-height:39px;border-radius:9px;font-weight:750;border:1px solid #344055;transition:.12s}
div.stButton>button:hover{transform:translateY(-1px);border-color:#9aa9c0}
div.stButton>button[kind="secondary"]{background:#171f2d;color:#fff}
div[data-testid="stTextInput"] input{background:#101725;color:white}
.history{background:#0c1220;border:1px solid #273247;border-radius:9px;padding:9px;margin-bottom:7px}
@media(max-width:700px){.block-container{padding:.6rem}.title{font-size:25px}}
</style>
""", unsafe_allow_html=True)

top1, top2 = st.columns([4,1])
with top1:
    st.markdown('<div class="brand">ALI JAMIL</div><div class="title">Scientific Calculator</div><div class="subtitle">ADVANCED CALCULATION SYSTEM</div>', unsafe_allow_html=True)
with top2:
    st.markdown(f'<div style="font-weight:800;color:{"#22c55e" if st.session_state.on else "#ef4444"}">● {"ON" if st.session_state.on else "OFF"}</div>', unsafe_allow_html=True)
    if st.button("⏻ ON / OFF", use_container_width=True):
        st.session_state.on = not st.session_state.on
        if not st.session_state.on: clear()
        st.rerun()

calc, hist = st.columns([1.7, .9], gap="medium")
with calc:
    st.markdown('<div class="screen"><div class="expr">'+(st.session_state.expr or '&nbsp;')+'</div><div class="output">'+(st.session_state.result or '&nbsp;')+'</div></div>', unsafe_allow_html=True)
    c = st.columns(3, gap="small")
    for col, label, fn in zip(c, ["DEL","CLR","AC"], [delete,clear,clear]):
        with col:
            if st.button(label, key="utility_"+label, use_container_width=True, disabled=not st.session_state.on):
                fn(); st.rerun()
    sci, pad = st.columns([1,1.12], gap="small")
    with sci:
        st.markdown('<div class="panel-title">SCIENTIFIC</div>', unsafe_allow_html=True)
        md = st.columns(2)
        with md[0]:
            if st.button("DEG", use_container_width=True): st.session_state.mode="DEG"; st.rerun()
        with md[1]:
            if st.button("RAD", use_container_width=True): st.session_state.mode="RAD"; st.rerun()
        scientific = [
            [("2nd","second"),("sin","sin("),("cos","cos(")],
            [("tan","tan("),("sin⁻¹","sin⁻¹("),("cos⁻¹","cos⁻¹(")],
            [("tan⁻¹","tan⁻¹("),("√","√("),("x²","^2")],
            [("xʸ","^"),("log","log("),("ln","ln(")],
            [("π","π"),("e","e"),("!","!")],
            [("(","("),(")",")"),("%","%")],
            [("ANS","ans"),("M+","mplus"),("MR","mr")],
        ]
        for ri,row in enumerate(scientific):
            cols=st.columns(3,gap="small")
            for j,(label,val) in enumerate(row):
                with cols[j]:
                    if st.button(label,key=f"sf{ri}{j}",use_container_width=True,disabled=not st.session_state.on):
                        if val=="second": st.session_state.second=not st.session_state.second
                        elif val=="ans": add(fmt(st.session_state.ans))
                        elif val=="mplus":
                            try: st.session_state.memory += float(evaluate(st.session_state.expr))
                            except Exception: st.session_state.result="Enter a valid value first"
                        elif val=="mr": add(fmt(st.session_state.memory))
                        elif val in ("sin(","cos(","tan(") and st.session_state.second:
                            add({"sin(":"sin⁻¹(","cos(":"cos⁻¹(","tan(":"tan⁻¹("}[val])
                        else: add(val)
                        st.rerun()
        st.caption(f"Angle: {st.session_state.mode} · 2nd: {'ON' if st.session_state.second else 'OFF'}")
    with pad:
        st.markdown('<div class="panel-title">KEYPAD</div>', unsafe_allow_html=True)
        rows=[
            [("7","7","n"),("8","8","n"),("9","9","n"),("+","+","op")],
            [("4","4","n"),("5","5","n"),("6","6","n"),("−","-","op")],
            [("1","1","n"),("2","2","n"),("3","3","n"),("×","*","op")],
            [("0","0","n"),(".",".","n"),("(","(","n"),("÷","/","op")],
            [(") ",")","n"),("^","^","n"),("%","%","n"),("=","=","eq")],
        ]
        for ri,row in enumerate(rows):
            cols=st.columns(4,gap="small")
            for j,(label,val,kind) in enumerate(row):
                with cols[j]:
                    if kind=="op": st.markdown('<div style="color:#ff5964">',unsafe_allow_html=True)
                    if st.button(label,key=f"kp{ri}{j}",use_container_width=True,disabled=not st.session_state.on):
                        calculate() if val=="=" else add(val)
                        st.rerun()
    st.caption("Physical keyboard: click the input below, type an expression, then press Enter.")
with hist:
    st.markdown('<div class="panel-title">CALCULATION HISTORY</div>',unsafe_allow_html=True)
    if st.session_state.history:
        if st.button("Clear history",use_container_width=True): st.session_state.history=[]; st.rerun()
        for ex,res,mode in st.session_state.history:
            st.markdown(f'<div class="history"><div style="font-size:12px;color:#9eabc0;overflow-wrap:anywhere">{ex} · {mode}</div><div style="font-size:17px;font-weight:800;color:#ff4b58">= {res}</div></div>',unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:13px;color:#93a1b6">Your calculations will be saved here after you calculate.</div>',unsafe_allow_html=True)

def keyboard_submit():
    value=st.session_state.get("keyboard_expr","").strip()
    if value:
        if value.lower() in ("clear","ac","esc"): clear()
        elif value.lower()=="del": delete()
        else:
            # Accept a complete typed expression, then calculate on Enter.
            st.session_state.expr=value
            calculate()
    st.session_state.keyboard_expr=""

st.text_input("Keyboard expression", key="keyboard_expr", placeholder="Type e.g. 5+3, sin(30), 2^8 and press Enter", on_change=keyboard_submit, disabled=not st.session_state.on)
st.caption("Functions: sin, cos, tan, inverse trig, √, log, ln, factorial (!), π, e, %, powers, parentheses, and standard arithmetic.")
