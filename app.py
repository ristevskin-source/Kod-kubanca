import streamlit as st
from datetime import time

# --- STANJE APLIKACIJE ---
if "zakazivanja" not in st.session_state:
    st.session_state.zakazivanja = []

if "usluge" not in st.session_state:
    # Sada čuvamo: Naziv: (Cena, Trajanje_u_minutima)
    st.session_state.usluge = {"Šišanje": (1000, 60), "Brada": (500, 30)}

# --- PROVERA ADMINA ---
query_params = st.query_params
je_admin = query_params.get("admin") == "true"

# --- ADMIN PANEL ---
if je_admin:
    st.sidebar.header("⚙️ Admin Podešavanja")
    nova_usluga = st.sidebar.text_input("Naziv usluge")
    nova_cena = st.sidebar.number_input("Cena", min_value=0)
    novo_trajanje = st.sidebar.number_input("Trajanje (min)", min_value=5, step=5, value=60)
    
    if st.sidebar.button("Dodaj/Izmeni uslugu"):
        st.session_state.usluge[nova_usluga] = (nova_cena, novo_trajanje)
        st.rerun()

    st.sidebar.divider()
    st.sidebar.subheader("Upravljanje terminima")
    for i, t in enumerate(st.session_state.zakazivanja):
        if st.sidebar.button(f"Obriši: {t['Ime']} ({t['Vreme']})", key=f"del_{i}"):
            st.session_state.zakazivanja.pop(i)
            st.rerun()

# --- GLAVNI DEO ---
st.title("Kod Kubanca")
st.image("Screenshot_20260717_011214.jpg", width=300)

with st.form("zakazivanje", clear_on_submit=True):
    izabrana_usluga = st.selectbox("Izaberi uslugu", list(st.session_state.usluge.keys()))
    datum = st.date_input("Izaberi datum")
    vreme = st.time_input("Izaberi vreme", value=time(12, 0)) # Podrazumevano 12:00
    ime = st.text_input("Ime i prezime")
    telefon = st.text_input("Broj telefona")
    submit = st.form_submit_button("Zakaži")

    if submit:
        if ime and telefon:
            cena, trajanje = st.session_state.usluge[izabrana_usluga]
            termin = {
                "Ime": ime, 
                "Usluga": izabrana_usluga, 
                "Cena": cena, 
                "Datum": datum, 
                "Vreme": vreme.strftime("%H:%M")
            }
            st.session_state.zakazivanja.append(termin)
            st.success(f"Termin za {izabrana_usluga} zakazan u {vreme.strftime('%H:%M')}!")
        else:
            st.error("Unesi ime i telefon.")

st.divider()
st.subheader("Svi termini:")
# Sortiramo da najnoviji budu pri vrhu
for t in st.session_state.zakazivanja:
    st.write(f"📅 {t['Datum']} u {t['Vreme']} | {t['Ime']} | {t['Usluga']} ({t['Cena']} RSD)")
