import streamlit as st
import pandas as pd
import joblib

# Carrega o modelo salvo
model = joblib.load('modelo_inadimplencia.joblib')

# 🎨 Interface Streamlit
st.set_page_config(page_title="Previsão de Inadimplência - Aluzy", layout="centered")
st.title("🔍 Previsão de Inadimplência - Aluzy")
st.markdown("Preencha os dados do inquilino para estimar o risco de inadimplência.")

# Inputs
idade = st.slider("Idade", 18, 70, 30)
renda = st.number_input("Renda mensal (R$)", 500, 20000, 3000, step=100)
valor_aluguel = st.number_input("Valor do aluguel (R$)", 300, 10000, 1200, step=50)
cartao = st.selectbox("Pagamento com cartão?", ["Sim", "Não"])
cartao_usado = 1 if cartao == "Sim" else 0
score = st.slider("Score de crédito", 300, 1000, 700)

# Quando clicar no botão
if st.button("🔮 Prever risco"):
    entrada = pd.DataFrame([{
        'idade': idade,
        'renda_mensal': renda,
        'valor_aluguel': valor_aluguel,
        'cartao_usado': cartao_usado,
        'score_credito': score
    }])

    prob = model.predict_proba(entrada)[0][1] * 100
    risco = f"{prob:.2f}%"
    st.success(f"✅ Risco de inadimplência: **{risco}**")

    if prob > 60:
        st.warning("⚠️ Risco alto! Avaliação detalhada recomendada.")
    elif prob > 30:
        st.info("🟡 Risco moderado.")
    else:
        st.success("🟢 Risco baixo.")

