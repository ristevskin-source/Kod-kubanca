import streamlit as st

# --- STANJE APLIKACIJE ---
if "zakazivanja" not in st.session_state:
    st.session_state.zakazivanja = []

if "admin_logovan" not in st.session_state:
    st.session_state.admin_logovan = False

# Inicijalne cene
if "usluge" not in st.session_state:
    st.session_state.usluge = {
        "Šišanje": 1000,
        "Brada": 500,
        "Šišanje i Brada": 1400,
        "Pranje kose": 300
    }

# --- ADMIN PRIJAVA ---
if not st.session_state.admin_logovan:
    st.title("Admin prijava")
    lozinka = st.text_input("Unesi admin lozinku", type="password")
    if st.button("Prijavi se"):
        if lozinka == "1234":
            st.session_state.admin_logovan = True
            st.rerun()
        else:
            st.error("Pogrešna lozinka!")
    st.stop()

# --- ADMIN KONTROLNA TABLA (Bočna traka) ---
with st.sidebar:
    st.header("⚙️ Admin panel")
    st.subheader("Izmena cena")
    for usluga in st.session_state.usluge:
        st.session_state.usluge[usluga] = st.number_input(f"Cena za {usluga}", value=st.session_state.usluge[usluga])
    
    if st.button("Odjavi se"):
        st.session_state.admin_logovan = False
        st.rerun()

# --- GLAVNI DEO ---
st.title("Kod Kubanca")
st.image("Screenshot_20260717_011214.jpg", width=300)
st.subheader("Planer termina")

with st.form("zakazivanje", clear_on_submit=True):
    # Koristimo ključeve iz našeg rečnika za selectbox
    izabrana_usluga = st.selectbox("Izaberi uslugu", list(st.session_state.usluge.keys()))
    datum = st.date_input("Izaberi datum")
    ime = st.text_input("Ime i prezime")
    telefon = st.text_input("Broj telefona")
    submit = st.form_submit_button("Zakaži")

    if submit:
        if ime and telefon:
            termin = {
                "Ime": ime, 
                "Telefon": telefon, 
                "Usluga": izabrana_usluga, 
                "Cena": st.session_state.usluge[izabrana_usluga],
                "Datum": datum
            }
            st.session_state.zakazivanja.append(termin)
            st.success(f"Termin dodat! Cena: {st.session_state.usluge[izabrana_usluga]} RSD")
        else:
            st.error("Molimo unesite podatke.")

st.divider()
st.subheader("Lista zakazanih termina:")
for i, t in enumerate(st.session_state.zakazivanja):
    st.write(f"{i+1}. **{t['Ime']}** - {t['Usluga']} ({t['Cena']} RSD) - {t['Datum']}")
