import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="STATLAB | Statistical Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown("""
<style>
:root { --navy:#102b46; --teal:#078b88; --teal-dark:#06716f; --ink:#172b43; --muted:#64748b; }
[data-testid="stAppViewContainer"] { background:#f5f7fa; }
[data-testid="stHeader"] { background:rgba(245,247,250,.92); }
.block-container { padding-top:1.5rem; padding-bottom:3rem; max-width:1440px; }
[data-testid="stSidebar"] { background:#102b46; }
[data-testid="stSidebar"] * { color:#f4f8fc !important; }
.brand { font-size:1.65rem; font-weight:800; letter-spacing:.04em; color:#fff; }
.brand-sub { color:#cbd8e5; font-size:.82rem; margin-top:-8px; margin-bottom:1.5rem; }
.eyebrow { color:#078b88; font-size:.78rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }
.hero-title { color:#102b46; font-size:2.15rem; line-height:1.15; font-weight:800; margin:.25rem 0; }
.hero-sub { color:#64748b; font-size:1.02rem; margin-bottom:1.4rem; }
.stat-card { background:white; border:1px solid #e3e9ef; border-radius:15px; padding:18px 18px; min-height:112px; }
.stat-icon { font-size:1.35rem; }
.stat-number { color:#102b46; font-size:1.55rem; font-weight:800; margin-top:6px; }
.stat-label { color:#64748b; font-size:.88rem; }
.panel { background:white; border:1px solid #e3e9ef; border-radius:16px; padding:20px; margin:10px 0 18px; }
.panel-title { color:#102b46; font-size:1.15rem; font-weight:800; margin-bottom:12px; }
.step { color:#102b46; font-weight:700; }
.step-no { display:inline-flex; background:#102b46; color:white; width:27px; height:27px; border-radius:50%; align-items:center; justify-content:center; margin-right:7px; }
.test-card { background:white; border:1px solid #e3e9ef; border-radius:13px; padding:15px; min-height:112px; }
.test-name { color:#102b46; font-weight:800; }
.test-desc { color:#64748b; font-size:.83rem; margin-top:5px; }
.pill { display:inline-block; padding:4px 9px; background:#e5f5f3; color:#06716f; border-radius:99px; font-size:.75rem; font-weight:700; }
.note { background:#edf7f7; border-left:4px solid #078b88; border-radius:8px; padding:12px 14px; color:#23445a; }
div.stButton > button { border-radius:10px; border:1px solid #d8e2e9; font-weight:700; min-height:42px; }
div.stButton > button[kind="primary"] { background:#078b88; border-color:#078b88; color:white; }
h1,h2,h3 { color:#102b46; }
@media (max-width: 700px) {
 .block-container { padding:1rem .8rem 2rem; }
 .hero-title { font-size:1.65rem; }
 .stat-card { min-height:95px; padding:13px; }
 .panel { padding:14px; }
}
</style>
""", unsafe_allow_html=True)

# ---------- Navigation ----------
pages = [
    "Dashboard", "Descriptive Statistics", "Categorical Data",
    "Non-parametric Tests", "Parametric Tests",
    "Correlation & Regression", "Reports", "About STATLAB"
]
with st.sidebar:
    st.markdown('<div class="brand">▥ STATLAB</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Analyse · Interpret · Report</div>', unsafe_allow_html=True)
    st.markdown("---")
    selected = st.radio("NAVIGATION", pages, label_visibility="collapsed")
    st.markdown("---")
    st.caption("Research statistics, made clearer.")
    st.caption("Prototype v0.1 · UI preview")

# ---------- Reusable helpers ----------
def heading(kicker, title, subtitle=""):
    st.markdown(f'<div class="eyebrow">{kicker}</div><div class="hero-title">{title}</div><div class="hero-sub">{subtitle}</div>', unsafe_allow_html=True)

def placeholder_page(title, description, tests):
    heading("STATISTICAL WORKSPACE", title, description)
    st.markdown('<div class="note">This section is part of the first UI build. The calculation engine will be connected in a later step; no statistical result is being calculated yet.</div>', unsafe_allow_html=True)
    st.subheader("Available test interfaces")
    cols = st.columns(2)
    for i, (name, desc) in enumerate(tests):
        with cols[i % 2]:
            st.markdown(f'<div class="test-card"><div class="test-name">{name}</div><div class="test-desc">{desc}</div></div>', unsafe_allow_html=True)
            st.write("")

# ---------- Pages ----------
if selected == "Dashboard":
    heading("WELCOME TO STATLAB", "Statistical Analysis", "Run your analysis with confidence.")
    a,b,c,d = st.columns(4)
    for col, icon, num, label in [
        (a,"🧪","25+","Planned statistical tests"),
        (b,"📁","4","Data import options"),
        (c,"📝","APA 7","Research reporting"),
        (d,"⬇️","Export","PDF · Word · Excel"),
    ]:
        with col:
            st.markdown(f'<div class="stat-card"><div class="stat-icon">{icon}</div><div class="stat-number">{num}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-title">⚡ Start a new analysis</div>', unsafe_allow_html=True)
    s1,s2,s3 = st.columns(3)
    with s1:
        st.markdown('<div class="step"><span class="step-no">1</span>Choose analysis</div><small>Select a statistical test</small>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="step"><span class="step-no">2</span>Upload or enter data</div><small>Excel, CSV or manual entry</small>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="step"><span class="step-no">3</span>Review results</div><small>Interpretation, graphs and report</small>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("Explore analysis categories")
    categories = [
        ("▦","Categorical Data","Nominal and ordinal outcomes","Categorical Data"),
        ("〰","Non-parametric Tests","Rank-based and distribution-free methods","Non-parametric Tests"),
        ("⚗","Parametric Tests","Compare means and model numeric outcomes","Parametric Tests"),
        ("⠿","Correlation & Regression","Explore relationships and build models","Correlation & Regression"),
    ]
    cols = st.columns(2)
    for i,(icon,name,desc,page) in enumerate(categories):
        with cols[i%2]:
            st.markdown(f'<div class="test-card"><div class="test-name">{icon} &nbsp; {name}</div><div class="test-desc">{desc}</div></div>', unsafe_allow_html=True)
            if st.button(f"Open {name} →", key=f"open_{i}", use_container_width=True):
                st.session_state["requested_page"] = page
                st.rerun()

    st.subheader("Popular tests")
    popular = [
        ("Chi-Square Test","Association between categorical variables"),
        ("Fisher's Exact Test","Exact association test, often useful for small samples"),
        ("McNemar's Test","Paired binary outcomes"),
        ("Mann–Whitney U Test","Compare two independent groups"),
        ("Independent Samples t-Test","Compare two group means"),
        ("Spearman's Correlation","Rank-based association"),
    ]
    cols = st.columns(3)
    for i,(name,desc) in enumerate(popular):
        with cols[i%3]:
            st.markdown(f'<div class="test-card"><div class="test-name">{name}</div><div class="test-desc">{desc}</div></div>', unsafe_allow_html=True)
            st.write("")

    st.subheader("Recent analyses")
    st.dataframe(pd.DataFrame([
        {"Date":"—","Test performed":"No analyses yet","Dataset":"—","Status":"Ready when you are"},
    ]), use_container_width=True, hide_index=True)

elif selected == "Descriptive Statistics":
    placeholder_page("Descriptive Statistics", "Summarise and understand your dataset before running inferential tests.", [
        ("Frequency Distribution","Counts and percentages for categorical variables"),
        ("Mean, Median & Mode","Measures of central tendency"),
        ("Variance & Standard Deviation","Measures of dispersion"),
        ("Quartiles & Percentiles","Understand spread and position"),
        ("Skewness & Kurtosis","Describe distribution shape"),
    ])
elif selected == "Categorical Data":
    placeholder_page("Categorical Data Analysis", "Tests for nominal and ordinal variables, including independent and paired designs.", [
        ("Pearson's Chi-Square","Association between categorical variables"),
        ("Fisher's Exact Test","Exact test for contingency tables"),
        ("McNemar's Test","Paired binary categorical outcomes"),
        ("Cochran's Q Test","Three or more related binary conditions"),
        ("Cochran–Armitage Trend Test","Trend across ordered groups"),
        ("Mantel–Haenszel Test","Association adjusted across strata"),
        ("Stuart–Maxwell Test","Marginal homogeneity for paired categories"),
        ("Bowker's Test","Symmetry in paired square tables"),
    ])
elif selected == "Non-parametric Tests":
    placeholder_page("Non-parametric Tests", "Methods commonly used for ordinal data or when parametric assumptions are not suitable.", [
        ("Mann–Whitney U Test","Two independent groups"),
        ("Wilcoxon Signed-Rank Test","Two related measurements"),
        ("Kruskal–Wallis Test","Three or more independent groups"),
        ("Friedman Test","Three or more related conditions"),
        ("Sign Test","Direction of paired differences"),
        ("Spearman's Rank Correlation","Monotonic rank association"),
        ("Kendall's Tau","Rank-based association"),
    ])
elif selected == "Parametric Tests":
    placeholder_page("Parametric Tests", "Compare means and model numerical outcomes using parametric methods.", [
        ("One-Sample t-Test","Compare a sample mean with a reference value"),
        ("Independent Samples t-Test","Compare two independent means"),
        ("Paired Samples t-Test","Compare two related means"),
        ("One-Way ANOVA","Compare three or more independent means"),
        ("Repeated Measures ANOVA","Compare repeated measurements"),
        ("Levene's Test","Assess equality of variances"),
        ("Shapiro–Wilk Test","Assess evidence against normality"),
    ])
elif selected == "Correlation & Regression":
    placeholder_page("Correlation & Regression", "Measure relationships and model outcomes.", [
        ("Pearson Correlation","Linear association between numeric variables"),
        ("Spearman Correlation","Monotonic association using ranks"),
        ("Kendall's Tau","Rank association"),
        ("Simple Linear Regression","Model one predictor and a numeric outcome"),
        ("Multiple Linear Regression","Model several predictors"),
        ("Binary Logistic Regression","Model a binary outcome"),
    ])
elif selected == "Reports":
    heading("YOUR RESEARCH OUTPUT", "Reports", "Your completed analyses and downloadable reports will appear here.")
    st.info("No reports yet. Run an analysis to create your first report.")
else:
    heading("ABOUT THE PROJECT", "About STATLAB", "A guided statistical analysis workspace for students and researchers.")
    st.markdown("""
    <div class="panel">
    <div class="panel-title">Built to make research statistics easier to use</div>
    STATLAB is planned to provide validated statistical calculations, transparent assumptions,
    plain-language interpretation, appropriate visualisations and research-ready reporting.
    <br><br><span class="pill">Current stage: UI prototype</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Important: This prototype is a user-interface preview. It does not yet calculate statistical tests.")
