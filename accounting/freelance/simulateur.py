import streamlit as st
from employee import compute_net_salary, compute_impot_revenu as compute_ir_employee
from freelancer_ir import estimate_sasu_ir_net_income
from freelancer_is import (
    estimate_sasu_is_net_income_v3_with_ir,
    optimise_salaire_vs_dividendes,
    compute_impot_revenu
)
from exporter import export_result_to_excel

import io
import pandas as pd

st.set_page_config(page_title="Simulateur Salarié vs Freelance", layout="centered")
st.title("📊 Simulateur Salarié vs Freelance")

mode = st.radio("Mode de simulation :", ["Salarié", "Freelance (SASU)", "Comparatif"])

brut = None
if mode in ["Salarié", "Comparatif"]:
    brut = st.number_input("💼 Votre salaire brut annuel (€)", min_value=0, step=1000, value=80000)

spouse_status = st.selectbox("👫 Statut de votre conjoint(e)", ["employee", "freelance"])
spouse_income_input = st.number_input(
    "💰 Revenu du conjoint (mensuel si salarié, annuel si freelance)",
    min_value=0,
    value=2000
)

conjoint_revenu_net = spouse_income_input * 12 if spouse_status == "employee" else spouse_income_input
parts = 2

if mode in ["Freelance (SASU)", "Comparatif"]:
    st.subheader("⚙️ Paramètres Freelance")
    regime = st.selectbox("Régime de la SASU", ["IR", "IS"])
    tjm = st.number_input("TJM (€)", min_value=100, value=770)
    jours = st.number_input("Jours facturés/an", min_value=0, max_value=365, value=220)
    frais = st.number_input("Frais déductibles (€)", min_value=0, value=5000)
    compta = st.number_input("Comptable (€)", min_value=0, value=2000)
    rc_pro = st.number_input("Assurance RC Pro (€)", min_value=0, value=500)
    salaire_brut = st.number_input("Salaire brut annuel versé (€)", min_value=0, value=20000)

def show_employee():
    net_salary = compute_net_salary(brut)
    total_net = net_salary + conjoint_revenu_net
    impots = compute_ir_employee(total_net, parts)
    after_tax = total_net - impots
    st.subheader("🧾 Résultat Salarié")
    st.write(f"Salaire net : **{round(net_salary, 2)} €**")
    st.write(f"Revenu net foyer : **{round(total_net, 2)} €**")
    st.write(f"Impôt sur le revenu : **{round(impots, 2)} €**")
    st.write(f"💶 Net après impôt : **{round(after_tax, 2)} €**")
    st.write(f"💸 Super net mensuel : **{round(after_tax / 12, 2)} €**")
    return round(after_tax / 12, 2)

