import ast
import math
import operator
import re
from html import escape

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
    st.session_state.result = ""

if "mode" not in st.session_state:
    st.session_state.mode = "DEG"

if "calculator_on" not in st.session_state:
    st.session_state.calculator_on = True

if "answer" not in st.session_state:
    st.session_state.answer = 0

if "memory" not in st.session_state:
    st.session_state.memory = 0

if "second_function" not in st.session_state:
    st.session_state.second_function = False


# ============================================================
# CALCULATOR FUNCTIONS
# ============================================================

def add_value(value):
    """Append a calculator key to the current expression."""
    if not st.session_state.calculator_on:
        return

    # Start a fresh expression after a completed calculation when a new
    # number or function is entered; operators continue from the answer.
    value = str(value)
    if st.session_state.result == "Error":
        st.session_state.expression = ""
        st.session_state.result = ""

    if st.session_state.expression and st.session_state.expression == format_number(st.session_state.answer):
        if value in "0123456789." or value in ("π", "e", "sin(", "cos(", "tan(", "sin⁻¹(", "cos⁻¹(", "tan⁻¹(", "log(", "ln(", "√(", "("):
            st.session_state.expression = ""

    st.session_state.expression += value
    st.session_state.result = st.session_state.expression


def clear_all():
    st.session_state.expression = ""
    st.session_state.result = ""


def delete_last():
    if st.session_state.expression:
        st.session_state.expression = st.session_state.expression[:-1]
    st.session_state.result = st.session_state.expression


def toggle_power():
    st.session_state.calculator_on = not st.session_state.calculator_on
    if not st.session_state.calculator_on:
        st.session_state.expression = ""
        st.session_state.result = ""


def toggle_second():
    st.session_state.second_function = not st.session_state.second_function


def current_numeric_value():
    """Return the current expression/result as a number, or last answer."""
    text = st.session_state.expression.strip()
    if text:
        return evaluate_expression(text)
    return float(st.session_state.answer)


def memory_add():
    if not st.session_state.calculator_on:
        return
    try:
        st.session_state.memory += current_numeric_value()
        st.session_state.result = f"M = {format_number(st.session_state.memory)}"
    except Exception:
        st.session_state.result = "Enter a valid value first"


def memory_recall():
    if st.session_state.calculator_on:
        st.session_state.expression = ""
        st.session_state.result = ""
        add_value(format_number(st.session_state.memory))


def memory_clear():
    st.session_state.memory = 0
    st.session_state.result = "Memory cleared"


def format_number(value):
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("Result is not finite")
        if value.is_integer():
            return str(int(value))
        return format(value, ".12g")
    return str(value)


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
    if not math.isfinite(float(value)) or float(value) < 0 or not float(value).is_integer():
        raise ValueError("Factorial requires a non-negative integer")
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
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise ValueError("Invalid value")

    # Compatibility with Python versions where numeric literals use ast.Num.
    if isinstance(node, ast.Num):
        return node.n

    if isinstance(node, ast.BinOp):
        left = evaluate_node(node.left)
        right = evaluate_node(node.right)
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
        }
        operation = allowed_operators.get(type(node.op))
        if operation is None:
            raise ValueError("Invalid operator")
        result = operation(left, right)
        if isinstance(result, complex):
            raise ValueError("Complex results are not supported")
        if isinstance(result, float) and not math.isfinite(result):
            raise ValueError("Result is outside the supported range")
        return result

    if isinstance(node, ast.UnaryOp):
        value = evaluate_node(node.operand)
        if isinstance(node.op, ast.USub):
            return -value
        if isinstance(node.op, ast.UAdd):
            return +value
        raise ValueError("Invalid unary operator")

    if isinstance(node, ast.Name):
        constants = {"pi": math.pi, "e": math.e}
        if node.id in constants:
            return constants[node.id]
        raise ValueError("Invalid constant")

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function")
        function_name = node.func.id
        if function_name not in FUNCTIONS or node.keywords:
            raise ValueError("Function not allowed")
        arguments = [evaluate_node(argument) for argument in node.args]
        return FUNCTIONS[function_name](*arguments)

    raise ValueError("Invalid expression")


