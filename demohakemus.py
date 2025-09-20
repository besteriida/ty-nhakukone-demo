import streamlit as st
import json
import re

# Lataa profiili
with open("profiili.json", "r", encoding="utf-8") as file:
    profiili = json.load(file)

st.title("Hakemuskirjeassistentti 🤖📄")
st.markdown("💡 Täytä kentät ja paina nappia – hakemus kirjoitetaan automaattisesti valintojesi mukaan.")

# Syöte: työpaikkailmoitus
ilmoitus = st.text_area("Liitä työpaikkailmoitus tähän")

# Valinnat: kieli ja sävy
kieli = st.radio("Valitse kieli", ["fi", "en"])
savy = st.radio("Valitse sävy", ["virallinen", "rennompi"])

# Kun käyttäjä painaa nappia
if st.button("Generoi hakemus"):
    avainsanat = re.findall(r"\b\w+\b", ilmoitus.lower())

    relevantit_taidot = [
        taito for taito in profiili["taidot"]
        if any(avain in taito.lower() for avain in avainsanat)
    ]

    relevantit_tyohistoria = []
    for tyopaikka in profiili["työhistoria"]:
        osumat = [
            kuvaus for kuvaus in tyopaikka["kuvaus"]
            if any(avain in kuvaus.lower() for avain in avainsanat)
        ]
        if osumat:
            relevantit_tyohistoria.append({
                "työnimike": tyopaikka["työnimike"],
                "yritys": tyopaikka["yritys"],
                "kuvaus": osumat
            })

    relevantit_faktat = [
        fakta for fakta in profiili.get("hauskat_faktat", [])
        if any(avain in fakta.lower() for avain in avainsanat)
    ]

    st.success("✅ Relevantit tiedot analysoitu – hakemus kirjoitetaan nyt!")

    # ✍️ Hakemuskirjeen generointi
    if kieli == "fi":
        if savy == "virallinen":
            selitys = "Tämä hakemus on tuotettu hyödyntäen digitaalista työnhakutyökalua, joka analysoi työpaikkailmoituksen ja yhdistää siihen profiilin keskeiset osaamiset. Tavoitteena on tuottaa kohdennettu ja relevantti hakemus tehokkaasti – mutta ajatuksella."
        else:
            selitys = "Hakemus on tehty omalla työnhakukoneella, joka lukee ilmoituksen ja yhdistää siihen osaamisen. Ei laiskuutta – vaan fiksua automaatiota."

        hakemus = f"""{selitys}

Olen monipuolinen ja utelias tekijä, jolla on kokemusta sisällöntuotannosta, projektinhallinnasta ja kumppanuuksien rakentamisesta. Työskentely eri organisaatioissa on kehittänyt osaamistani oppimateriaalien tuotannossa, markkinoinnin tukemisessa ja tapahtumien suunnittelussa.

Taitoni ulottuvat teknisestä osaamisesta ({', '.join(relevantit_taidot[:5])}...) aina pehmeisiin taitoihin kuten viestintään, tiimityöhön ja asiakassuhteiden hoitoon. Lisäksi minulla on taustaa hankevalmistelussa ja kampanjasuunnittelussa. Ja kyllä – olen myös pubivisa-asiantuntija, joka vetää omaa visaa paikallisessa baarissa kerran kuussa.

Persoonani tuo tiimiin iloa, omistautumista ja ripauksen koiratanssia – koirani kanssa harrastetaan lajia, vaikka tanssitaidot eivät ole meillä kummallakaan huippuluokkaa.

Toivon mahdollisuutta keskustella tehtävästä lisää ja kuulla, miten voisin tuoda osaamiseni teidän tiimiin.

Ystävällisin terveisin,  
Demo Käyttäjä  
demo@example.com | 040 123 4567
"""
    else:
        if savy == "virallinen":
            selitys = "This application was generated using a personal job application assistant that analyzes the job posting and matches it with a profile. The goal is to deliver a targeted and thoughtful application efficiently."
        else:
            selitys = "I used my own job application bot to create this letter – it reads the job ad and mixes in my skills. Smart automation, not laziness."

        hakemus = f"""{selitys}

I'm a versatile and curious professional with experience in content creation, project coordination, and partnership development. My work across various organizations has strengthened my skills in educational material production, marketing support, and event planning.

My abilities range from technical skills ({', '.join(relevantit_taidot[:5])}...) to soft skills like communication, teamwork, and client relations. I also bring a background in project preparation and campaign planning. And yes – I'm a pub quiz expert who hosts monthly trivia nights at a local bar.

I bring energy, dedication, and a touch of dog dancing to any team – my dog and I practice together, though neither of us is winning awards anytime soon.

I’d love the opportunity to discuss how I can contribute to your team.

Best regards,  
Demo User  
demo@example.com | +358 40 123 4567
"""

    # Näytä hakemus
    st.text_area("Valmis hakemuskirje", hakemus, height=400)

    # Tallennusnapilla lataus
    st.download_button("📥 Lataa hakemus .txt-muodossa", hakemus, file_name="hakemus.txt")