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

    /* Page */
    .stApp {
        background:
            radial-gradient(
                circle at top,
                #292929 0%,
                #111111 45%,
                #070707 100%
            );
    }

    .block-container {
        max-width: 600px;
        padding-top: 35px;
        padding-bottom: 35px;
    }

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }


    /* Calculator */
    .calculator {
        background: #181818;
        border: 1px solid #333333;
        border-radius: 28px;
        padding: 22px;
        box-shadow:
            0 30px 70px rgba(0,0,0,.65),
            inset 0 1px 0 rgba(255,255,255,.04);
    }


    /* Header */
    .calc-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 18px;
    }

    .logo {
        width: 48px;
        height: 48px;
        border-radius: 14px;

        display: flex;
        align-items: center;
        justify-content: center;

        background: #242424;
        border: 1px solid #414141;

        font-size: 25px;
    }

    .title {
        color: white;
        font-size: 24px;
        font-weight: 700;
        line-height: 1.1;
    }

    .subtitle {
        color: #777;
        font-size: 10px;
        letter-spacing: 1.4px;
        margin-top: 4px;
    }


    /* Display */
    .display {
        height: 125px;
        box-sizing: border-box;

        background: #080808;
        border: 1px solid #303030;
        border-radius: 18px;

        padding: 15px 20px;

        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: flex-end;

        margin-bottom: 16px;

        box-shadow: inset 0 4px 16px rgba(0,0,0,.75);
    }

    .display-mode {
        width: 100%;
        color: #777;
        text-align: right;
        font-size: 10px;
        letter-spacing: 1.3px;
    }

    .display-expression {
        width: 100%;
        color: #777;
        text-align: right;
        font-size: 15px;
        min-height: 23px;
        overflow-wrap: anywhere;
    }

    .display-result {
        width: 100%;
        color: white;
        text-align: right;
        font-size: 38px;
        font-weight: 600;
        line-height: 1.15;
        overflow-wrap: anywhere;
    }


    /* All buttons */
    div.stButton {
        width: 100%;
    }

    div.stButton > button {
    width: 100%;
    height: 75px;
    border-radius: 12px;
    font-size: 22px;
    font-weight: 600;
    border: 1px solid #374151;
    transition: all 0.15s ease;
}

    div.stButton > button:hover {
    transform: translateY(-2px);
    border-color: #60a5fa;
}

    div.stButton > button:active {
    transform: translateY(1px);
}

div[data-testid="column"] {
    padding: 4px;
}


    /* Orange operators */
    div.stButton > button.operator {
        background: #e67e22 !important;
        border-color: #f39a45 !important;
        box-shadow:
            0 4px 0 #914d12,
            0 6px 10px rgba(0,0,0,.25);
    }


    /* Red AC / DEL */
    div.stButton > button.danger {
        background: #c62828 !important;
        border-color: #e14b4b !important;
        box-shadow:
            0 4px 0 #721717,
            0 6px 10px rgba(0,0,0,.25);
    }


    /* Equal */
    div.stButton > button.equals {
        background: #eeeeee !important;
        color: #111111 !important;
        border-color: white !important;
        box-shadow:
            0 4px 0 #999999,
            0 6px 10px rgba(0,0,0,.25);
    }


    /* Section */
    .section {
        color: #666;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        margin: 7px 0 8px 2px;
    }


    /* Status */
    .status {
        display: flex;
        justify-content: space-between;
        margin-top: 5px;
        padding: 0 3px;
        color: #666;
        font-size: 10px;
        letter-spacing: 1px;
    }

    .online {
        color: #6bc476;
    }


    /* Mobile */
    @media (max-width: 600px) {

        .block-container {
            padding: 15px 8px;
        }

        .calculator {
            padding: 15px;
            border-radius: 22px;
        }

        .title {
            font-size: 20px;
        }

        .logo {
            width: 42px;
            height: 42px;
        }

        .display {
            height: 110px;
        }

        .display-result {
            font-size: 30px;
        }

        div.stButton > button {
            height: 47px !important;
            font-size: 14px !important;
            border-radius: 10px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# CALCULATOR
# ---------------------------------------------------------

st.markdown('<div class="calculator">', unsafe_allow_html=True)


# ---------------------------------------------------------
# LOGO + TITLE
# ---------------------------------------------------------

st.markdown(
    """
    <div class="calc-header">

        <div class="logo">🧮</div>

        <div>
            <div class="title">Scientific Calculator</div>
            <div class="subtitle">ADVANCED CALCULATION SYSTEM</div>
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# OUTPUT SCREEN
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
# DEG / RAD / CLR / ON
# ---------------------------------------------------------

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
    if st.button("ON", key="power"):
        toggle_power()


# ---------------------------------------------------------
# SCIENTIFIC SECTION
# ---------------------------------------------------------

st.markdown(
    '<div class="section">Scientific Functions</div>',
    unsafe_allow_html=True,
)


# Scientific row 1
c1, c2, c3, c4, c5, c6 = st.columns(6)

scientific_1 = ["2nd", "sin", "cos", "tan", "π", "e"]

for col, label in zip(
    [c1, c2, c3, c4, c5, c6],
    scientific_1,
):
    with col:
        if st.button(label, key=f"sci1_{label}"):
            add_value(label)


# Scientific row 2
c1, c2, c3, c4, c5, c6 = st.columns(6)

scientific_2 = ["log", "ln", "√", "x²", "xʸ", "!"]

for col, label in zip(
    [c1, c2, c3, c4, c5, c6],
    scientific_2,
):
    with col:
        if st.button(label, key=f"sci2_{label}"):
            add_value(label)


# Scientific row 3
c1, c2, c3, c4, c5, c6 = st.columns(6)

scientific_3 = ["(", ")", "%", "EXP", "ANS", "M+"]

for col, label in zip(
    [c1, c2, c3, c4, c5, c6],
    scientific_3,
):
    with col:
        if st.button(label, key=f"sci3_{label}"):
            add_value(label)


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


# ---------------------------------------------------------
# 4 5 6 MULTIPLY DIVISION
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# 1 2 3 ADDITION SUBTRACTION
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# 0 . EXP ANS =
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# STATUS
# ---------------------------------------------------------

status = "● ON" if st.session_state.calculator_on else "● OFF"

st.markdown(
    f"""
    <div class="status">

        <span>SCIENTIFIC MODE</span>

        <span class="online">{status}</span>

    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown("</div>", unsafe_allow_html=True)
