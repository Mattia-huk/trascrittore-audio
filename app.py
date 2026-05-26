import streamlit as st
import whisper
import os

st.set_page_config(page_title="Trascrizione Audio AI", page_icon="🎙️", layout="centered")

@st.cache_resource
def carica_modello_audio():
    # Usiamo il modello 'tiny' o 'base' ideale per i server cloud gratuiti
    return whisper.load_model("tiny")

st.title("🎙️ Trascrizione Audio Intelligente")
st.write("Carica un file audio. L'AI lo trascriverà fedelmente in paragrafi, ripulendolo dai tic del linguaggio.")

file_audio = st.file_uploader("Scegli un file audio (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"])

if file_audio is not None:
    st.success("✅ File audio caricato con successo!")
    
    if st.button("🚀 Avvia Trascrizione e Pulizia"):
        with st.spinner("L'AI sta elaborando il tuo audio... Attendi..."):
            with open("temp_audio.mp3", "wb") as f:
                f.write(file_audio.getbuffer())
            try:
                modello = carica_modello_audio()
                risultato = modello.transcribe("temp_audio.mp3")
                testo_greggio = risultato["text"]
                
                parole_da_eliminare = [" ehm,", " ehm", " uhm,", " uhm", " cioè,", " praticamente,", " tipo,"]
                testo_pulito = testo_greggio
                for parola in parole_da_eliminare:
                    testo_pulito = testo_pulito.replace(parola, "")
                    testo_pulito = testo_pulito.replace(parola.capitalize(), "")

                frasi = testo_pulito.split(". ")
                paragrafi = []
                paragrafo_corrente = []
                for i, frase in enumerate(frasi):
                    paragrafo_corrente.append(frase)
                    if (i + 1) % 4 == 0:
                        paragrafi.append(". ".join(paragrafo_corrente) + ".")
                        paragrafo_corrente = []
                if paragrafo_corrente:
                    paragrafi.append(". ".join(paragrafo_corrente))
                
                testo_finale = "\n\n".join(paragrafi)
                st.success("✨ Trascrizione completata!")
                st.text_area("Ecco il testo:", testo_finale, height=350)
                st.download_button("⬇️ Scarica Trascrizione (.txt)", testo_finale, "trascrizione.txt")
            except Exception as e:
                st.error(f"Errore: {e}")
            if os.path.exists("temp_audio.mp3"):
                os.remove("temp_audio.mp3")
