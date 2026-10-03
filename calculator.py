import ast
import math
import operator
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# =========================================================
# SESSION STATE
# =========================================================

DEFAULTS = {
    "expression": "",
    "result": "0",
    "mode": "DEG",
    "calculator_on": True,
    "answer": 0,
    "second_function": False,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# SAFE MATHEMATICAL EVALUATOR
# =========================================================

BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def factorial(value):
    if value < 0 or int(value) != value:
        raise ValueError("Factorial requires a non-negative integer.")

    return math.factorial(int(value))


def sin_function(value):
    if st.session_state.mode == "DEG":
        value = math.radians(value)

    return math.sin(value)


def cos_function(value):
    if st.session_state.mode == "DEG":
        value = math.radians(value)

    return math.cos(value)


def tan_function(value):
    if st.session_state.mode == "DEG":
        value = math.radians(value)

    return math.tan(value)


def asin_function(value):
    result = math.asin(value)

    if st.session_state.mode == "DEG":
        return math.degrees(result)

    return result


def acos_function(value):
    result = math.acos(value)

    if st.session_state.mode == "DEG":
        return math.degrees(result)

    return result


def atan_function(value):
    result = math.atan(value)

    if st.session_state.mode == "DEG":
        return math.degrees(result)

    return result


FUNCTIONS = {
    "sin": sin_function,
    "cos": cos_function,
    "tan": tan_function,
    "asin": asin_function,
    "acos": acos_function,
    "atan": atan_function,
    "sqrt": math.sqrt,
    "log": math.log10,
    "ln": math.log,
    "abs": abs,
    "factorial": factorial,
}


CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "Ans": 0,
}


def evaluate_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Invalid value.")

    if isinstance(node, ast.Num):
        return node.n

    if isinstance(node, ast.Name):

        if node.id == "Ans":
            return st.session_state.answer

        if node.id in CONSTANTS:
            return CONSTANTS[node.id]

        raise ValueError(f"Unknown value: {node.id}")

    if isinstance(node, ast.UnaryOp):

        operation = UNARY_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported operation.")

        return operation(evaluate_node(node.operand))

    if isinstance(node, ast.BinOp):

        operation = BINARY_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported operation.")

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        return operation(left, right)

    if isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function.")

        function_name = node.func.id

        if function_name not in FUNCTIONS:
            raise ValueError(
                f"Unsupported function: {function_name}"
            )

        if len(node.args) != 1:
            raise ValueError(
                f"{function_name} requires one argument."
            )

        argument = evaluate_node(node.args[0])

        return FUNCTIONS[function_name](argument)

    raise ValueError("Invalid expression.")


def evaluate_expression(expression):

    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")
    expression = expression.replace("−", "-")
    expression = expression.replace("^", "**")

    expression = expression.replace("π", "pi")

    expression = expression.replace("√(", "sqrt(")

    expression = expression.replace("sin⁻¹(", "asin(")
    expression = expression.replace("cos⁻¹(", "acos(")
    expression = expression.replace("tan⁻¹(", "atan(")

    expression = expression.replace("!", "")

    expression = expression.replace("%", "/100")

    expression = expression.strip()

    if not expression:
        return 0

    tree = ast.parse(expression, mode="eval")

    result = evaluate_node(tree.body)

    if isinstance(result, complex):
        raise ValueError("Complex numbers are not supported.")

    if not math.isfinite(result):
        raise ValueError("Result is not finite.")

    return result


def format_result(value):

    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):

        if value.is_integer():
            return str(int(value))

        return f"{value:.12g}"

    return str(value)


# =========================================================
# CALCULATOR FUNCTIONS
# =========================================================

def add_value(value):

    if not st.session_state.calculator_on:
        return

    st.session_state.expression += value


def clear_all():

    st.session_state.expression = ""
    st.session_state.result = "0"


def delete_last():

    if not st.session_state.calculator_on:
        return

    st.session_state.expression = (
        st.session_state.expression[:-1]
    )


def calculate():

    if not st.session_state.calculator_on:
        return

    expression = st.session_state.expression

    if not expression:
        return

    try:

        result = evaluate_expression(expression)

        st.session_state.answer = result
        st.session_state.result = format_result(result)

    except ZeroDivisionError:

        st.session_state.result = "Cannot divide by 0"

    except Exception:

        st.session_state.result = "Error"


def toggle_second():

    if st.session_state.calculator_on:

        st.session_state.second_function = (
            not st.session_state.second_function
        )


def toggle_power():

    st.session_state.calculator_on = (
        not st.session_state.calculator_on
    )

    if not st.session_state.calculator_on:

        st.session_state.expression = ""
        st.session_state.result = ""

    else:

        st.session_state.expression = ""
        st.session_state.result = "0"


# =========================================================
# PROFESSIONAL UI CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL PAGE
       ===================================================== */

    .stApp {

        background:
            radial-gradient(
                circle at 50% -10%,
                #303030 0%,
                #171717 35%,
                #090909 75%,
                #050505 100%
            );

        min-height: 100vh;
    }


    .block-container {

        width: 100% !important;

        max-width: 820px !important;

        padding-top: 35px !important;
        padding-bottom: 40px !important;

        padding-left: 20px !important;
        padding-right: 20px !important;
    }


    #MainMenu,
    header,
    footer {

        visibility: hidden;
    }


    /* =====================================================
       MAIN CALCULATOR
       ===================================================== */

    .calculator-shell {

        width: 100%;

        box-sizing: border-box;

        background:
            linear-gradient(
                145deg,
                #202020,
                #151515
            );

        border: 1px solid #353535;

        border-radius: 32px;

        padding: 28px;

        box-shadow:

            0 40px 100px
            rgba(0, 0, 0, 0.75),

            inset 0 1px 0
            rgba(255, 255, 255, 0.06),

            inset 0 -1px 0
            rgba(0, 0, 0, 0.8);
    }


    /* =====================================================
       HEADER
       ===================================================== */

    .calculator-header {

        display: flex;

        align-items: center;

        gap: 16px;

        margin-bottom: 22px;
    }


    .calculator-logo {

        width: 62px;
        height: 62px;

        flex-shrink: 0;

        display: flex;

        align-items: center;
        justify-content: center;

        background:
            linear-gradient(
                145deg,
                #303030,
                #1d1d1d
            );

        border: 1px solid #464646;

        border-radius: 17px;

        font-size: 32px;

        box-shadow:

            0 8px 20px
            rgba(0, 0, 0, 0.35),

            inset 0 1px 0
            rgba(255,255,255,0.05);
    }


    .calculator-title {

        color: #ffffff;

        font-size: 29px;

        font-weight: 750;

        letter-spacing: -0.5px;

        line-height: 1.1;
    }


    .calculator-subtitle {

        color: #777777;

        font-size: 10px;

        font-weight: 600;

        letter-spacing: 2.2px;

        margin-top: 7px;
    }


    /* =====================================================
       DISPLAY
       ===================================================== */

    .calculator-display {

        position: relative;

        min-height: 165px;

        padding: 20px 24px;

        box-sizing: border-box;

        display: flex;

        flex-direction: column;

        justify-content: flex-end;

        align-items: flex-end;

        background:
            linear-gradient(
                145deg,
                #0b0b0b,
                #050505
            );

        border: 1px solid #303030;

        border-radius: 21px;

        margin-bottom: 22px;

        overflow: hidden;

        box-shadow:

            inset 0 7px 25px
            rgba(0,0,0,0.85),

            inset 0 -1px 0
            rgba(255,255,255,0.025),

            0 3px 10px
            rgba(0,0,0,0.3);
    }


    .calculator-display::before {

        content: "";

        position: absolute;

        top: 0;
        left: 0;

        width: 100%;
        height: 1px;

        background:
            rgba(255,255,255,0.08);
    }


    .display-mode {

        width: 100%;

        color: #8a8a8a;

        text-align: right;

        font-size: 10px;

        font-weight: 700;

        letter-spacing: 1.6px;

        margin-bottom: 5px;
    }


    .display-expression {

        width: 100%;

        min-height: 28px;

        color: #707070;

        text-align: right;

        font-size: 18px;

        line-height: 1.4;

        overflow-wrap: anywhere;
    }


    .display-result {

        width: 100%;

        color: #f7f7f7;

        text-align: right;

        font-size: 48px;

        font-weight: 600;

        letter-spacing: -1px;

        line-height: 1.1;

        overflow-wrap: anywhere;
    }


    /* =====================================================
       STREAMLIT CONTAINERS
       ===================================================== */

    div[data-testid="stVerticalBlock"] {

        gap: 0;
    }


    /* =====================================================
       BUTTON GRID
       ===================================================== */

    div[data-testid="column"] {

        padding-left: 4px !important;
        padding-right: 4px !important;

        min-width: 0 !important;
    }


    div.stButton {

        width: 100% !important;

        margin: 0 !important;
    }


    div.stButton > button {

        width: 100% !important;

        min-width: 100% !important;

        height: 72px !important;

        min-height: 72px !important;

        box-sizing: border-box !important;

        padding: 0 !important;

        border-radius: 15px !important;

        background:
            linear-gradient(
                145deg,
                #303030,
                #252525
            ) !important;

        color: #f2f2f2 !important;

        border: 1px solid #444444 !important;

        font-size: 20px !important;

        font-weight: 650 !important;

        letter-spacing: 0 !important;

        box-shadow:

            0 5px 0 #111111,

            0 8px 16px
            rgba(0,0,0,0.28),

            inset 0 1px 0
            rgba(255,255,255,0.05) !important;

        transition:
            transform 0.12s ease,
            background 0.12s ease,
            border-color 0.12s ease,
            box-shadow 0.12s ease !important;
    }


    div.stButton > button:hover {

        background:
            linear-gradient(
                145deg,
                #393939,
                #2d2d2d
            ) !important;

        border-color: #5c5c5c !important;

        transform: translateY(-2px) !important;

        box-shadow:

            0 7px 0 #111111,

            0 12px 22px
            rgba(0,0,0,0.35),

            inset 0 1px 0
            rgba(255,255,255,0.06) !important;
    }


    div.stButton > button:active {

        transform: translateY(4px) !important;

        box-shadow:

            0 1px 0 #111111,

            0 3px 7px
            rgba(0,0,0,0.3) !important;
    }


    /* =====================================================
       CONTROL BUTTONS
       ===================================================== */

    .st-key-control_row div.stButton > button {

        height: 58px !important;

        min-height: 58px !important;

        font-size: 14px !important;

        background:
            linear-gradient(
                145deg,
                #252525,
                #1d1d1d
            ) !important;
    }


    /* =====================================================
       SCIENTIFIC BUTTONS
       ===================================================== */

    .st-key-scientific_row_1 div.stButton > button,
    .st-key-scientific_row_2 div.stButton > button,
    .st-key-scientific_row_3 div.stButton > button {

        height: 62px !important;

        min-height: 62px !important;

        font-size: 16px !important;

        border-radius: 13px !important;
    }


    /* =====================================================
       OPERATOR ROWS
       ===================================================== */

    .st-key-row_operator_1 div.stButton:nth-child(4) > button,
    .st-key-row_operator_1 div.stButton:nth-child(5) > button,
    .st-key-row_operator_2 div.stButton:nth-child(4) > button,
    .st-key-row_operator_2 div.stButton:nth-child(5) > button {

        background:
            linear-gradient(
                145deg,
                #f09332,
                #d86e12
            ) !important;

        border-color: #f5a04d !important;

        color: #ffffff !important;

        box-shadow:

            0 5px 0 #914d12,

            0 8px 16px
            rgba(0,0,0,0.3),

            inset 0 1px 0
            rgba(255,255,255,0.15) !important;
    }


    .st-key-row_operator_1 div.stButton:nth-child(4) > button:hover,
    .st-key-row_operator_1 div.stButton:nth-child(5) > button:hover,
    .st-key-row_operator_2 div.stButton:nth-child(4) > button:hover,
    .st-key-row_operator_2 div.stButton:nth-child(5) > button:hover {

        background:
            linear-gradient(
                145deg,
                #ffa044,
                #e57b1d
            ) !important;
    }


    /* =====================================================
       DANGER ROW
       ===================================================== */

    .st-key-row_danger div.stButton:nth-child(4) > button,
    .st-key-row_danger div.stButton:nth-child(5) > button {

        background:
            linear-gradient(
                145deg,
                #df3b3b,
                #b91f1f
            ) !important;

        border-color: #ef6464 !important;

        color: #ffffff !important;

        box-shadow:

            0 5px 0 #711616,

            0 8px 16px
            rgba(0,0,0,0.3),

            inset 0 1px 0
            rgba(255,255,255,0.12) !important;
    }


    .st-key-row_danger div.stButton:nth-child(4) > button:hover,
    .st-key-row_danger div.stButton:nth-child(5) > button:hover {

        background:
            linear-gradient(
                145deg,
                #ef4a4a,
                #c92525
            ) !important;
    }


    /* =====================================================
       EQUAL BUTTON
       ===================================================== */

    .st-key-row_equals div.stButton:nth-child(5) > button {

        background:
            linear-gradient(
                145deg,
                #ffffff,
                #dcdcdc
            ) !important;

        color: #111111 !important;

        border-color: #ffffff !important;

        font-size: 25px !important;

        box-shadow:

            0 5px 0 #929292,

            0 8px 16px
            rgba(0,0,0,0.3),

            inset 0 1px 0
            rgba(255,255,255,0.8) !important;
    }


    .st-key-row_equals div.stButton:nth-child(5) > button:hover {

        background:
            linear-gradient(
                145deg,
                #ffffff,
                #eeeeee
            ) !important;
    }


    /* =====================================================
       SECTION HEADINGS
       ===================================================== */

    .section-heading {

        color: #707070;

        font-size: 10px;

        font-weight: 750;

        letter-spacing: 2px;

        text-transform: uppercase;

        margin:

            18px 0
            10px 4px;
    }


    /* =====================================================
       FOOTER STATUS
       ===================================================== */

    .calculator-status {

        display: flex;

        align-items: center;

        justify-content: space-between;

        margin-top: 17px;

        padding: 0 4px;

        color: #606060;

        font-size: 10px;

        font-weight: 600;

        letter-spacing: 1.3px;
    }


    .status-online {

        color: #6bc476;
    }


    .status-off {

        color: #e45c5c;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 700px) {

        .block-container {

            padding:

                15px
                8px
                30px
                8px !important;
        }


        .calculator-shell {

            padding: 17px;

            border-radius: 24px;
        }


        .calculator-logo {

            width: 49px;
            height: 49px;

            border-radius: 14px;

            font-size: 25px;
        }


        .calculator-title {

            font-size: 22px;
        }


        .calculator-subtitle {

            font-size: 8px;

            letter-spacing: 1.5px;
        }


        .calculator-display {

            min-height: 135px;

            padding: 16px;

            border-radius: 17px;
        }


        .display-result {

            font-size: 36px;
        }


        div[data-testid="column"] {

            padding-left: 2px !important;
            padding-right: 2px !important;
        }


        div.stButton > button {

            height: 62px !important;

            min-height: 62px !important;

            border-radius: 12px !important;

            font-size: 17px !important;
        }


        .st-key-scientific_row_1 div.stButton > button,
        .st-key-scientific_row_2 div.stButton > button,
        .st-key-scientific_row_3 div.stButton > button {

            height: 54px !important;

            min-height: 54px !important;

            font-size: 13px !important;
        }


        .st-key-control_row div.stButton > button {

            height: 52px !important;

            min-height: 52px !important;

            font-size: 12px !important;
        }
    }


    /* =====================================================
       SMALL PHONES
       ===================================================== */

    @media (max-width: 420px) {

        .calculator-shell {

            padding: 12px;
        }


        .calculator-title {

            font-size: 19px;
        }


        .calculator-subtitle {

            font-size: 7px;
        }


        div.stButton > button {

            height: 57px !important;

            min-height: 57px !important;

            font-size: 15px !important;
        }


        .st-key-scientific_row_1 div.stButton > button,
        .st-key-scientific_row_2 div.stButton > button,
        .st-key-scientific_row_3 div.stButton > button {

            height: 49px !important;

            min-height: 49px !important;

            font-size: 11px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CALCULATOR OPENING
# =========================================================

st.markdown(
    """
    <div class="calculator-shell">
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="calculator-header">

        <div class="calculator-logo">
            🧮
        </div>

        <div>

            <div class="calculator-title">
                Scientific Calculator
            </div>

            <div class="calculator-subtitle">
                ADVANCED CALCULATION SYSTEM
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DISPLAY
# =========================================================

if st.session_state.calculator_on:

    mode_text = f"{st.session_state.mode} MODE"

    expression_text = (
        st.session_state.expression
        if st.session_state.expression
        else "READY"
    )

    result_text = (
        st.session_state.result
        if st.session_state.result
        else "0"
    )

else:

    mode_text = "POWER OFF"
    expression_text = ""
    result_text = "OFF"


st.markdown(
    f"""
    <div class="calculator-display">

        <div class="display-mode">
            {mode_text}
        </div>

        <div class="display-expression">
            {expression_text}
        </div>

        <div class="display-result">
            {result_text}
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CONTROL ROW
# =========================================================

with st.container(key="control_row"):

    c1, c2, c3, c4 = st.columns(4, gap="small")

    with c1:

        if st.button(
            "DEG",
            key="mode_deg",
            use_container_width=True,
        ):

            st.session_state.mode = "DEG"

    with c2:

        if st.button(
            "RAD",
            key="mode_rad",
            use_container_width=True,
        ):

            st.session_state.mode = "RAD"

    with c3:

        if st.button(
            "CLR",
            key="clear",
            use_container_width=True,
        ):

            clear_all()

    with c4:

        power_text = (
            "OFF"
            if st.session_state.calculator_on
            else "ON"
        )

        if st.button(
            power_text,
            key="power_button",
            use_container_width=True,
        ):

            toggle_power()


# =========================================================
# SCIENTIFIC FUNCTIONS
# =========================================================

st.markdown(
    """
    <div class="section-heading">
        Scientific Functions
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SCIENTIFIC ROW 1
# =========================================================

with st.container(key="scientific_row_1"):

    c1, c2, c3, c4, c5, c6 = st.columns(
        6,
        gap="small",
    )

    scientific_row_1 = [
        ("2nd", "second"),
        ("sin", "sin("),
        ("cos", "cos("),
        ("tan", "tan("),
        ("π", "π"),
        ("e", "e"),
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4, c5, c6],
        scientific_row_1,
    ):

        with col:

            if st.button(
                label,
                key=f"sci_1_{label}",
                use_container_width=True,
            ):

                if value == "second":

                    toggle_second()

                else:

                    if st.session_state.second_function:

                        inverse = {
                            "sin(": "asin(",
                            "cos(": "acos(",
                            "tan(": "atan(",
                        }

                        value = inverse.get(
                            value,
                            value,
                        )

                        st.session_state.second_function = False

                    add_value(value)


# =========================================================
# SCIENTIFIC ROW 2
# =========================================================

with st.container(key="scientific_row_2"):

    c1, c2, c3, c4, c5, c6 = st.columns(
        6,
        gap="small",
    )

    scientific_row_2 = [
        ("log", "log("),
        ("ln", "ln("),
        ("√", "sqrt("),
        ("x²", "^2"),
        ("xʸ", "^"),
        ("!", "!"),
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4, c5, c6],
        scientific_row_2,
    ):

        with col:

            if st.button(
                label,
                key=f"sci_2_{label}",
                use_container_width=True,
            ):

                if value == "^2":

                    add_value("^2")

                elif value == "!":

                    add_value("!")

                else:

                    add_value(value)


# =========================================================
# SCIENTIFIC ROW 3
# =========================================================

with st.container(key="scientific_row_3"):

    c1, c2, c3, c4, c5, c6 = st.columns(
        6,
        gap="small",
    )

    scientific_row_3 = [
        ("(", "("),
        (")", ")"),
        ("%", "%"),
        ("EXP", "e"),
        ("ANS", "Ans"),
        ("M+", "Ans+"),
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4, c5, c6],
        scientific_row_3,
    ):

        with col:

            if st.button(
                label,
                key=f"sci_3_{label}",
                use_container_width=True,
            ):

                if value == "Ans+":

                    add_value("Ans")

                else:

                    add_value(value)


# =========================================================
# MAIN KEYPAD
# =========================================================

st.markdown(
    """
    <div class="section-heading">
        Keypad
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 7 8 9 DEL AC
# =========================================================

with st.container(key="row_danger"):

    c1, c2, c3, c4, c5 = st.columns(
        5,
        gap="small",
    )

    with c1:

        if st.button(
            "7",
            key="number_7",
            use_container_width=True,
        ):

            add_value("7")

    with c2:

        if st.button(
            "8",
            key="number_8",
            use_container_width=True,
        ):

            add_value("8")

    with c3:

        if st.button(
            "9",
            key="number_9",
            use_container_width=True,
        ):

            add_value("9")

    with c4:

        if st.button(
            "DEL",
            key="delete",
            use_container_width=True,
        ):

            delete_last()

    with c5:

        if st.button(
            "AC",
            key="all_clear",
            use_container_width=True,
        ):

            clear_all()


# =========================================================
# 4 5 6 × ÷
# =========================================================

with st.container(key="row_operator_1"):

    c1, c2, c3, c4, c5 = st.columns(
        5,
        gap="small",
    )

    with c1:

        if st.button(
            "4",
            key="number_4",
            use_container_width=True,
        ):

            add_value("4")

    with c2:

        if st.button(
            "5",
            key="number_5",
            use_container_width=True,
        ):

            add_value("5")

    with c3:

        if st.button(
            "6",
            key="number_6",
            use_container_width=True,
        ):

            add_value("6")

    with c4:

        if st.button(
            "×",
            key="multiply",
            use_container_width=True,
        ):

            add_value("×")

    with c5:

        if st.button(
            "÷",
            key="divide",
            use_container_width=True,
        ):

            add_value("÷")


# =========================================================
# 1 2 3 + −
# =========================================================

with st.container(key="row_operator_2"):

    c1, c2, c3, c4, c5 = st.columns(
        5,
        gap="small",
    )

    with c1:

        if st.button(
            "1",
            key="number_1",
            use_container_width=True,
        ):

            add_value("1")

    with c2:

        if st.button(
            "2",
            key="number_2",
            use_container_width=True,
        ):

            add_value("2")

    with c3:

        if st.button(
            "3",
            key="number_3",
            use_container_width=True,
        ):

            add_value("3")

    with c4:

        if st.button(
            "+",
            key="addition",
            use_container_width=True,
        ):

            add_value("+")

    with c5:

        if st.button(
            "−",
            key="subtraction",
            use_container_width=True,
        ):

            add_value("−")


# =========================================================
# 0 . EXP ANS =
# =========================================================

with st.container(key="row_equals"):

    c1, c2, c3, c4, c5 = st.columns(
        5,
        gap="small",
    )

    with c1:

        if st.button(
            "0",
            key="number_0",
            use_container_width=True,
        ):

            add_value("0")

    with c2:

        if st.button(
            ".",
            key="decimal",
            use_container_width=True,
        ):

            add_value(".")

    with c3:

        if st.button(
            "EXP",
            key="scientific_exp",
            use_container_width=True,
        ):

            add_value("e")

    with c4:

        if st.button(
            "ANS",
            key="previous_answer",
            use_container_width=True,
        ):

            add_value("Ans")

    with c5:

        if st.button(
            "=",
            key="calculate",
            use_container_width=True,
        ):

            calculate()


# =========================================================
# STATUS BAR
# =========================================================

if st.session_state.calculator_on:

    status_text = "● ON"
    status_class = "status-online"

else:

    status_text = "● OFF"
    status_class = "status-off"


st.markdown(
    f"""
    <div class="calculator-status">

        <span>
            SCIENTIFIC MODE
        </span>

        <span class="{status_class}">
            {status_text}
        </span>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CLOSE CALCULATOR
# =========================================================

st.markdown(
    """
    </div>
    """,
    unsafe_allow_html=True,
)