import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="STATLAB", page_icon="📊", layout="wide")

st.markdown("""
<style>
.stApp{background:#0b1220;color:#edf2f7}
[data-testid="stHeader"]{background:#0b1220}
[data-testid="stSidebar"]{background:#101a2b;border-right:1px solid #26364d}
[data-testid="stSidebar"] *{color:#e7edf5!important}
h1,h2,h3,h4{color:#f4f7fb!important}
p,label,.stMarkdown,[data-testid="stCaptionContainer"]{color:#d3dce8}
[data-testid="stMetric"]{background:#142238;border:1px solid #2a405c;padding:14px;border-radius:12px}
[data-testid="stMetricLabel"]{color:#b9c8d9!important}
[data-testid="stMetricValue"]{color:#fff!important}
.stButton>button,.stDownloadButton>button{background:#0f9d9a;color:white!important;border:0;border-radius:9px;font-weight:600}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div,.stTextInput input{background:#17263b!important;color:#f4f7fb!important;border-color:#3a506d!important}
[data-testid="stFileUploader"]{background:#142238;border:1px dashed #52708f;border-radius:12px;padding:10px}
.statcard{background:linear-gradient(135deg,#142238,#172b43);border:1px solid #2b4562;border-radius:14px;padding:18px;margin:8px 0 16px}
</style>
""", unsafe_allow_html=True)

if "data" not in st.session_state:
    st.session_state.data = None
    st.session_state.filename = None

def read_file(f):
    if f.name.lower().endswith(".csv"):
        return pd.read_csv(f)
    return pd.read_excel(f)

def upload_widget(key):
    f = st.file_uploader("Upload CSV or Excel dataset", type=["csv","xlsx","xls"], key=key)
    if f:
        try:
            st.session_state.data = read_file(f)
            st.session_state.filename = f.name
            st.success(f"{f.name} loaded successfully.")
        except Exception as e:
            st.error(f"Unable to read file: {e}")

st.sidebar.markdown("## 📊 STATLAB")
st.sidebar.caption("Statistical Analysis & Research Assistant")
page = st.sidebar.radio("NAVIGATION",[
    "Dashboard","Data Workspace","Descriptive Statistics","Categorical Data",
    "Non-parametric Tests","Parametric Tests","Correlation & Regression","Reports","About STATLAB"
])
if st.session_state.data is not None:
    st.sidebar.success(f"Loaded: {st.session_state.filename}")
    st.sidebar.caption(f"{len(st.session_state.data)} rows × {len(st.session_state.data.columns)} columns")
else:
    st.sidebar.info("No dataset loaded")

df = st.session_state.data

if page == "Dashboard":
    st.title("STATLAB")
    st.subheader("Statistical Analysis & Research Assistant")
    st.markdown('<div class="statcard"><b style="color:#55d6cf">VERSION 0.2</b><p>Dark-mode research statistics workspace with readable, high-contrast typography.</p></div>',unsafe_allow_html=True)
    x,y,z = st.columns(3)
    x.metric("Version","0.2"); y.metric("Working modules","2"); z.metric("Theme","Dark")
    st.header("Start your analysis")
    upload_widget("dashboard_upload")
    st.info("Working now: data upload, dataset inspection and descriptive statistics. Inferential tests and report exports are planned, not yet active.")

elif page == "Data Workspace":
    st.title("Data Workspace")
    upload_widget("workspace_upload")
    df = st.session_state.data
    if df is not None:
        a,b,c,e = st.columns(4)
        a.metric("Observations",f"{len(df):,}")
        b.metric("Variables",f"{len(df.columns):,}")
        c.metric("Missing cells",f"{int(df.isna().sum().sum()):,}")
        e.metric("Duplicate rows",f"{int(df.duplicated().sum()):,}")
        st.header("Data preview")
        st.dataframe(df.head(100),use_container_width=True)
        info = pd.DataFrame({"Variable":df.columns.astype(str),"Data type":df.dtypes.astype(str).values,
          "Missing values":df.isna().sum().values,"Unique values":[df[c].nunique(dropna=True) for c in df.columns]})
        st.header("Variable information")
        st.dataframe(info,use_container_width=True,hide_index=True)
        st.download_button("Download dataset copy (CSV)",df.to_csv(index=False).encode(), "statlab_dataset.csv","text/csv")
    else:
        st.info("Upload a dataset above to begin.")

