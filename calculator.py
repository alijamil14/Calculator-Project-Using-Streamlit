import streamlit as st

st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered",
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "expression" not in st.session_state:
    st.session_state.expression = ""

if "result" not in st.session_state:
    st.session_state.result = "0"

if "mode" not in st.session_state:
    st.session_state.mode = "DEG"

if "calculator_on" not in st.session_state:
    st.session_state.calculator_on = True


# ---------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------

def add_value(value):
    if st.session_state.calculator_on:
        st.session_state.expression += value


def clear_all():
    st.session_state.expression = ""
    st.session_state.result = "0"


def delete_last():
    if st.session_state.calculator_on:
        st.session_state.expression = st.session_state.expression[:-1]


def calculate():
    # UI stage only.
    # Scientific calculation logic can be added later.
    if st.session_state.expression:
        st.session_state.result = st.session_state.expression


def toggle_power():
    st.session_state.calculator_on = not st.session_state.calculator_on

    if not st.session_state.calculator_on:
        st.session_state.expression = ""
        st.session_state.result = ""


# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* =====================================================
       PAGE
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 20% 0%,
                #292929 0%,
                #111111 48%,
                #070707 100%
            );
    }

    .block-container {
        max-width: 760px !important;
        padding-top: 35px !important;
        padding-bottom: 35px !important;
    }

    #MainMenu,
    header,
    footer {
        visibility: hidden;
    }


    /* =====================================================
       CALCULATOR BODY
       ===================================================== */

    .calculator {
        width: 100%;
        box-sizing: border-box;

        background: #181818;

        border: 1px solid #333333;
        border-radius: 30px;

        padding: 28px;

        box-shadow:
            0 30px 80px rgba(0, 0, 0, 0.75),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }


    /* =====================================================
       HEADER
       ===================================================== */

    .calc-header {
        display: flex;
        align-items: center;
        gap: 15px;

        margin-bottom: 22px;
    }

    .logo {
        width: 58px;
        height: 58px;

        flex-shrink: 0;

        display: flex;
        align-items: center;
        justify-content: center;

        background: #242424;

        border: 1px solid #414141;
        border-radius: 16px;

        font-size: 30px;

        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.04);
    }

    .title {
        color: #ffffff;

        font-size: 28px;
        font-weight: 700;

        line-height: 1.1;
    }

    .subtitle {
        color: #777777;

        font-size: 11px;
        letter-spacing: 2px;

        margin-top: 6px;
    }


    /* =====================================================
       DISPLAY
       ===================================================== */

    .display {
        min-height: 155px;

        box-sizing: border-box;

        background: #080808;

        border: 1px solid #303030;
        border-radius: 20px;

        padding: 18px 22px;

        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: flex-end;

        margin-bottom: 20px;

        box-shadow:
            inset 0 5px 20px rgba(0, 0, 0, 0.85),
            0 1px 0 rgba(255, 255, 255, 0.02);
    }

    .display-mode {
        width: 100%;

        color: #777777;

        text-align: right;

        font-size: 11px;
        font-weight: 600;

        letter-spacing: 1.5px;
    }

    .display-expression {
        width: 100%;

        color: #777777;

        text-align: right;

        font-size: 18px;

        min-height: 27px;

        overflow-wrap: anywhere;
    }

    .display-result {
        width: 100%;

        color: #ffffff;

        text-align: right;

        font-size: 46px;
        font-weight: 600;

        line-height: 1.15;

        overflow-wrap: anywhere;
    }


    /* =====================================================
       SECTION LABEL
       ===================================================== */

    .section {
        color: #666666;

        font-size: 10px;
        font-weight: 700;

        letter-spacing: 2px;

        text-transform: uppercase;

        margin: 14px 0 10px 3px;
    }


    /* =====================================================
       STREAMLIT COLUMNS
       ===================================================== */

    div[data-testid="column"] {
    padding-left: 2px !important;
    padding-right: 2px !important;
}


    /* =====================================================
       ALL BUTTONS
       ===================================================== */

    div.stButton {
       width: 100% !important;
    margin: 0 !important;
    }

    div.stButton > button {
        width: 100% !important;
    min-width: 100% !important;

    height: 68px !important;
    min-height: 68px !important;

    padding: 0 !important;

    border-radius: 14px !important;

    font-size: 19px !important;
    font-weight: 600 !important;

    box-sizing: border-box !important;

        box-shadow:
            0 4px 0 #111111,
            0 7px 12px rgba(0, 0, 0, 0.30);

        transition:
            transform 0.12s ease,
            background 0.12s ease,
            border-color 0.12s ease,
            box-shadow 0.12s ease;
    }

    /* Hover */

    div.stButton > button:hover {
        background: #303030 !important;

        border-color: #5a5a5a !important;

        color: #ffffff !important;

        transform: translateY(-2px);

        box-shadow:
            0 6px 0 #111111,
            0 10px 18px rgba(0, 0, 0, 0.35);
    }

    /* Press */

    div.stButton > button:active {
        transform: translateY(3px) !important;

        box-shadow:
            0 1px 0 #111111,
            0 3px 6px rgba(0, 0, 0, 0.30);
    }


    /* =====================================================
       TOP CONTROL BUTTONS
       ===================================================== */

    .control-row div.stButton > button {
        min-height: 58px !important;
        height: 58px !important;

        font-size: 15px !important;

        background: #202020 !important;
    }


    /* =====================================================
       SCIENTIFIC BUTTONS
       ===================================================== */

    .scientific-row div.stButton > button {
        min-height: 62px !important;
        height: 62px !important;

        font-size: 16px !important;

        background: #202020 !important;
    }


    /* =====================================================
       ORANGE OPERATORS
       We target buttons by their position instead of
       nonexistent custom button classes.
       ===================================================== */

    .operator-row div.stButton:nth-child(4) > button,
    .operator-row div.stButton:nth-child(5) > button {
        background: #e67e22 !important;

        border-color: #f39a45 !important;

        color: #ffffff !important;

        box-shadow:
            0 4px 0 #914d12,
            0 7px 12px rgba(0, 0, 0, 0.30);
    }

    .operator-row div.stButton:nth-child(4) > button:hover,
    .operator-row div.stButton:nth-child(5) > button:hover {
        background: #f08b2d !important;

        border-color: #ffad62 !important;
    }


    /* =====================================================
       DANGER BUTTONS
       ===================================================== */

    .danger-row div.stButton:nth-child(4) > button,
    .danger-row div.stButton:nth-child(5) > button {
        background: #c62828 !important;

        border-color: #e14b4b !important;

        color: #ffffff !important;

        box-shadow:
            0 4px 0 #721717,
            0 7px 12px rgba(0, 0, 0, 0.30);
    }

    .danger-row div.stButton:nth-child(4) > button:hover,
    .danger-row div.stButton:nth-child(5) > button:hover {
        background: #d93636 !important;

        border-color: #f05b5b !important;
    }


    /* =====================================================
       EQUAL BUTTON
       ===================================================== */

    .equals-row div.stButton:nth-child(5) > button {
        background: #eeeeee !important;

        color: #111111 !important;

        border-color: #ffffff !important;

        box-shadow:
            0 4px 0 #999999,
            0 7px 12px rgba(0, 0, 0, 0.30);
    }

    .equals-row div.stButton:nth-child(5) > button:hover {
        background: #ffffff !important;

        color: #000000 !important;
    }


    /* =====================================================
       STATUS
       ===================================================== */

    .status {
        display: flex;
        justify-content: space-between;

        margin-top: 14px;

        padding: 0 4px;

        color: #666666;

        font-size: 10px;

        letter-spacing: 1px;
    }

    .online {
        color: #6bc476;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 600px) {

        .block-container {
            padding: 15px 7px !important;
        }

        .calculator {
            padding: 22px;

            border-radius: 23px;
        }

        .calc-header {
            gap: 11px;
        }

        .logo {
            width: 46px;
            height: 46px;

            border-radius: 13px;

            font-size: 24px;
        }

        .title {
            font-size: 21px;
        }

        .subtitle {
            font-size: 8px;
            letter-spacing: 1.3px;
        }

        .display {
            min-height: 125px;

            padding: 15px 16px;

            border-radius: 16px;
        }

        .display-result {
            font-size: 34px;
        }

        div[data-testid="column"] {
            padding-left: 2px !important;
            padding-right: 2px !important;
        }

        div.stButton > button {
            min-height: 60px !important;
            height: 60px !important;

            font-size: 17px !important;

            border-radius: 11px !important;
        }

        .control-row div.stButton > button {
            min-height: 52px !important;
            height: 52px !important;

            font-size: 13px !important;
        }

        .scientific-row div.stButton > button {
            min-height: 55px !important;
            height: 55px !important;

            font-size: 14px !important;
        }
    }


    /* =====================================================
       VERY SMALL SCREENS
       ===================================================== */

    @media (max-width: 400px) {

        .calculator {
            padding: 12px;
        }

        div.stButton > button {
            min-height: 54px !important;
            height: 54px !important;

            font-size: 15px !important;
        }

        .scientific-row div.stButton > button {
            min-height: 50px !important;
            height: 50px !important;

            font-size: 12px !important;
        }

        .display-result {
            font-size: 29px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# CALCULATOR CONTAINER
# ---------------------------------------------------------

st.markdown(
    '<div class="calculator">',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# LOGO + TITLE
# ---------------------------------------------------------

st.markdown(
    """
    <div class="calc-header">

        <div class="logo">🧮</div>

        <div>
            <div class="title">
                Scientific Calculator
            </div>

            <div class="subtitle">
                ADVANCED CALCULATION SYSTEM
            </div>
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------

if st.session_state.calculator_on:

    mode_text = f"{st.session_state.mode} MODE"

    expression = st.session_state.expression

    result = st.session_state.result or "0"

else:

    mode_text = "POWER OFF"

    expression = ""

    result = "OFF"


st.markdown(
    f"""
    <div class="display">

        <div class="display-mode">
            {mode_text}
        </div>

        <div class="display-expression">
            {expression}
        </div>

        <div class="display-result">
            {result}
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# CONTROL ROW
# ---------------------------------------------------------

st.markdown(
    '<div class="control-row">',
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("DEG", key="deg"):
        st.session_state.mode = "DEG"

with c2:
    if st.button("RAD", key="rad"):
        st.session_state.mode = "RAD"

with c3:
    if st.button("CLR", key="clr"):
        clear_all()

with c4:
    if st.button(
        "ON" if not st.session_state.calculator_on else "OFF",
        key="power",
    ):
        toggle_power()

st.markdown(
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SCIENTIFIC FUNCTIONS
# ---------------------------------------------------------

st.markdown(
    '<div class="section">Scientific Functions</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SCIENTIFIC ROW 1
# ---------------------------------------------------------

st.markdown(
    '<div class="scientific-row">',
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5, c6 = st.columns(6)

scientific_1 = [
    "2nd",
    "sin",
    "cos",
    "tan",
    "π",
    "e",
]

for col, label in zip(
    [c1, c2, c3, c4, c5, c6],
    scientific_1,
):
    with col:
        if st.button(
            label,
            key=f"sci1_{label}",
        ):
            add_value(label)

st.markdown(
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SCIENTIFIC ROW 2
# ---------------------------------------------------------

st.markdown(
    '<div class="scientific-row">',
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5, c6 = st.columns(6)

scientific_2 = [
    "log",
    "ln",
    "√",
    "x²",
    "xʸ",
    "!",
]

for col, label in zip(
    [c1, c2, c3, c4, c5, c6],
    scientific_2,
):
    with col:
        if st.button(
            label,
            key=f"sci2_{label}",
        ):
            add_value(label)

st.markdown(
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SCIENTIFIC ROW 3
# ---------------------------------------------------------

st.markdown(
    '<div class="scientific-row">',
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5, c6 = st.columns(6)

scientific_3 = [
    "(",
    ")",
    "%",
    "EXP",
    "ANS",
    "M+",
]

for col, label in zip(
    [c1, c2, c3, c4, c5, c6],
    scientific_3,
):
    with col:
        if st.button(
            label,
            key=f"sci3_{label}",
        ):
            add_value(label)

st.markdown(
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# KEYPAD
# ---------------------------------------------------------

st.markdown(
    '<div class="section">Keypad</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# 7 8 9 DEL AC
# ---------------------------------------------------------

st.markdown(
    '<div class="danger-row">',
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    if st.button("7", key="7"):
        add_value("7")

with c2:
    if st.button("8", key="8"):
        add_value("8")

with c3:
    if st.button("9", key="9"):
        add_value("9")

with c4:
    if st.button("DEL", key="del"):
        delete_last()

with c5:
    if st.button("AC", key="ac"):
        clear_all()

st.markdown(
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# 4 5 6 × ÷
# ---------------------------------------------------------

st.markdown(
    '<div class="operator-row">',
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    if st.button("4", key="4"):
        add_value("4")

with c2:
    if st.button("5", key="5"):
        add_value("5")

with c3:
    if st.button("6", key="6"):
        add_value("6")

with c4:
    if st.button("×", key="multiply"):
        add_value("×")

with c5:
    if st.button("÷", key="division"):
        add_value("÷")

st.markdown(
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# 1 2 3 + −
# ---------------------------------------------------------

st.markdown(
    '<div class="operator-row">',
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    if st.button("1", key="1"):
        add_value("1")

with c2:
    if st.button("2", key="2"):
        add_value("2")

with c3:
    if st.button("3", key="3"):
        add_value("3")

with c4:
    if st.button("+", key="addition"):
        add_value("+")

with c5:
    if st.button("−", key="subtraction"):
        add_value("−")

st.markdown(
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# 0 . EXP ANS =
# ---------------------------------------------------------

st.markdown(
    '<div class="equals-row">',
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    if st.button("0", key="zero"):
        add_value("0")

with c2:
    if st.button(".", key="decimal"):
        add_value(".")

with c3:
    if st.button("EXP", key="exp"):
        add_value("EXP")

with c4:
    if st.button("ANS", key="ans"):
        add_value("ANS")

with c5:
    if st.button("=", key="equals"):
        calculate()

st.markdown(
    '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# STATUS
# ---------------------------------------------------------

status = (
    "● ON"
    if st.session_state.calculator_on
    else "● OFF"
)

st.markdown(
    f"""
    <div class="status">

        <span>SCIENTIFIC MODE</span>

        <span class="online">
            {status}
        </span>

    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# CLOSE CALCULATOR
# ---------------------------------------------------------

st.markdown(
    '</div>',
    unsafe_allow_html=True,
)