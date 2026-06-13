import streamlit as st
import joblib

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="FinCheck",
    page_icon="💰",
    layout="centered"
)

# ---------------- LOAD MODEL ----------------

model = joblib.load("model.pkl")

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* Background */
.stApp{
    background:white;
}

/* Main title */
.main-title{
    font-size:4rem;
    font-weight:900;
    text-align:center;
    color:#16a34a;
    margin-bottom:0px;
}

/* Subtitle */
.subtitle{
    text-align:center;
    font-size:1.2rem;
    color:#64748b;
    margin-bottom:25px;
}

/* Headings */
h1,h2,h3,h4{
    color:#0f172a !important;
}

/* Labels */
label{
    color:#334155 !important;
    font-weight:600;
}

/* Inputs */
input{
    color:#0f172a !important;
}

.stNumberInput input{
    color:#0f172a !important;
}

/* Metrics */
[data-testid="stMetricLabel"]{
    color:#64748b !important;
}

[data-testid="stMetricValue"]{
    color:#16a34a !important;
    font-weight:800;
}

/* General text */
p{
    color:#334155 !important;
}

/* Buttons */
.stButton > button{
    background:#16a34a !important;
    color:white !important;
    border:none !important;
    border-radius:12px !important;
    font-weight:700 !important;
    padding:12px 24px !important;
}

.stButton > button:hover{
    background:#15803d !important;
}

/* Progress Bar */
.stProgress > div > div{
    background:#16a34a !important;
}

/* Floating Money */

.money{
    position:fixed;
    font-size:35px;
    z-index:999;
    pointer-events:none;
    animation-name:floatMoney;
    animation-timing-function:linear;
    animation-iteration-count:infinite;
}

.m1{
    left:5%;
    animation-duration:12s;
}

.m2{
    left:25%;
    animation-duration:18s;
}

.m3{
    left:45%;
    animation-duration:15s;
}

.m4{
    left:65%;
    animation-duration:20s;
}

.m5{
    left:85%;
    animation-duration:14s;
}

@keyframes floatMoney{

    from{
        top:110%;
        transform:rotate(0deg);
    }

    to{
        top:-20%;
        transform:rotate(360deg);
    }
}

</style>

<div class="money m1">💸</div>
<div class="money m2">💵</div>
<div class="money m3">💰</div>
<div class="money m4">💸</div>
<div class="money m5">💵</div>

""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="main-title">
💰 FinCheck
</div>

<div class="subtitle">
Track Finances • Build Dreams • Make Better Decisions
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- INPUTS ----------------

income = st.number_input(
    "💵 Monthly Income (₹)",
    min_value=0,
    step=1000
)

expenses = st.number_input(
    "💸 Monthly Expenses (₹)",
    min_value=0,
    step=1000
)

savings = st.number_input(
    "🏦 Current Savings (₹)",
    min_value=0,
    step=1000
)

goal_name = st.selectbox(
    "🎯 Select Your Dream",
    [
        "🎸 Guitar",
        "💻 Laptop",
        "🏍️ Bike",
        "✈️ Vacation",
        "📱 Phone",
        "🚗 Car",
        "🏠 House"
    ]
)

goal_cost = st.number_input(
    "💰 Dream Cost (₹)",
    min_value=0,
    step=1000
)

st.write("")

col1,col2,col3 = st.columns([1,1,1])

with col2:
    analyze = st.button("🚀 Analyze")

# ---------------- RESULTS ----------------

if analyze:

    features = [[
        income,
        expenses,
        savings,
        goal_cost
    ]]

    prediction = model.predict(features)[0]

    probability = (
        model.predict_proba(features)[0][1]
        * 100
    )

    surplus = income - expenses

    if surplus > 0:
        months = max(
            0,
            (goal_cost - savings) / surplus
        )
    else:
        months = -1

    if income > 0:
        score = int(
            max(
                0,
                min(
                    100,
                    (surplus / income) * 100
                )
            )
        )
    else:
        score = 0

    st.markdown("---")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric(
            "💚 Health Score",
            f"{score}/100"
        )

    with c2:
        st.metric(
            "🎯 Success Chance",
            f"{probability:.1f}%"
        )

    with c3:
        if months >= 0:
            st.metric(
                "⏳ Months Needed",
                f"{months:.1f}"
            )
        else:
            st.metric(
                "⏳ Months Needed",
                "∞"
            )

    st.markdown("### 📈 Dream Progress")

    progress = (
        savings /
        max(goal_cost,1)
    ) * 100

    st.progress(
        min(
            int(progress),
            100
        )
    )

    st.write(
        f"Progress: {min(progress,100):.1f}%"
    )

    st.markdown("---")

    if prediction == 1:

        st.success(
            f"🎉 High probability of achieving {goal_name}"
        )

    else:

        st.error(
            f"⚠️ Reaching {goal_name} may be difficult right now"
        )

    st.markdown("### 🤖 AI Recommendation")

    if probability >= 80:

        st.success(
            "Excellent financial position. Keep saving consistently."
        )

    elif probability >= 50:

        st.warning(
            "Moderate chance. Reducing expenses can help you reach your goal faster."
        )

    else:

        st.error(
            "Consider lowering expenses or increasing income to improve your chances."
        )

st.markdown("---")
st.caption("💰 FinCheck | Machine Learning Powered Financial Goal Planner")
