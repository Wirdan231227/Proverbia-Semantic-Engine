import streamlit as st
import pandas as pd
from rdflib import Graph, Namespace
import matplotlib.pyplot as plt
import base64

def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# CALL THE FUNCTION
set_background("assets/photo.jpg")


# ========== CONFIG ==========
TTL_FILE_PATH = "data/proverbs.ttl"
EX = Namespace("http://example.org/proverbs#")
# ============================

# ---------- LOAD RDF ----------
@st.cache_resource
def load_graph():
    g = Graph()
    g.parse(TTL_FILE_PATH, format="turtle")
    return g

g = load_graph()
# ----------------------------

# ---------- UTIL ----------
def get_distinct_values(predicate):
    query = f"""
    SELECT DISTINCT ?value
    WHERE {{
        ?p <{predicate}> ?value .
    }}
    """
    return sorted(str(r.value).split("#")[-1] for r in g.query(query))
# --------------------------

# ---------- FILTER VALUES ----------
regions = get_distinct_values(EX.hasRegion)
sources = get_distinct_values(EX.hasSource)
themes = get_distinct_values(EX.hasTheme)
subthemes = get_distinct_values(EX.hasSubTheme)
# ----------------------------------

# ---------- UI ----------
st.set_page_config(page_title="Proverb Ontology Explorer", layout="wide")
st.title("📜 Proverbia Semantic Engine")
st.write("Semantic search, similarity detection, and analytics using RDF & SPARQL")

c1, c2, c3, c4 = st.columns(4)

with c1:
    region = st.selectbox("Region", ["Any"] + regions)
with c2:
    source = st.selectbox("Source", ["Any"] + sources)
with c3:
    theme = st.selectbox("Theme", ["Any"] + themes)
with c4:
    subtheme = st.selectbox("SubTheme", ["Any"] + subthemes)

keyword = st.text_input("🔍 Keyword search (text or meaning)")
# --------------------------

# ---------- SPARQL BUILDER ----------
def build_query(region, source, theme, subtheme, keyword):
    filters = []

    if region != "Any":
        filters.append(f"?p <{EX.hasRegion}> <{EX}{region}> .")
    if source != "Any":
        filters.append(f"?p <{EX.hasSource}> <{EX}{source}> .")
    if theme != "Any":
        filters.append(f"?p <{EX.hasTheme}> <{EX}{theme}> .")
    if subtheme != "Any":
        filters.append(f"?p <{EX.hasSubTheme}> <{EX}{subtheme}> .")

    if keyword:
        filters.append(
            f'FILTER (CONTAINS(LCASE(STR(?text)), "{keyword.lower()}") '
            f'|| CONTAINS(LCASE(STR(?meaning)), "{keyword.lower()}"))'
        )

    filter_block = "\n".join(filters)

    return f"""
    SELECT ?text ?meaning ?region ?source ?theme ?subtheme
    WHERE {{
        ?p a <{EX.Proverb}> ;
           <{EX.hasText}> ?text ;
           <{EX.hasMeaning}> ?meaning ;
           <{EX.hasRegion}> ?region ;
           <{EX.hasSource}> ?source ;
           <{EX.hasTheme}> ?theme ;
           <{EX.hasSubTheme}> ?subtheme .
        {filter_block}
    }}
    """
# -----------------------------------

# ---------- RUN QUERY ----------
query = build_query(region, source, theme, subtheme, keyword)
results = g.query(query)

rows = []
for r in results:
    rows.append({
        "Proverb": str(r.text),
        "Meaning": str(r.meaning),
        "Region": str(r.region).split("#")[-1],
        "Source": str(r.source).split("#")[-1],
        "Theme": str(r.theme).split("#")[-1],
        "SubTheme": str(r.subtheme).split("#")[-1],
    })

df = pd.DataFrame(rows)
# -------------------------------

# ---------- RESULTS ----------
st.subheader(f"Results ({len(df)})")

if df.empty:
    st.warning("No matching proverbs found.")
else:
    st.dataframe(df, width='stretch')

# ---------------------------
