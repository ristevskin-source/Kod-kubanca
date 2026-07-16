
import streamlit as st

# Prvo slika
st.image("Screenshot_20260716_172456_com_viber_voip_MediaPreviewActivity.jpg", width=300)

# Zatim naslov
st.title("Kod kubanca")

# 2. Cenovnik
cenovnik = {
    "Obrve": 400,
    "Šišanje": 1500,
    "Šišanje i Brada": 2000,
    "Brada": 1000,
    "Pranje Kose": 400
}

# 3. Forma za unos
with st.form("zakazivanje_forme"):
    st.subheader("Rezervacija termina")
    
    ime = st.text_input("Ime klijenta")
    datum = st.date_input("Izaberi datum")
    vreme = st.time_input("Izaberi vreme")
    
    odabrane_usluge = st.multiselect("Izaberi usluge:", list(cenovnik.keys()))
    
    submit = st.form_submit_button("Zakaži termin")

# 4. Logika nakon slanja
if submit:
    if ime and odabrane_usluge:
        ukupna_cena = sum([cenovnik[u] for u in odabrane_usluge])
        st.success(f"Uspešno zakazano za: {ime}")
        st.write(f"📅 Datum: {datum} u {vreme}")
        st.write(f"✂️ Usluge: {', '.join(odabrane_usluge)}")
        st.write(f"💰 Ukupna cena: {ukupna_cena} RSD")
    else:
        st.error("Molim te, unesi ime klijenta i izaberi bar jednu uslugu.")