elif page == "Descriptive Statistics":
    st.title("Descriptive Statistics")
    df = st.session_state.data
    if df is None:
        st.warning("Upload a dataset first in Dashboard or Data Workspace.")
    else:
        numeric = df.select_dtypes(include=np.number).columns.tolist()
        categorical = [c for c in df.columns if c not in numeric]
        if numeric:
            st.header("Numerical variables")
            selected = st.multiselect("Select numerical variables",numeric,default=numeric[:4])
            if selected:
                out = df[selected].describe().T
                out["Median"] = df[selected].median()
                out["Mode"] = [df[c].mode().iloc[0] if not df[c].mode().empty else np.nan for c in selected]
                out["Variance"] = df[selected].var()
                out = out.rename(columns={"count":"N","mean":"Mean","std":"Std. deviation","min":"Minimum","25%":"25th percentile","50%":"Median (50th percentile)","75%":"75th percentile","max":"Maximum"})
                st.dataframe(out.round(4),use_container_width=True)
                v = st.selectbox("Visualise variable",selected)
                kind = st.radio("Chart",["Histogram","Box plot"],horizontal=True)
                fig = px.histogram(df,x=v,nbins=25,title=f"Distribution of {v}",template="plotly_dark") if kind=="Histogram" else px.box(df,y=v,title=f"Box plot of {v}",template="plotly_dark")
                fig.update_layout(paper_bgcolor="#0b1220",plot_bgcolor="#101a2b",font_color="#eaf1f8")
                st.plotly_chart(fig,use_container_width=True)
                st.download_button("Download numerical summary CSV",out.to_csv().encode(),"descriptive_statistics.csv","text/csv")
        else:
            st.info("No numerical variables detected.")
        st.header("Categorical variables")
        if categorical:
            v = st.selectbox("Choose categorical variable",categorical)
            freq = df[v].value_counts(dropna=False).rename_axis("Category").reset_index(name="Frequency")
            freq["Percentage"] = (freq["Frequency"]/len(df)*100).round(2)
            st.dataframe(freq,use_container_width=True,hide_index=True)
            fig = px.bar(freq.head(30),x="Category",y="Frequency",title=f"Frequency distribution: {v}",template="plotly_dark")
            fig.update_layout(paper_bgcolor="#0b1220",plot_bgcolor="#101a2b",font_color="#eaf1f8")
            st.plotly_chart(fig,use_container_width=True)
            st.download_button("Download frequency table CSV",freq.to_csv(index=False).encode(),"frequency_table.csv","text/csv")
        else:
            st.info("No categorical/text variables detected.")

elif page in ["Categorical Data","Non-parametric Tests","Parametric Tests","Correlation & Regression","Reports"]:
    st.title(page)
    st.markdown('<div class="statcard"><b style="color:#55d6cf">COMING IN A LATER VERSION</b><p>This section is visible in navigation but its statistical procedures are not implemented yet.</p></div>',unsafe_allow_html=True)
    st.info("Version 0.2 supports data upload, inspection and descriptive statistics. Each inferential method will be added and validated before being enabled.")

else:
    st.title("About STATLAB")
    st.markdown('<div class="statcard"><b style="color:#55d6cf">STATLAB v0.2</b><p>A practical statistical analysis assistant for students and researchers.</p></div>',unsafe_allow_html=True)
    st.markdown("""
    **Working features**
    - CSV and Excel upload
    - Dataset preview and variable information
    - Missing-value and duplicate-row overview
    - Numerical descriptive statistics
    - Categorical frequency tables and percentages
    - Histograms, box plots and bar charts
    - CSV downloads for summary tables

    **Not active yet:** inferential hypothesis tests, automatic test selection, APA 7 reporting, and Word/PDF report exports.
    """)
