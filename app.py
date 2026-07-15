
import streamlit as st

st.title("💈 Berbernica - Upravljanje terminima")

# Forma za unos
with st.form("zakazivanje_forme"):
    ime = st.text_input("Ime klijenta")
    datum = st.date_input("Izaberi datum")
    submit = st.form_submit_button("Zakaži termin")

if submit:
    if ime:
        st.success(f"Uspešno zakazano za: {ime} na datum {datum}")
    else:
        st.error("Molim te, unesi ime klijenta.")
