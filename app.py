
import streamlit as st
 hashlib
import json
import smtplib
import os
from email.message import EmailMessage

# --- KONFIGURACIJA ---
CONFIG_FILE = "config.json"

def ucitaj_config():
    if not os.path.exists(CONFIG_FILE):
        return {"admin_hash": "NONE"}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def hesuj(tekst):
    return hashlib.sha256(tekst.encode()).hexdigest()

def posalji_mail(subjekt, sadrzaj):
    # Napomena: U st.secrets treba definisati email_user i email_pass
    try:
        msg = EmailMessage()
        msg.set_content(sadrzaj)
        msg['Subject'] = subjekt
        msg['From'] = st.secrets["email_user"]
        msg['To'] = st.secrets["email_user"]
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(st.secrets["email_user"], st.secrets["email_pass"])
            smtp.send_message(msg)
    except Exception as e:
        st.error(f"Greška pri slanju maila: {e}")

# --- GLAVNI DEO ---
# Cenovnik
cenovnik = {
    "Šišanje": 1500,
    "Brada": 1000,
    "Šišanje i Brada": 2000,
    "Pranje kose": 400
}

st.subheader("Naše usluge")
for usluga, cena in cenovnik.items():
    st.write(f"{usluga}: {cena} RSD")

# Prikaz slike (postavi putanju do slike ako je u folderu)
# st.image("ime_tvoje_slike.jpg", width=300)

st.title("Zakazivanje termina")

# 1. KLIJENTSKI DEO
ime = st.text_input("Ime i prezime")
termin = st.text_input("Željeni termin")
if st.button("Zakaži termin"):
    posalji_mail("Novi termin", f"Klijent: {ime}\nTermin: {termin}")
    st.success("Zahtev uspešno prosleđen!")

st.divider()

# 2. ADMIN DEO
with st.expander("Admin pristup"):
    # CSS za "prsten" koji se primenjuje SAMO na polja unutar ovog expander-a
    st.markdown("""
        <style>
        .st-emotion-cache-1vt4y4j input {
            border: 3.5px solid #4CAF50 !important;
            border-radius: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    config = ucitaj_config()
    
    # Inicijalizacija ako nema otiska
    if config["admin_hash"] == "NONE":
        if st.text_input("Lozinka za inicijalizaciju:", type="password") == "1234":
            novi_otisak = st.text_input("Postavi novi admin otisak:")
            if st.button("Aktiviraj Admina"):
                config["admin_hash"] = hesuj(novi_otisak)
                with open(CONFIG_FILE, "w") as f: json.dump(config, f)
                st.rerun()
    else:
        # Login za postojećeg admina
        if not st.session_state.get("admin_ulogovan"):
            pass_input = st.text_input("Admin lozinka:", type="password")
            if st.button("Pristupi admin panelu"):
                if hesuj(pass_input) == config["admin_hash"]:
                    st.session_state.admin_ulogovan = True
                    st.rerun()
        else:
            st.write("Dobrodošao, Admire. Ovde možeš menjati podešavanja.")
            if st.button("Odjavi se"):
                st.session_state.admin_ulogovan = False
                st.rerun()
