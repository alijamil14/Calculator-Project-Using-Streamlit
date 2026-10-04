import ast
import math
import operator

import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered",
)


# ============================================================
# SESSION STATE
# ============================================================

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


# ============================================================
# CALCULATOR FUNCTIONS
# ============================================================

def add_value(value):
    if not st.session_state.calculator_on:
        return

    st.session_state.expression += str(value)
    st.session_state.result = st.session_state.expression


def clear_all():
    st.session_state.expression = ""
    st.session_state.result = "0"


def delete_last():
    if st.session_state.expression:
        st.session_state.expression = st.session_state.expression[:-1]

    st.session_state.result = (
        st.session_state.expression
        if st.session_state.expression
        else "0"
    )


def toggle_power():
    st.session_state.calculator_on = not st.session_state.calculator_on

    if not st.session_state.calculator_on:
        st.session_state.expression = ""
        st.session_state.result = "0"


def toggle_second():
    st.session_state.second_function = (
        not st.session_state.second_function
    )


# ============================================================
# TRIGONOMETRIC FUNCTIONS
# ============================================================

def sin_func(value):
    if st.session_state.mode == "DEG":
        return math.sin(math.radians(value))

    return math.sin(value)


def cos_func(value):
    if st.session_state.mode == "DEG":
        return math.cos(math.radians(value))

    return math.cos(value)


def tan_func(value):
    if st.session_state.mode == "DEG":
        return math.tan(math.radians(value))

    return math.tan(value)


def asin_func(value):
    result = math.asin(value)

    if st.session_state.mode == "DEG":
        return math.degrees(result)

    return result


def acos_func(value):
    result = math.acos(value)

    if st.session_state.mode == "DEG":
        return math.degrees(result)

    return result


def atan_func(value):
    result = math.atan(value)

    if st.session_state.mode == "DEG":
        return math.degrees(result)

    return result


def factorial(value):
    return math.factorial(int(value))


# ============================================================
# FUNCTION MAPPING
# ============================================================

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


# ============================================================
# SAFE AST CALCULATOR
# ============================================================

def evaluate_node(node):

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Invalid value")

    if isinstance(node, ast.Num):
        return node.n

    if isinstance(node, ast.BinOp):

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
        }

        operation = operators.get(type(node.op))

        if operation is None:
            raise ValueError("Invalid operator")

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):

        value = evaluate_node(node.operand)

        if isinstance(node.op, ast.USub):
            return -value

        if isinstance(node.op, ast.UAdd):
            return +value

        raise ValueError("Invalid unary operator")

    if isinstance(node, ast.Name):

        constants = {
            "pi": math.pi,
            "e": math.e,
        }

        if node.id in constants:
            return constants[node.id]

        raise ValueError("Invalid constant")

    if isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function")

        function_name = node.func.id

        if function_name not in FUNCTIONS:
            raise ValueError("Function not allowed")

        arguments = [
            evaluate_node(argument)
            for argument in node.args
        ]

        return FUNCTIONS[function_name](*arguments)

    raise ValueError("Invalid expression")


def evaluate_expression(expression):

    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")
    expression = expression.replace("−", "-")
    expression = expression.replace("^", "**")

    expression = expression.replace("π", "pi")

    expression = expression.replace("√(", "sqrt(")

    expression = expression.replace("sin⁻¹", "asin")
    expression = expression.replace("cos⁻¹", "acos")
    expression = expression.replace("tan⁻¹", "atan")

    expression = expression.replace("%", "/100")

    tree = ast.parse(expression, mode="eval")

    return evaluate_node(tree.body)


