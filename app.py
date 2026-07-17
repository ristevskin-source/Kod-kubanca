import streamlit as st

# --- STANJE APLIKACIJE ---
if "zakazivanja" not in st.session_state:
    st.session_state.zakazivanja = []

# --- ADMIN PROVERA ---
if "admin_logovan" not in st.session_state:
    st.session_state.admin_logovan = False

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

# --- GLAVNI DEO ---
st.title("Kod Kubanca")
st.image("Screenshot_20260717_011214.jpg", width=300)
st.subheader("Planer termina")

with st.form("zakazivanje", clear_on_submit=True):
    izabrana_usluga = st.selectbox("Izaberi uslugu", ["Šišanje", "Brada", "Šišanje i Brada", "Pranje kose"])
    datum = st.date_input("Izaberi datum")
    ime = st.text_input("Ime i prezime")
    telefon = st.text_input("Broj telefona")
    submit = st.form_submit_button("Zakaži")

    if submit:
        if ime and telefon:
            termin = {"Ime": ime, "Telefon": telefon, "Usluga": izabrana_usluga, "Datum": datum}
            st.session_state.zakazivanja.append(termin)
            st.success("Termin uspešno dodat u listu!")
        else:
            st.error("Molimo unesite ime i broj telefona.")

st.divider()
st.subheader("Lista zakazanih termina:")

if not st.session_state.zakazivanja:
    st.write("Nema zakazanih termina za danas.")
else:
    for i, t in enumerate(st.session_state.zakazivanja):
        st.write(f"{i+1}. **{t['Ime']}** ({t['Telefon']}) - {t['Usluga']} ({t['Datum']})")

if st.button("Obriši sve termine"):
    st.session_state.zakazivanja = []
    st.rerun()
