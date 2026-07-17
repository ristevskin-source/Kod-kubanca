import streamlit as st
import datetime

# --- STANJE APLIKACIJE ---
if "zakazivanja" not in st.session_state:
    st.session_state.zakazivanja = []

if "usluge" not in st.session_state:
    st.session_state.usluge = {"Šišanje": (1000, 60), "Brada": (500, 30)}

if "radno_vreme" not in st.session_state:
    st.session_state.radno_vreme = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]

# --- PROVERA ADMINA ---
query_params = st.query_params
je_admin = query_params.get("admin") == "true"

# --- ADMIN PANEL ---
if je_admin:
    st.sidebar.header("⚙️ Admin Podešavanja")
    
    # Statistika prometa
    st.sidebar.subheader("📈 Statistika prometa")
    ukupan_promet = sum([t['Cena'] for t in st.session_state.zakazivanja])
    st.sidebar.metric("Ukupan promet", f"{ukupan_promet} RSD")
    
    st.sidebar.subheader("Upravljanje terminima")
    for i, t in enumerate(st.session_state.zakazivanja):
        d_str = t['Datum'].strftime('%d.%m.%Y.')
        if st.sidebar.button(f"Obriši: {d_str} {t['Vreme']} - {t['Ime']}", key=f"del_{i}"):
            st.session_state.zakazivanja.pop(i)
            st.rerun()

# --- GLAVNI DEO ---
# Postavljanje logotipa
try:
    st.image("Screenshot_20260717_011214.jpg", width=300)
except:
    st.warning("Logo nije pronađen (fajl 'logo.png' treba da bude u folderu).")

st.title("Kod Kubanca")

with st.form("zakazivanje", clear_on_submit=True):
    izabrana_usluga = st.selectbox("Izaberi uslugu", list(st.session_state.usluge.keys()))
    datum = st.date_input("Izaberi datum")
    
    zauzeti_termini = [t['Vreme'] for t in st.session_state.zakazivanja if str(t['Datum']) == str(datum)]
    slobodni_termini = [t for t in st.session_state.radno_vreme if t not in zauzeti_termini]
    
    if slobodni_termini:
        izabrano_vreme = st.selectbox("Izaberi slobodan termin", slobodni_termini)
        ime = st.text_input("Ime i prezime")
        telefon = st.text_input("Broj telefona")
        submit = st.form_submit_button("Zakaži")
    else:
        st.warning("Nema slobodnih termina za izabrani datum.")
        submit = False

    if submit:
        if ime and telefon:
            cena, _ = st.session_state.usluge[izabrana_usluga]
            termin = {
                "Ime": ime, "Telefon": telefon, 
                "Usluga": izabrana_usluga, "Cena": cena, 
                "Datum": datum, "Vreme": izabrano_vreme
            }
            st.session_state.zakazivanja.append(termin)
            
            datum_formatiran = datum.strftime('%d.%m.%Y.')
            st.success(f"✅ Uspešno zakazano! {izabrana_usluga} za {datum_formatiran} u {izabrano_vreme}. Vidimo se!")
        else:
            st.error("Unesi ime i telefon.")

st.divider()
st.subheader("Zakazani termini:")
for t in st.session_state.zakazivanja:
    d = t['Datum'].strftime('%d.%m.%Y.')
    st.write(f"📅 **{d}** | ⏰ **{t['Vreme']}** | 👤 {t['Ime']} ({t['Telefon']}) | ✂️ {t['Usluga']} ({t['Cena']} RSD)")
