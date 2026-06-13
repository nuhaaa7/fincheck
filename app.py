import streamlit as st
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FinCheck AI",
    page_icon="💰",
    layout="centered"
)

# ---------------- LOAD MODEL ----------------
model = joblib.load("model.pkl")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* White Background */
.stApp{
    background:white;
}

/* Center Layout */
.block-container{
    max-width:900px;
    text-align:center;
}

/* Title */
.main-title{
    font-size:4rem;
    font-weight:900;
    color:#16a34a;
    margin-bottom:0px;
}

.subtitle{
    font-size:1.2rem;
    color:#666;
    margin-bottom:30px;
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
    left:20%;
    animation-duration:18s;
}

.m3{
    left:40%;
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

/* Card */
.card{
    background:#f8f8f8;
    padding:20px;
    border-radius:20px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.1);
}

/* Hide Streamlit Footer */
footer{
    visibility:hidden;
}

</style>

<div class="money m1">💸</div>
<div class="money m2">💵</div>
<div class="money m3">💰</div>
<div class="money m4">💸</div>
<div class="money m5">💵</div>

""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown(
"""
<div class="main-title">
💰 FinCheck AI
</div>
<div class="subtitle">
Turn Dreams Into Plans
</div>
""",
unsafe_allow_html=True
)

st.markdown("---")

# ---------------- INPUTS ----------------

income = st.number_input(
    "💵 Monthly Income (₹)",
    min_value=0
)

expenses = st.number_input(
    "💸 Monthly Expenses (₹)",
    min_value=0
)

savings = st.number_input(
    "🏦 Current Savings (₹)",
    min_value=0
)

goal_name = st.selectbox(
    "🎯 Select Your Dream",
    [
        "🎸 Guitar",
        "💻 Laptop",
        "🏍️ Bike",
        "✈️ Vacation",
        "📱 Phone",
        "🏠 House",
        "🚗 Car"
    ]
)

goal_cost = st.number_input(
    "💰 Goal Cost (₹)",
    min_value=0
)

st.write("")

# Center Button
col1, col2, col3 = st.columns([1,1,1])

with col2:
    analyze = st.button("🚀 Analyze")

# ---------------- ANALYSIS ----------------

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

    # Metrics

    c1, c2, c3 = st.columns(3)

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

    # Prediction

    if prediction == 1:

        st.success(
            f"🎉 FinCheck predicts a HIGH chance of achieving {goal_name}"
        )

    else:

        st.error(
            f"⚠️ FinCheck predicts difficulty achieving {goal_name}"
        )

    # Advice

    st.markdown("### 🤖 AI Recommendation")

    if probability >= 80:

        st.success(
            "Excellent! Continue your current savings strategy."
        )

    elif probability >= 50:

        st.warning(
            "You are on track, but reducing expenses could help reach your goal faster."
        )

    else:

        st.error(
            "Consider lowering expenses or increasing income to improve your chances."
        )

st.markdown("---")
st.caption("Built with ❤️ using Streamlit & Machine Learning")