def show_freelancer():
    if regime == "IR":
        data = estimate_sasu_ir_net_income(
            tjm=tjm,
            jours_facturés=jours,
            charges_fixes=compta + rc_pro,
            frais_deductibles=frais,
            salaire_annuel=7000
        )
        total_net = data["revenu_net_avant_ir"] + conjoint_revenu_net
        impots, _ = compute_impot_revenu(total_net, parts)
        after_tax = total_net - impots
        st.subheader("🧾 Freelance (SASU à l’IR)")
        st.write(f"Net avant IR : **{round(data['revenu_net_avant_ir'], 2)} €**")
        st.write(f"Foyer net : **{round(total_net, 2)} €**")
        st.write(f"Impôt sur le revenu : **{round(impots, 2)} €**")
        st.write(f"💶 Net après IR : **{round(after_tax, 2)} €**")
        st.write(f"💸 Super net mensuel : **{round(after_tax / 12, 2)} €**")

    else:
        st.subheader("🧠 Option d'optimisation")
        optimiser = st.checkbox("Optimiser automatiquement le salaire brut")

        if optimiser:
            data = optimise_salaire_vs_dividendes(
                tjm=tjm,
                jours_facturés=jours,
                charges_fixes=compta + rc_pro,
                frais_deductibles=frais,
                revenu_conjoint_net=conjoint_revenu_net,
                parts_fiscales=parts
            )
        else:
            data = estimate_sasu_is_net_income_v3_with_ir(
                tjm=tjm,
                jours_facturés=jours,
                salaire_brut_annuel=salaire_brut,
                charges_fixes=compta + rc_pro,
                frais_deductibles=frais,
                revenu_conjoint_net=conjoint_revenu_net,
                parts_fiscales=parts
            )

        st.subheader("🧾 Freelance (SASU à l’IS)")
        if optimiser and "salaire_brut_optimisé" in data:
            st.write(f"🧮 Salaire brut optimisé : **{data['salaire_brut_optimisé']} €**")
        st.write(f"Salaire net : **{round(data['salaire_net'], 2)} €**")
        st.write(f"Dividendes nets : **{round(data['dividendes_nets'], 2)} €**")
        st.write(f"Impôt sur le revenu : **{round(data['impot_revenu_total'], 2)} €**")
        st.write(f"📊 TMI : **{int(data['tmi'] * 100)} %**")
        st.write(f"💶 Net final après tous impôts : **{round(data['net_final_apres_ir'], 2)} €**")
        st.write(f"💸 Super net mensuel : **{round(data['net_final_apres_ir'] / 12, 2)} €**")

        df = pd.DataFrame(list(data.items()), columns=["Poste", "Montant (€)"])
        df["Poste"] = df["Poste"].str.replace("_", " ").str.capitalize()
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        st.download_button(
            label="📥 Télécharger le résultat Excel",
            data=buffer.getvalue(),
            file_name="simulation_result.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if mode == "Salarié":
    show_employee()
elif mode == "Freelance (SASU)":
    show_freelancer()
else:
    emp_monthly = show_employee()

    st.markdown("---")
    show_freelancer()

    st.markdown("### 📊 Comparaison visuelle des régimes")

    # 1. Salarié
    net_salary = compute_net_salary(brut)
    net_employee = net_salary + conjoint_revenu_net
    impots_employee = compute_ir_employee(net_employee, parts)
    final_employee = net_employee - impots_employee
    monthly_employee = round(final_employee / 12, 2)

    # 2. Freelance IR
    data_ir = estimate_sasu_ir_net_income(
        tjm=tjm,
        jours_facturés=jours,
        salaire_annuel=7000,
        charges_fixes=compta + rc_pro,
        frais_deductibles=frais
    )
    total_ir = data_ir["revenu_net_avant_ir"] + conjoint_revenu_net
    impots_ir, _ = compute_impot_revenu(total_ir, parts)
    monthly_ir = round((total_ir - impots_ir) / 12, 2)

    # 3. Freelance IS optimisé
    data_is = optimise_salaire_vs_dividendes(
        tjm=tjm,
        jours_facturés=jours,
        charges_fixes=compta + rc_pro,
        frais_deductibles=frais,
        revenu_conjoint_net=conjoint_revenu_net,
        parts_fiscales=parts
    )
    monthly_is = data_is.get("super_net_mensuel", round(data_is["net_final_apres_ir"] / 12, 2))

    df = pd.DataFrame({
        "Régime": ["Salarié", "Freelance IR", "Freelance IS (opt.)"],
        "Net mensuel (€)": [monthly_employee, monthly_ir, monthly_is]
    })
    st.bar_chart(df.set_index("Régime"))

    # Résumé
    chiffre_affaires = tjm * jours
    st.markdown(f"#### 💼 Chiffre d'affaires total : **{round(chiffre_affaires)} €**")

    def pourcentage_diff(ref, val):
        return round(((val - ref) / ref) * 100, 2)

    diff_ir = pourcentage_diff(monthly_employee, monthly_ir)
    diff_is = pourcentage_diff(monthly_employee, monthly_is)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("📈 Écart IR vs Salarié", f"{diff_ir:+.2f} %")
    with col2:
        st.metric("📈 Écart IS vs Salarié", f"{diff_is:+.2f} %")
