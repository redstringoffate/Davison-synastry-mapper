import streamlit as st
import pandas as pd
from io import BytesIO

# ---------------- GLOBAL SESSION INIT ----------------
if "page" not in st.session_state:
    st.session_state.page = 1

if "houses" not in st.session_state:
    st.session_state.houses = {c:[None]*12 for c in ["A","B","Composite","Davison"]}

if "planets" not in st.session_state:
    st.session_state.planets = {c:[] for c in ["A","B","Composite","Davison"]}

if "mode" not in st.session_state:
    st.session_state.mode = "A"


# ---------------- CONSTANTS ----------------
SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
         "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]

ZODIAC_SYMBOL = {
    "Aries":"♈","Taurus":"♉","Gemini":"♊","Cancer":"♋","Leo":"♌","Virgo":"♍",
    "Libra":"♎","Scorpio":"♏","Sagittarius":"♐","Capricorn":"♑","Aquarius":"♒","Pisces":"♓"
}

degree_options = range(30)
minute_options = range(60)
CHARTS = ["A","B","Composite","Davison"]


def opposite(sign):
    return SIGNS[(SIGNS.index(sign)+6)%12]


# ===========================================================
# STEP 1 — HOUSES
# ===========================================================
def show_step1():
    st.title("✨ Davison Synastry Mapper — Step 1: House Cusps")

    INPUT=["1H (Asc)", "2H", "3H", "4H (IC)", "5H", "6H"]
    AUTO=["7H (Dsc)", "8H", "9H", "10H (MC)", "11H", "12H"]

    for chart in CHARTS:
        st.subheader(chart)

        omit = False
        if chart != "A":
            omit = st.checkbox(f"Omit {chart}", key=f"omit_house_{chart}")

        disabled = omit

        cols=st.columns(3)
        order=[0,2,4,1,3,5]

        for idx in order:
            with cols[order.index(idx)%3]:
                st.write(INPUT[idx])

                key=f"{chart}_{idx}"
                sign=st.selectbox("",SIGNS,key=f"{key}_sign", disabled=disabled)
                deg =st.selectbox("°",degree_options,key=f"{key}_deg", disabled=disabled)
                minute=st.selectbox("′",minute_options,key=f"{key}_min", disabled=disabled)

                st.session_state.houses[chart][idx]=(sign,deg,minute)

        if not disabled:
            for i in range(6):
                base=st.session_state.houses[chart][i]
                if base:
                    st.session_state.houses[chart][i+6]=(opposite(base[0]),base[1],base[2])

        else:
            # If omitted: clear data
            st.session_state.houses[chart] = [None]*12

        st.write("---")

    if st.button("➡ Step 2"):
        st.session_state.page=2
        st.rerun()


# ===========================================================
# STEP 2 — PLANETS
# ===========================================================
def show_step2():
    st.title("✨ Step 2 — Enter Planets")

    for chart in CHARTS:
        st.subheader(chart)

        omit = False
        if chart!="A":
            omit = st.checkbox(f"Omit {chart}", key=f"omit_planet_{chart}")

        disabled = omit

        with st.form(f"form_{chart}", clear_on_submit=True):
            c1,c2,c3,c4=st.columns([3,2,1,1])
            name=c1.text_input("Name", disabled=disabled)
            sign=c2.selectbox("Sign",SIGNS, disabled=disabled)
            deg=c3.selectbox("°",degree_options, disabled=disabled)
            minute=c4.selectbox("′",minute_options, disabled=disabled)

            if st.form_submit_button("Add") and name.strip() and not disabled:
                st.session_state.planets[chart].append(
                    {"name":name,"sign":sign,"deg":deg,"min":minute}
                )
                st.rerun()

        if disabled:
            st.session_state.planets[chart] = []  # If omitted, clear

        for i,p in enumerate(st.session_state.planets[chart]):
            row=st.columns([5,1])
            row[0].write(f"{p['name']} {ZODIAC_SYMBOL[p['sign']]} {p['deg']}°{p['min']}′")
            if row[1].button("✕", key=f"del_{chart}_{i}"):
                st.session_state.planets[chart].pop(i)
                st.rerun()

        st.write("---")

    col1,col2=st.columns(2)
    if col1.button("⬅ Back"):
        st.session_state.page=1
        st.rerun()
    if col2.button("➡ Step 3"):
        st.session_state.page=3
        st.rerun()


# ===========================================================
# STEP 3 — RESULTS + XLSX EXPORT
# ===========================================================
def show_step3():
    st.title("🔍 Synastry Result Table")

    ZMAP={s:i for i,s in enumerate(SIGNS)}
    def to_long(sign,d,m): return ZMAP[sign]*30 + d + m/60

    def find_house(pos,cusps):
        for i in range(12):
            start,end=cusps[i],cusps[(i+1)%12]
            p=pos
            if end<start:end+=360
            if p<start:p+=360
            if start<=p<end:return i
        return 11

    cols = st.columns(4)
    for i,c in enumerate(CHARTS):
        if cols[i].button(c):
            st.session_state.mode = c
            st.rerun()

    def build_sheet(ref):
        if any(h is None for h in st.session_state.houses[ref]):
            return None

        cusps=[to_long(*h) for h in st.session_state.houses[ref]]
        flat=[]

        for chart in CHARTS:
            for p in st.session_state.planets[chart]:
                pos=to_long(p["sign"],p["deg"],p["min"])
                h=find_house(pos,cusps)
                dist=pos-cusps[h]
                if dist<0:dist+=360

                flat.append({
                    "h":h,
                    "chart":chart,
                    "label":f"{p['name']} {ZODIAC_SYMBOL[p['sign']]} {p['deg']}°{p['min']}′",
                    "dist":dist
                })

        flat.sort(key=lambda x:(x["h"],x["dist"],CHARTS.index(x["chart"])))

        rows=[]
        last=-1
        for item in flat:
            h=item["h"]
            cusp=st.session_state.houses[ref][h]

            house_label=f"{h+1}H ({ZODIAC_SYMBOL[cusp[0]]} {cusp[1]}°{cusp[2]}′)" if h!=last else ""
            last=h

            row={"House":house_label, "A":"—","B":"—","Composite":"—","Davison":"—"}
            row[item["chart"]]=item["label"]
            rows.append(row)

        return pd.DataFrame(rows)

    preview = build_sheet(st.session_state.mode)
    st.dataframe(preview, use_container_width=True)

    buffer=BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for c in CHARTS:
            df=build_sheet(c)
            if df is not None:
                df.to_excel(writer, sheet_name=c, index=False)

    st.download_button("📥 Download XLSX", buffer.getvalue(),
                       file_name="synastry.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    if st.button("⬅ Back"):
        st.session_state.page=2
        st.rerun()


# ===========================================================
# ROUTING
# ===========================================================
if st.session_state.page==1: show_step1()
elif st.session_state.page==2: show_step2()
else: show_step3()