def convert_factorials(expression):
    """Convert postfix factorials (5!, (2+3)!) into safe factorial(...) calls."""
    while "!" in expression:
        bang = expression.find("!")
        end = bang - 1
        while end >= 0 and expression[end].isspace():
            end -= 1
        if end < 0:
            raise ValueError("Missing factorial operand")

        if expression[end] == ")":
            depth = 1
            start = end - 1
            while start >= 0 and depth:
                if expression[start] == ")":
                    depth += 1
                elif expression[start] == "(":
                    depth -= 1
                start -= 1
            if depth:
                raise ValueError("Unmatched parentheses")
            start += 1
            # Include a function name before the opening parenthesis, e.g. sin(30)!
            name_end = start - 1
            name_start = name_end
            while name_start >= 0 and (expression[name_start].isalnum() or expression[name_start] == "_"):
                name_start -= 1
            if name_start + 1 <= name_end and expression[name_start + 1:name_end + 1] in FUNCTIONS:
                start = name_start + 1
        elif expression[end].isdigit() or expression[end] == ".":
            start = end
            while start >= 0 and (expression[start].isdigit() or expression[start] == "."):
                start -= 1
            start += 1
        else:
            raise ValueError("Invalid factorial operand")

        operand = expression[start:end + 1].strip()
        expression = expression[:start] + f"factorial({operand})" + expression[bang + 1:]
    return expression


def evaluate_expression(expression):
    expression = expression.strip()
    if not expression:
        raise ValueError("Enter an expression")

    expression = expression.replace("×", "*").replace("÷", "/").replace("−", "-")
    expression = expression.replace("π", "pi").replace("√(", "sqrt(")
    expression = expression.replace("sin⁻¹", "asin").replace("cos⁻¹", "acos").replace("tan⁻¹", "atan")
    expression = expression.replace("^", "**")
    expression = convert_factorials(expression)

    # Percent is a postfix percentage key: 25% becomes 25/100.
    expression = re.sub(r"(?<=[0-9.)])%", "/100", expression)
    if "%" in expression:
        raise ValueError("Invalid percentage")

    # Support common implicit multiplication, e.g. 2π, 2(3+4), (2+3)(4+5).
    expression = re.sub(r"(?<=[0-9)])(?=pi\b|e\b(?![+-]?\d)|\()", "*", expression)
    expression = re.sub(r"(?<=\))(?=[A-Za-z])", "*", expression)
    expression = re.sub(r"(?<=[0-9)])(?=(?:sin|cos|tan|asin|acos|atan|sqrt|log|ln)\()", "*", expression)

    tree = ast.parse(expression, mode="eval")
    value = evaluate_node(tree.body)
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Result is not finite")
    return value


