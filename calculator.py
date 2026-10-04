
import ast
import math
import operator
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered",
)


# =========================================================
# SESSION STATE
# =========================================================

if "expression" not in st.session_state:
    st.session_state.expression = ""

if "result" not in st.session_state:
    st.session_state.result = "0"

if "mode" not in st.session_state:
    st.session_state.mode = "DEG"

if "calculator_on" not in st.session_state:
    st.session_state.calculator_on = True

if "answer" not in st.session_state:
    st.session_state.answer = 0

if "second_function" not in st.session_state:
    st.session_state.second_function = False


# =========================================================
# CALCULATOR FUNCTIONS
# =========================================================

def add_value(value):
    """Add a value to the current expression."""

    if not st.session_state.calculator_on:
        return

    if not st.session_state.expression:
        st.session_state.expression = value
        return

    st.session_state.expression += value


def clear_all():
    """Clear the complete calculator."""

    st.session_state.expression = ""
    st.session_state.result = "0"


def delete_last():
    """Delete the last character from the expression."""

    if not st.session_state.calculator_on:
        return

    st.session_state.expression = (
        st.session_state.expression[:-1]
    )


def toggle_power():
    """Turn the calculator ON or OFF."""

    st.session_state.calculator_on = (
        not st.session_state.calculator_on
    )

    if not st.session_state.calculator_on:
        st.session_state.expression = ""
        st.session_state.result = ""
        st.session_state.second_function = False

    else:
        st.session_state.expression = ""
        st.session_state.result = "0"


def toggle_second():
    """Toggle second/inverse scientific functions."""

    if st.session_state.calculator_on:
        st.session_state.second_function = (
            not st.session_state.second_function
        )


# =========================================================
# SCIENTIFIC FUNCTIONS
# =========================================================

def sin_func(x):

    if st.session_state.mode == "DEG":
        x = math.radians(x)

    return math.sin(x)


def cos_func(x):

    if st.session_state.mode == "DEG":
        x = math.radians(x)

    return math.cos(x)


def tan_func(x):

    if st.session_state.mode == "DEG":
        x = math.radians(x)

    return math.tan(x)


def asin_func(x):

    result = math.asin(x)

    if st.session_state.mode == "DEG":
        return math.degrees(result)

    return result


def acos_func(x):

    result = math.acos(x)

    if st.session_state.mode == "DEG":
        return math.degrees(result)

    return result


def atan_func(x):

    result = math.atan(x)

    if st.session_state.mode == "DEG":
        return math.degrees(result)

    return result


def factorial(x):

    if x < 0 or int(x) != x:
        raise ValueError

    return math.factorial(int(x))


FUNCTIONS = {
    "sin": sin_func,
    "cos": cos_func,
    "tan": tan_func,
    "asin": asin_func,
    "acos": acos_func,
    "atan": atan_func,
    "sqrt": math.sqrt,
    "log": math.log10,
    "ln": math.log,
    "factorial": factorial,
}


# =========================================================
# SAFE EXPRESSION EVALUATOR
# =========================================================

def evaluate_node(node):

    # -----------------------------------------------------
    # Numbers
    # -----------------------------------------------------

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError


    # -----------------------------------------------------
    # Constants
    # -----------------------------------------------------

    if isinstance(node, ast.Name):

        if node.id == "pi":
            return math.pi

        if node.id == "e":
            return math.e

        if node.id == "Ans":
            return st.session_state.answer

        raise ValueError


    # -----------------------------------------------------
    # Unary operations
    # -----------------------------------------------------

    if isinstance(node, ast.UnaryOp):

        if isinstance(node.op, ast.UAdd):
            return +evaluate_node(node.operand)

        if isinstance(node.op, ast.USub):
            return -evaluate_node(node.operand)

        raise ValueError


    # -----------------------------------------------------
    # Binary operations
    # -----------------------------------------------------

    if isinstance(node, ast.BinOp):

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        if isinstance(node.op, ast.Add):
            return left + right

        if isinstance(node.op, ast.Sub):
            return left - right

        if isinstance(node.op, ast.Mult):
            return left * right

        if isinstance(node.op, ast.Div):
            return left / right

        if isinstance(node.op, ast.Pow):
            return left ** right

        if isinstance(node.op, ast.Mod):
            return left % right

        raise ValueError


    # -----------------------------------------------------
    # Scientific function calls
    # -----------------------------------------------------

    if isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise ValueError

        name = node.func.id

        if name not in FUNCTIONS:
            raise ValueError

        if len(node.args) != 1:
            raise ValueError

        argument = evaluate_node(node.args[0])

        return FUNCTIONS[name](argument)


    raise ValueError


