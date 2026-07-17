import streamlit as st
import smtplib
from email.message import EmailMessage

# --- FUNKCIJA ZA SLANJE EMAIL-A ---
def posalji_email(ime, telefon, usluga, datum):
    msg = EmailMessage()
    msg.set_content(f"Novo zakazivanje!\n\nIme: {ime}\nTelefon: {telefon}\nUsluga: {usluga}\nDatum: {datum}")
    msg['Subject'] = 'Novo zakazivanje - Kod Kubanca'
    msg['From'] = 'ristevskin@gmail.com'
    msg['To'] = 'ristevskin@gmail.com'

    # Koristimo tvoju lozinku
    password = 'tatarista1199111' 
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('ristevskin@gmail.com', password)
        smtp.send_message(msg)

# --- ADMIN PROVERA ---
if "admin_logovan" not in st.session_state:
    st.session_state.admin_logovan = False

if not st.session_state.admin_logovan:
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

cenovnik = {"Šišanje": 1500, "Brada": 1000, "Šišanje i Brada": 2000, "Pranje kose": 400}
for usluga, cena in cenovnik.items():
    st.write(f"{usluga}: {cena} RSD")

st.divider()

with st.form("zakazivanje"):
    izabrana_usluga = st.selectbox("Izaberi uslugu", list(cenovnik.keys()))
    datum = st.date_input("Izaberi datum")
    ime = st.text_input("Ime i prezime")
    telefon = st.text_input("Broj telefona")
    submit = st.form_submit_button("Zakaži")

    if submit:
        if not telefon:
            st.error("Molimo vas da unesete broj telefona!")
        else:
            try:
                posalji_email(ime, telefon, izabrana_usluga, datum)
                st.success("Uspešno zakazano i poslato na mail!")
            except Exception as e:
                st.error(f"Greška pri slanju maila: {e}")