def calculate():
    if not st.session_state.calculator_on:
        return
    expression = st.session_state.expression.strip()
    if not expression:
        return
    try:
        value = evaluate_expression(expression)
        st.session_state.answer = value
        st.session_state.result = format_number(value)
        st.session_state.expression = format_number(value)
    except ZeroDivisionError:
        st.session_state.result = "Cannot divide by zero"
    except (SyntaxError, ValueError, TypeError, OverflowError) as error:
        st.session_state.result = str(error) if str(error) else "Invalid expression"
    except Exception:
        st.session_state.result = "Calculation error"


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
        max-width: 790px;
        padding-top: 14px;
        padding-bottom: 18px;
    }


    /* -------------------------------------------------------
       MAIN CALCULATOR
    ------------------------------------------------------- */

    .st-key-calculator {
        background: #ffffff;
        padding: 18px;
        border-radius: 22px;
        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.15);
        border: 1px solid #e5e7eb;
    }


    /* -------------------------------------------------------
       HEADER
    ------------------------------------------------------- */

    .calculator-header {
        text-align: center;
        margin-bottom: 14px;
    }

    .calculator-logo {
        font-size: 34px;
        margin-bottom: 5px;
    }

    .calculator-title {
        font-size: 23px;
        font-weight: 800;
        color: #111827;
        margin: 0;
    }

    .calculator-subtitle {
        color: #6b7280;
        font-size: 11px;
        letter-spacing: 2px;
        margin-top: 6px;
    }


    /* -------------------------------------------------------
       OUTPUT SCREEN
    ------------------------------------------------------- */

    .display-screen {
        background: #080b0d;
        border-radius: 18px;
        min-height: 88px;
        padding: 13px 18px;
        margin-bottom: 12px;
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
        font-size: 13px;
        min-height: 18px;
        margin-bottom: 5px;
    }

    .display-result {
        color: #39ff72;
        font-size: 31px;
        font-weight: 700;
        letter-spacing: 1px;
        text-shadow:
            0 0 8px rgba(57, 255, 114, 0.8),
            0 0 20px rgba(57, 255, 114, 0.35);
        overflow-x: auto;
        white-space: nowrap;
    }

    .display-expression, .display-result {
        overflow-wrap: anywhere;
    }

    /* -------------------------------------------------------
       GENERAL BUTTON STYLE
    ------------------------------------------------------- */

    div.stButton > button {
        width: 100%;
        min-height: 40px;
        border-radius: 10px;
        font-size: 14px;
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
        padding: 12px;
        border-radius: 14px;
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
        padding: 12px;
        border-radius: 14px;
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
        font-size: 15px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 15px;
    }


    /* -------------------------------------------------------
       MOBILE RESPONSIVE
    ------------------------------------------------------- */

    @media (max-width: 768px) {

        .block-container {
            padding: 10px;
        }

        .st-key-calculator {
            padding: 12px;
            border-radius: 16px;
        }

        .calculator-title {
            font-size: 23px;
        }

        .calculator-subtitle {
            font-size: 10px;
            letter-spacing: 2px;
        }

        .display-result {
            font-size: 26px;
        }

        div.stButton > button {
            min-height: 40px;
            font-size: 13px;
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

    st.html(
    """
    <div class="calculator-header">
        <div class="calculator-logo">🧮  Ali Jamil</div>

        <h1 class="calculator-title">
            Scientific Calculator
        </h1>

        <div class="calculator-subtitle">
            ADVANCED CALCULATION SYSTEM
        </div>
    </div>
    """
)



    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    st.html(
        f"""
        <div class="display-screen">

            <div class="display-expression">
                {escape(str(st.session_state.expression))}
            </div>

            <div class="display-result">
                {escape(str(st.session_state.result))}
            </div>

        </div>
        """
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


    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)


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
                    "2nd ✓" if st.session_state.second_function else "2nd",
                    key="scientific_second",
                    use_container_width=True,
                ):
                    toggle_second()

            with col2:
                if st.button(
                    "sin⁻¹" if st.session_state.second_function else "sin",
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
                    "cos⁻¹" if st.session_state.second_function else "cos",
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
                    "tan⁻¹" if st.session_state.second_function else "tan",
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
                    add_value("×10^")

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
                    memory_add()

            # ROW 7 — memory recall and reset
            col1, col2, col3 = st.columns(3, gap="small")
            with col1:
                if st.button("MR", key="scientific_memory_recall", use_container_width=True):
                    memory_recall()
            with col2:
                if st.button("MC", key="scientific_memory_clear", use_container_width=True):
                    memory_clear()
            with col3:
                st.caption("Memory")


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



# ============================================================
# PHYSICAL KEYBOARD SUPPORT
# ============================================================

st.html(
    """
    <script>
    (() => {
        // Prevent duplicate keyboard listeners when Streamlit reruns the app.
        if (window.__calculatorKeyboardHandlerAttached) return;
        window.__calculatorKeyboardHandlerAttached = true;

        const buttonSelectors = {
            "0": ".st-key-keypad_0 button",
            "1": ".st-key-keypad_1 button",
            "2": ".st-key-keypad_2 button",
            "3": ".st-key-keypad_3 button",
            "4": ".st-key-keypad_4 button",
            "5": ".st-key-keypad_5 button",
            "6": ".st-key-keypad_6 button",
            "7": ".st-key-keypad_7 button",
            "8": ".st-key-keypad_8 button",
            "9": ".st-key-keypad_9 button",
            ".": ".st-key-keypad_decimal button",
            "+": ".st-key-plus-button button",
            "-": ".st-key-minus-button button",
            "*": ".st-key-multiply-button button",
            "/": ".st-key-divide-button button",
            "(": ".st-key-keypad_open button",
            ")": ".st-key-keypad_close button",
            "%": ".st-key-scientific_percent button",
            "^": ".st-key-scientific_power button",
            "!": ".st-key-scientific_factorial button",
            "Enter": ".st-key-equal-button button",
            "=": ".st-key-equal-button button",
            "Backspace": ".st-key-delete-button button",
            "Escape": ".st-key-keypad_ac button",
        };

        document.addEventListener("keydown", (event) => {
            // Do not interfere with typing in any editable field.
            const target = event.target;
            if (
                target && (
                    target.isContentEditable ||
                    ["INPUT", "TEXTAREA", "SELECT"].includes(target.tagName)
                )
            ) return;

            const selector = buttonSelectors[event.key];
            if (!selector) return;

            const button = document.querySelector(selector);
            if (!button || button.disabled) return;

            event.preventDefault();
            button.click();
        });
    })();
    </script>
    """,
    unsafe_allow_javascript=True,
)