# =========================================================
# EXPRESSION CONVERSION
# =========================================================

def evaluate_expression(expression):

    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")
    expression = expression.replace("−", "-")
    expression = expression.replace("^", "**")
    expression = expression.replace("π", "pi")

    expression = expression.replace(
        "√(",
        "sqrt("
    )

    expression = expression.replace(
        "sin⁻¹(",
        "asin("
    )

    expression = expression.replace(
        "cos⁻¹(",
        "acos("
    )

    expression = expression.replace(
        "tan⁻¹(",
        "atan("
    )

    expression = expression.replace(
        "%",
        "/100"
    )

    tree = ast.parse(
        expression,
        mode="eval",
    )

    return evaluate_node(tree.body)


# =========================================================
# CALCULATE
# =========================================================

def calculate():

    if not st.session_state.calculator_on:
        return

    expression = st.session_state.expression

    if not expression:
        return

    try:

        value = evaluate_expression(expression)

        st.session_state.answer = value

        if isinstance(value, float) and value.is_integer():
            value = int(value)

        st.session_state.result = str(value)

        st.session_state.expression = str(value)

    except ZeroDivisionError:

        st.session_state.result = "Cannot divide by 0"

    except Exception:

        st.session_state.result = "Error"


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       PAGE
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 50% 0%,
                #303030 0%,
                #161616 45%,
                #070707 100%
            );
    }

    .block-container {
        max-width: 780px !important;
        padding-top: 35px !important;
        padding-bottom: 40px !important;
    }

    header,
    footer,
    #MainMenu {
        visibility: hidden;
    }


    /* =====================================================
       CALCULATOR
       ===================================================== */

    .calculator-box {
        background: #181818;
        border: 1px solid #363636;
        border-radius: 30px;
        padding: 28px;

        box-shadow:
            0 30px 80px rgba(0, 0, 0, 0.75),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }


    /* =====================================================
       HEADER
       ===================================================== */

    .header-title {
        color: white;
        font-size: 29px;
        font-weight: 700;
        margin-bottom: 3px;
    }

    .header-subtitle {
        color: #777;
        font-size: 10px;
        letter-spacing: 2px;
    }


    /* =====================================================
       DISPLAY
       ===================================================== */

    .display-box {
        background: #080808;
        border: 1px solid #303030;
        border-radius: 20px;
        padding: 20px;
        min-height: 145px;

        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        text-align: right;

        margin: 20px 0;

        box-shadow:
            inset 0 5px 20px rgba(0, 0, 0, 0.8);
    }

    .result-text {
        color: white;
        font-size: 46px;
        font-weight: 600;

        overflow-wrap: anywhere;
        word-break: break-word;
    }


    /* =====================================================
       SECTION TITLE
       ===================================================== */

    .section-title {
        color: #666;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;

        margin: 18px 0 9px 2px;

        text-transform: uppercase;
    }


    /* =====================================================
       COLUMNS
       ===================================================== */

    div[data-testid="column"] {
        padding-left: 3px !important;
        padding-right: 3px !important;
    }


    /* =====================================================
       ALL BUTTONS
       ===================================================== */

    div.stButton {
        width: 100%;
    }

    div.stButton > button {

        width: 100% !important;

        height: 70px !important;
        min-height: 70px !important;

        border-radius: 14px !important;

        background:
            linear-gradient(
                145deg,
                #303030,
                #242424
            ) !important;

        color: #ffffff !important;

        border: 1px solid #444444 !important;

        font-size: 20px !important;
        font-weight: 600 !important;

        box-shadow:
            0 5px 0 #111,
            0 8px 14px rgba(0, 0, 0, 0.3);

        transition: 0.12s ease !important;
    }

    div.stButton > button:hover {

        background:
            linear-gradient(
                145deg,
                #3a3a3a,
                #2b2b2b
            ) !important;

        border-color: #666 !important;

        transform: translateY(-2px) !important;
    }

    div.stButton > button:active {

        transform: translateY(3px) !important;

        box-shadow:
            0 1px 0 #111 !important;
    }


    /* =====================================================
       ON / OFF BUTTON
       ===================================================== */

    .on-button + div.stButton > button,
    .on-button ~ div.stButton > button {

        background:
            linear-gradient(
                145deg,
                #2e7d32,
                #1b5e20
            ) !important;

        color: white !important;

        border-color: #66bb6a !important;

        box-shadow:
            0 5px 0 #124416,
            0 8px 14px rgba(0, 0, 0, 0.30) !important;
    }


    /* =====================================================
       DEL BUTTON
       ===================================================== */

    .del-button + div.stButton > button,
    .del-button ~ div.stButton > button {

        background:
            linear-gradient(
                145deg,
                #df3c3c,
                #b91f1f
            ) !important;

        color: white !important;

        border-color: #ef6464 !important;

        box-shadow:
            0 5px 0 #711616,
            0 8px 14px rgba(0, 0, 0, 0.30) !important;
    }


    /* =====================================================
       KEYPAD WHITE BUTTONS
       ===================================================== */

    .keypad-button + div.stButton > button,
    .keypad-button ~ div.stButton > button {

        background: #ffffff !important;

        color: #111111 !important;

        border-color: #ffffff !important;

        box-shadow:
            0 5px 0 #aaaaaa,
            0 8px 14px rgba(0, 0, 0, 0.25) !important;
    }

    .keypad-button + div.stButton > button:hover,
    .keypad-button ~ div.stButton > button:hover {

        background: #f2f2f2 !important;

        color: #111111 !important;

        border-color: #ffffff !important;
    }


    /* =====================================================
       CONTROL BUTTONS
       ===================================================== */

    .control-button div.stButton > button {

        height: 55px !important;
        min-height: 55px !important;

        font-size: 14px !important;
    }


    /* =====================================================
       SCIENTIFIC BUTTONS
       ===================================================== */

    .scientific-button div.stButton > button {

        height: 60px !important;
        min-height: 60px !important;

        font-size: 15px !important;
    }


    /* =====================================================
       EQUAL BUTTON
       ===================================================== */

    .equal-button + div.stButton > button,
    .equal-button ~ div.stButton > button {

        background:
            linear-gradient(
                145deg,
                #ffffff,
                #dcdcdc
            ) !important;

        color: #111111 !important;

        border-color: white !important;

        font-size: 25px !important;

        box-shadow:
            0 5px 0 #929292,
            0 8px 14px rgba(0, 0, 0, 0.3) !important;
    }


    /* =====================================================
       STATUS
       ===================================================== */

    .status-bar {

        display: flex;
        justify-content: space-between;

        margin-top: 17px;

        color: #666;

        font-size: 10px;

        letter-spacing: 1.3px;
    }

    .status-on {
        color: #6bc476;
    }

    .status-off {
        color: #e45c5c;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 600px) {

        .block-container {

            padding:
                15px 8px 30px 8px !important;
        }

        .calculator-box {

            padding: 16px;

            border-radius: 23px;
        }

        .header-title {

            font-size: 21px;
        }

        .header-subtitle {

            font-size: 8px;
        }

        .display-box {

            min-height: 125px;
        }

        .result-text {

            font-size: 34px;
        }

        div[data-testid="column"] {

            padding-left: 2px !important;
            padding-right: 2px !important;
        }

        div.stButton > button {

            height: 62px !important;
            min-height: 62px !important;

            font-size: 17px !important;
        }

        .scientific-button div.stButton > button {

            height: 54px !important;
            min-height: 54px !important;

            font-size: 13px !important;
        }

        .control-button div.stButton > button {

            height: 50px !important;
            min-height: 50px !important;

            font-size: 12px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CALCULATOR CONTAINER
# =========================================================

st.markdown(
    '<div class="calculator-box">',
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

header_col1, header_col2 = st.columns(
    [0.12, 0.88],
    vertical_alignment="center",
)

with header_col1:

    st.markdown("### 🧮")


with header_col2:

    st.markdown(
        '<div class="header-title">'
        'Scientific Calculator'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="header-subtitle">'
        'ADVANCED CALCULATION SYSTEM'
        '</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# DISPLAY
# =========================================================

if st.session_state.calculator_on:

    if st.session_state.expression:

        display_value = (
            st.session_state.expression
        )

    else:

        display_value = "0"

else:

    display_value = "OFF"


st.html(
    f"""
    <div class="display-box">
        <div class="result-text">
            {display_value}
        </div>
    </div>
    """
)


# =========================================================
# CONTROL BUTTONS
# =========================================================

st.markdown(
    '<div class="section-title">Controls</div>',
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(
    4,
    gap="small",
)


# ---------------------------------------------------------
# DEG
# ---------------------------------------------------------

with c1:

    if st.button(
        "DEG",
        key="degree",
        use_container_width=True,
    ):

        if st.session_state.calculator_on:
            st.session_state.mode = "DEG"


# ---------------------------------------------------------
# RAD
# ---------------------------------------------------------

with c2:

    if st.button(
        "RAD",
        key="radian",
        use_container_width=True,
    ):

        if st.session_state.calculator_on:
            st.session_state.mode = "RAD"


# ---------------------------------------------------------
# CLR
# ---------------------------------------------------------

with c3:

    if st.button(
        "CLR",
        key="clear",
        use_container_width=True,
    ):

        clear_all()


# ---------------------------------------------------------
# ON / OFF
# ---------------------------------------------------------

with c4:

    st.markdown(
        '<div class="on-button"></div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "ON / OFF",
        key="power_button",
        use_container_width=True,
    ):

        toggle_power()


# =========================================================
# SCIENTIFIC FUNCTIONS
# =========================================================

st.markdown(
    '<div class="section-title">'
    'Scientific Functions'
    '</div>',
    unsafe_allow_html=True,
)


# =========================================================
# SCIENTIFIC ROW 1
# =========================================================

with st.container():

    c1, c2, c3, c4, c5, c6 = st.columns(
        6,
        gap="small",
    )

    buttons = [
        ("2nd", "second"),
        ("sin", "sin("),
        ("cos", "cos("),
        ("tan", "tan("),
        ("π", "π"),
        ("e", "e"),
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4, c5, c6],
        buttons,
    ):

        with col:

            if st.button(
                label,
                key=f"s1_{label}",
                use_container_width=True,
            ):

                if value == "second":

                    toggle_second()

                else:

                    if (
                        st.session_state.second_function
                        and value in [
                            "sin(",
                            "cos(",
                            "tan(",
                        ]
                    ):

                        inverse = {
                            "sin(": "sin⁻¹(",
                            "cos(": "cos⁻¹(",
                            "tan(": "tan⁻¹(",
                        }

                        add_value(
                            inverse[value]
                        )

                        st.session_state.second_function = False

                    else:

                        add_value(value)


# =========================================================
# SCIENTIFIC ROW 2
# =========================================================

with st.container():

    c1, c2, c3, c4, c5, c6 = st.columns(
        6,
        gap="small",
    )

    buttons = [
        ("log", "log("),
        ("ln", "ln("),
        ("√", "sqrt("),
        ("x²", "^2"),
        ("xʸ", "^"),
        ("!", "!"),
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4, c5, c6],
        buttons,
    ):

        with col:

            if st.button(
                label,
                key=f"s2_{label}",
                use_container_width=True,
            ):

                add_value(value)


# =========================================================
# SCIENTIFIC ROW 3
# =========================================================

with st.container():

    c1, c2, c3, c4, c5, c6 = st.columns(
        6,
        gap="small",
    )

    buttons = [
        ("(", "("),
        (")", ")"),
        ("%", "%"),
        ("EXP", "e"),
        ("ANS", "Ans"),
        ("M+", "Ans"),
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4, c5, c6],
        buttons,
    ):

        with col:

            if st.button(
                label,
                key=f"s3_{label}",
                use_container_width=True,
            ):

                add_value(value)


# =========================================================
# KEYPAD
# =========================================================

st.markdown(
    '<div class="section-title">Keypad</div>',
    unsafe_allow_html=True,
)


# =========================================================
# 7 8 9 DEL AC
# =========================================================

with st.container():

    c1, c2, c3, c4, c5 = st.columns(
        5,
        gap="small",
    )


    # -----------------------------------------------------
    # 7
    # -----------------------------------------------------

    with c1:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "7",
            key="num7",
            use_container_width=True,
        ):

            add_value("7")


    # -----------------------------------------------------
    # 8
    # -----------------------------------------------------

    with c2:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "8",
            key="num8",
            use_container_width=True,
        ):

            add_value("8")


    # -----------------------------------------------------
    # 9
    # -----------------------------------------------------

    with c3:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "9",
            key="num9",
            use_container_width=True,
        ):

            add_value("9")


    # -----------------------------------------------------
    # DEL
    # -----------------------------------------------------

    with c4:

        st.markdown(
            '<div class="del-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "DEL",
            key="delete_button",
            use_container_width=True,
        ):

            delete_last()


    # -----------------------------------------------------
    # AC
    # -----------------------------------------------------

    with c5:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "AC",
            key="allclear",
            use_container_width=True,
        ):

            clear_all()


# =========================================================
# 4 5 6 × ÷
# =========================================================

with st.container():

    c1, c2, c3, c4, c5 = st.columns(
        5,
        gap="small",
    )


    with c1:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "4",
            key="num4",
            use_container_width=True,
        ):

            add_value("4")


    with c2:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "5",
            key="num5",
            use_container_width=True,
        ):

            add_value("5")


    with c3:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "6",
            key="num6",
            use_container_width=True,
        ):

            add_value("6")


    with c4:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "×",
            key="multiply",
            use_container_width=True,
        ):

            add_value("×")


    with c5:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "÷",
            key="divide",
            use_container_width=True,
        ):

            add_value("÷")


# =========================================================
# 1 2 3 + −
# =========================================================

with st.container():

    c1, c2, c3, c4, c5 = st.columns(
        5,
        gap="small",
    )


    with c1:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "1",
            key="num1",
            use_container_width=True,
        ):

            add_value("1")


    with c2:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "2",
            key="num2",
            use_container_width=True,
        ):

            add_value("2")


    with c3:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "3",
            key="num3",
            use_container_width=True,
        ):

            add_value("3")


    with c4:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "+",
            key="plus",
            use_container_width=True,
        ):

            add_value("+")


    with c5:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "−",
            key="minus",
            use_container_width=True,
        ):

            add_value("−")


# =========================================================
# 0 . EXP ANS =
# =========================================================

with st.container():

    c1, c2, c3, c4, c5 = st.columns(
        5,
        gap="small",
    )


    # -----------------------------------------------------
    # 0
    # -----------------------------------------------------

    with c1:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "0",
            key="num0",
            use_container_width=True,
        ):

            add_value("0")


    # -----------------------------------------------------
    # DECIMAL
    # -----------------------------------------------------

    with c2:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            ".",
            key="decimal",
            use_container_width=True,
        ):

            add_value(".")


    # -----------------------------------------------------
    # EXP
    # -----------------------------------------------------

    with c3:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "EXP",
            key="exp",
            use_container_width=True,
        ):

            add_value("e")


    # -----------------------------------------------------
    # ANS
    # -----------------------------------------------------

    with c4:

        st.markdown(
            '<div class="keypad-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "ANS",
            key="ans",
            use_container_width=True,
        ):

            add_value("Ans")


    # -----------------------------------------------------
    # EQUAL
    # -----------------------------------------------------

    with c5:

        st.markdown(
            '<div class="equal-button"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "=",
            key="equals",
            use_container_width=True,
        ):

            calculate()


# =========================================================
# STATUS
# =========================================================

if st.session_state.calculator_on:

    st.markdown(
        '<div class="status-bar">'
        '<span>SCIENTIFIC MODE</span>'
        '<span class="status-on">● ON</span>'
        '</div>',
        unsafe_allow_html=True,
    )

else:

    st.markdown(
        '<div class="status-bar">'
        '<span>SCIENTIFIC MODE</span>'
        '<span class="status-off">● OFF</span>'
        '</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# CLOSE CALCULATOR
# =========================================================

st.markdown(
    '</div>',
    unsafe_allow_html=True,
)