def calculate():

    if not st.session_state.calculator_on:
        return

    expression = st.session_state.expression

    if not expression:
        return

    try:

        value = evaluate_expression(expression)

        st.session_state.answer = value

        if isinstance(value, float):
            if value.is_integer():
                value = int(value)

        st.session_state.result = str(value)
        st.session_state.expression = str(value)

    except Exception:
        st.session_state.result = "Error"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       PAGE
    ------------------------------------------------------- */

    .stApp {
        background: #eef1f5;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 30px;
        padding-bottom: 40px;
    }


    /* -------------------------------------------------------
       MAIN CALCULATOR
    ------------------------------------------------------- */

    .st-key-calculator {
        background: #ffffff;
        padding: 30px;
        border-radius: 28px;
        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.15);
        border: 1px solid #e5e7eb;
    }


    /* -------------------------------------------------------
       HEADER
    ------------------------------------------------------- */

    .calculator-header {
        text-align: center;
        margin-bottom: 24px;
    }

    .calculator-logo {
        font-size: 48px;
        margin-bottom: 5px;
    }

    .calculator-title {
        font-size: 34px;
        font-weight: 800;
        color: #111827;
        margin: 0;
    }

    .calculator-subtitle {
        color: #6b7280;
        font-size: 13px;
        letter-spacing: 3px;
        margin-top: 6px;
    }


    /* -------------------------------------------------------
       OUTPUT SCREEN
    ------------------------------------------------------- */

    .display-screen {
        background: #080b0d;
        border-radius: 18px;
        min-height: 125px;
        padding: 20px 25px;
        margin-bottom: 20px;
        border: 2px solid #20262b;
        box-shadow:
            inset 0 0 25px rgba(0, 0, 0, 0.8),
            0 8px 20px rgba(0, 0, 0, 0.15);
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: right;
    }

    .display-expression {
        color: #8ca294;
        font-size: 16px;
        min-height: 24px;
        margin-bottom: 5px;
    }

    .display-result {
        color: #39ff72;
        font-size: 40px;
        font-weight: 700;
        letter-spacing: 1px;
        text-shadow:
            0 0 8px rgba(57, 255, 114, 0.8),
            0 0 20px rgba(57, 255, 114, 0.35);
        overflow-x: auto;
        white-space: nowrap;
    }


    /* -------------------------------------------------------
       GENERAL BUTTON STYLE
    ------------------------------------------------------- */

    div.stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 700;
        transition: all 0.15s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
    }


    /* -------------------------------------------------------
       CONTROL BUTTONS
    ------------------------------------------------------- */

    .st-key-deg-button div.stButton > button,
    .st-key-rad-button div.stButton > button,
    .st-key-clr-button div.stButton > button {

        background: #e5e7eb !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
    }

    .st-key-power-button div.stButton > button {

        background: #16a34a !important;
        color: white !important;
        border: 1px solid #15803d !important;
        box-shadow:
            0 4px 12px rgba(22, 163, 74, 0.3);
    }


    /* -------------------------------------------------------
       SCIENTIFIC PANEL
    ------------------------------------------------------- */

    .st-key-scientific-panel {
        background: #f8fafc;
        padding: 18px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
    }

    .st-key-scientific-panel div.stButton > button {

        background: #ffffff !important;
        color: #111827 !important;

        border: 1px solid #d1d5db !important;

        box-shadow:
            0 4px 10px rgba(0, 0, 0, 0.12);
    }

    .st-key-scientific-panel div.stButton > button:hover {

        background: #f3f4f6 !important;

        box-shadow:
            0 7px 14px rgba(0, 0, 0, 0.18);
    }


    /* -------------------------------------------------------
       KEYPAD PANEL
    ------------------------------------------------------- */

    .st-key-keypad-panel {
        background: #f8fafc;
        padding: 18px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
    }

    .st-key-keypad-panel div.stButton > button {

        background: #111111 !important;
        color: #ffffff !important;

        border: 1px solid #222222 !important;

        box-shadow:
            0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .st-key-keypad-panel div.stButton > button:hover {

        background: #242424 !important;
    }


    /* -------------------------------------------------------
       RED OPERATORS
    ------------------------------------------------------- */

    .st-key-plus-button div.stButton > button,
    .st-key-minus-button div.stButton > button,
    .st-key-multiply-button div.stButton > button,
    .st-key-divide-button div.stButton > button {

        background: #dc2626 !important;
        color: #ffffff !important;

        border: 1px solid #b91c1c !important;

        box-shadow:
            0 4px 10px rgba(220, 38, 38, 0.3);
    }

    .st-key-plus-button div.stButton > button:hover,
    .st-key-minus-button div.stButton > button:hover,
    .st-key-multiply-button div.stButton > button:hover,
    .st-key-divide-button div.stButton > button:hover {

        background: #b91c1c !important;
    }


    /* -------------------------------------------------------
       DELETE BUTTON
    ------------------------------------------------------- */

    .st-key-delete-button div.stButton > button {

        background: #dc2626 !important;
        color: #ffffff !important;

        border: 1px solid #b91c1c !important;
    }


    /* -------------------------------------------------------
       EQUAL BUTTON
    ------------------------------------------------------- */

    .st-key-equal-button div.stButton > button {

        background: #111111 !important;
        color: #39ff72 !important;

        border: 1px solid #333333 !important;
    }


    /* -------------------------------------------------------
       SECTION TITLES
    ------------------------------------------------------- */

    .panel-title {
        text-align: center;
        font-size: 18px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 15px;
    }


    /* -------------------------------------------------------
       MOBILE RESPONSIVE
    ------------------------------------------------------- */

    @media (max-width: 768px) {

        .block-container {
            padding: 15px;
        }

        .st-key-calculator {
            padding: 18px;
            border-radius: 20px;
        }

        .calculator-title {
            font-size: 27px;
        }

        .calculator-subtitle {
            font-size: 10px;
            letter-spacing: 2px;
        }

        .display-result {
            font-size: 30px;
        }

        div.stButton > button {
            min-height: 44px;
            font-size: 14px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# MAIN CALCULATOR
# ============================================================

with st.container(key="calculator"):

# ============================================================
# HEADER
# ============================================================

    st.markdown(
    """
    <div class="calculator-header">
        <div class="calculator-logo">🧮</div>

        <h1 class="calculator-title">
            Scientific Calculator
        </h1>

        <div class="calculator-subtitle">
            ADVANCED CALCULATION SYSTEM
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)



    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="display-screen">

            <div class="display-expression">
                {st.session_state.expression}
            </div>

            <div class="display-result">
                {st.session_state.result}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # CONTROL BUTTONS
    # --------------------------------------------------------

    control1, control2, control3, control4 = st.columns(
        4,
        gap="small",
    )


    with control1:

        with st.container(key="deg-button"):

            if st.button(
                "DEG",
                key="deg",
                use_container_width=True,
            ):
                st.session_state.mode = "DEG"


    with control2:

        with st.container(key="rad-button"):

            if st.button(
                "RAD",
                key="rad",
                use_container_width=True,
            ):
                st.session_state.mode = "RAD"


    with control3:

        with st.container(key="clr-button"):

            if st.button(
                "CLR",
                key="clr",
                use_container_width=True,
            ):
                clear_all()


    with control4:

        with st.container(key="power-button"):

            if st.button(
                "ON / OFF",
                key="power",
                use_container_width=True,
            ):
                toggle_power()


    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)


    # ========================================================
    # TWO COLUMN CALCULATOR
    # ========================================================

    left_column, right_column = st.columns(
        [1, 1],
        gap="medium",
    )


    # ========================================================
    # SCIENTIFIC BUTTONS
    # ========================================================

    with left_column:

        with st.container(key="scientific-panel"):

            st.markdown(
                '<div class="panel-title">Scientific Functions</div>',
                unsafe_allow_html=True,
            )


            # ROW 1
            col1, col2, col3 = st.columns(3, gap="small")

            with col1:
                if st.button(
                    "2nd",
                    key="scientific_second",
                    use_container_width=True,
                ):
                    toggle_second()

            with col2:
                if st.button(
                    "sin",
                    key="scientific_sin",
                    use_container_width=True,
                ):
                    add_value(
                        "sin⁻¹("
                        if st.session_state.second_function
                        else "sin("
                    )

            with col3:
                if st.button(
                    "cos",
                    key="scientific_cos",
                    use_container_width=True,
                ):
                    add_value(
                        "cos⁻¹("
                        if st.session_state.second_function
                        else "cos("
                    )


            # ROW 2
            col1, col2, col3 = st.columns(3, gap="small")

            with col1:
                if st.button(
                    "tan",
                    key="scientific_tan",
                    use_container_width=True,
                ):
                    add_value(
                        "tan⁻¹("
                        if st.session_state.second_function
                        else "tan("
                    )

            with col2:
                if st.button(
                    "π",
                    key="scientific_pi",
                    use_container_width=True,
                ):
                    add_value("π")

            with col3:
                if st.button(
                    "e",
                    key="scientific_e",
                    use_container_width=True,
                ):
                    add_value("e")


            # ROW 3
            col1, col2, col3 = st.columns(3, gap="small")

            with col1:
                if st.button(
                    "log",
                    key="scientific_log",
                    use_container_width=True,
                ):
                    add_value("log(")

            with col2:
                if st.button(
                    "ln",
                    key="scientific_ln",
                    use_container_width=True,
                ):
                    add_value("ln(")

            with col3:
                if st.button(
                    "√",
                    key="scientific_sqrt",
                    use_container_width=True,
                ):
                    add_value("√(")


            # ROW 4
            col1, col2, col3 = st.columns(3, gap="small")

            with col1:
                if st.button(
                    "x²",
                    key="scientific_square",
                    use_container_width=True,
                ):
                    add_value("^2")

            with col2:
                if st.button(
                    "xʸ",
                    key="scientific_power",
                    use_container_width=True,
                ):
                    add_value("^")

            with col3:
                if st.button(
                    "!",
                    key="scientific_factorial",
                    use_container_width=True,
                ):
                    add_value("!")


            # ROW 5
            col1, col2, col3 = st.columns(3, gap="small")

            with col1:
                if st.button(
                    "(",
                    key="scientific_open",
                    use_container_width=True,
                ):
                    add_value("(")

            with col2:
                if st.button(
                    ")",
                    key="scientific_close",
                    use_container_width=True,
                ):
                    add_value(")")

            with col3:
                if st.button(
                    "%",
                    key="scientific_percent",
                    use_container_width=True,
                ):
                    add_value("%")


            # ROW 6
            col1, col2, col3 = st.columns(3, gap="small")

            with col1:
                if st.button(
                    "EXP",
                    key="scientific_exp",
                    use_container_width=True,
                ):
                    add_value("e")

            with col2:
                if st.button(
                    "ANS",
                    key="scientific_ans",
                    use_container_width=True,
                ):
                    add_value(st.session_state.answer)

            with col3:
                if st.button(
                    "M+",
                    key="scientific_memory",
                    use_container_width=True,
                ):
                    pass


    # ========================================================
    # KEYPAD
    # ========================================================

    with right_column:

        with st.container(key="keypad-panel"):

            st.markdown(
                '<div class="panel-title">Keypad</div>',
                unsafe_allow_html=True,
            )


            # ROW 1
            col1, col2, col3, col4 = st.columns(
                4,
                gap="small",
            )

            with col1:
                if st.button(
                    "7",
                    key="keypad_7",
                    use_container_width=True,
                ):
                    add_value("7")

            with col2:
                if st.button(
                    "8",
                    key="keypad_8",
                    use_container_width=True,
                ):
                    add_value("8")

            with col3:
                if st.button(
                    "9",
                    key="keypad_9",
                    use_container_width=True,
                ):
                    add_value("9")

            with col4:

                with st.container(key="delete-button"):

                    if st.button(
                        "DEL",
                        key="delete",
                        use_container_width=True,
                    ):
                        delete_last()


            # ROW 2
            col1, col2, col3, col4 = st.columns(
                4,
                gap="small",
            )

            with col1:
                if st.button(
                    "4",
                    key="keypad_4",
                    use_container_width=True,
                ):
                    add_value("4")

            with col2:
                if st.button(
                    "5",
                    key="keypad_5",
                    use_container_width=True,
                ):
                    add_value("5")

            with col3:
                if st.button(
                    "6",
                    key="keypad_6",
                    use_container_width=True,
                ):
                    add_value("6")

            with col4:

                with st.container(key="divide-button"):

                    if st.button(
                        "÷",
                        key="divide",
                        use_container_width=True,
                    ):
                        add_value("÷")


            # ROW 3
            col1, col2, col3, col4 = st.columns(
                4,
                gap="small",
            )

            with col1:
                if st.button(
                    "1",
                    key="keypad_1",
                    use_container_width=True,
                ):
                    add_value("1")

            with col2:
                if st.button(
                    "2",
                    key="keypad_2",
                    use_container_width=True,
                ):
                    add_value("2")

            with col3:
                if st.button(
                    "3",
                    key="keypad_3",
                    use_container_width=True,
                ):
                    add_value("3")

            with col4:

                with st.container(key="multiply-button"):

                    if st.button(
                        "×",
                        key="multiply",
                        use_container_width=True,
                    ):
                        add_value("×")


            # ROW 4
            col1, col2, col3, col4 = st.columns(
                4,
                gap="small",
            )

            with col1:
                if st.button(
                    "0",
                    key="keypad_0",
                    use_container_width=True,
                ):
                    add_value("0")

            with col2:
                if st.button(
                    ".",
                    key="keypad_decimal",
                    use_container_width=True,
                ):
                    add_value(".")


            with col3:

                with st.container(key="equal-button"):

                    if st.button(
                        "=",
                        key="equal",
                        use_container_width=True,
                    ):
                        calculate()


            with col4:

                if st.button(
                    "AC",
                    key="keypad_ac",
                    use_container_width=True,
                ):
                    clear_all()


            # ROW 5
            col1, col2, col3, col4 = st.columns(
                4,
                gap="small",
            )

            with col1:

                with st.container(key="plus-button"):

                    if st.button(
                        "+",
                        key="plus",
                        use_container_width=True,
                    ):
                        add_value("+")


            with col2:

                with st.container(key="minus-button"):

                    if st.button(
                        "−",
                        key="minus",
                        use_container_width=True,
                    ):
                        add_value("−")


            with col3:
                if st.button(
                    "(",
                    key="keypad_open",
                    use_container_width=True,
                ):
                    add_value("(")


            with col4:
                if st.button(
                    ")",
                    key="keypad_close",
                    use_container_width=True,
                ):
                    add_value(")")


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#9ca3af;
            font-size:12px;
            margin-top:20px;
        ">
            Scientific Calculator • Python + Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )

