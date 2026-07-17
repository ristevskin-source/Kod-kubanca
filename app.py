import streamlit as st

# --- STANJE APLIKACIJE ---
if "zakazivanja" not in st.session_state:
    st.session_state.zakazivanja = []

if "usluge" not in st.session_state:
    st.session_state.usluge = {"Šišanje": 1000, "Brada": 500}

# --- PROVERA ADMINA ---
query_params = st.query_params
je_admin = query_params.get("admin") == "true"

# --- ADMIN PANEL (Vidljiv samo ako je ?admin=true u linku) ---
if je_admin:
    st.sidebar.header("⚙️ Admin Podešavanja")
    
    # Dodavanje/Izmena usluga
    nova_usluga = st.sidebar.text_input("Naziv usluge")
    nova_cena = st.sidebar.number_input("Cena", min_value=0)
    if st.sidebar.button("Dodaj/Izmeni uslugu"):
        st.session_state.usluge[nova_usluga] = nova_cena
        st.rerun()

    st.sidebar.divider()
    st.sidebar.subheader("Upravljanje terminima")
    for i, t in enumerate(st.session_state.zakazivanja):
        if st.sidebar.button(f"Obriši: {t['Ime']}", key=f"del_{i}"):
            st.session_state.zakazivanja.pop(i)
            st.rerun()

# --- GLAVNI DEO (Javni) ---
st.title("Kod Kubanca")
# Ovde je tvoj logo
st.image("Screenshot_20260717_011214.jpg", width=300)

st.subheader("Planer termina")

with st.form("zakazivanje", clear_on_submit=True):
    izabrana_usluga = st.selectbox("Izaberi uslugu", list(st.session_state.usluge.keys()))
    datum = st.date_input("Izaberi datum")
    ime = st.text_input("Ime i prezime")
    telefon = st.text_input("Broj telefona")
    submit = st.form_submit_button("Zakaži")

    if submit:
        if ime and telefon:
            termin = {"Ime": ime, "Usluga": izabrana_usluga, "Cena": st.session_state.usluge[izabrana_usluga], "Datum": datum}
            st.session_state.zakazivanja.append(termin)
            st.success("Termin uspešno dodat!")
        else:
            st.error("Unesi ime i telefon.")

st.divider()
st.subheader("Svi termini:")
for t in st.session_state.zakazivanja:
    st.write(f"📅 {t['Datum']} | {t['Ime']} | {t['Usluga']} ({t['Cena']} RSD)")
