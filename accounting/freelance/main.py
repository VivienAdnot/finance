from employee import compute_net_salary, compute_impot_revenu as compute_ir_employee
from freelancer_ir import estimate_sasu_ir_net_income
from freelancer_is import estimate_sasu_is_net_income_v3_with_ir, compute_impot_revenu
from exporter import export_result_to_excel, export_result_to_csv

import argparse

def compute_spouse_income(spouse_status, income_value):
    if spouse_status == "employee":
        return income_value * 12
    elif spouse_status == "freelance":
        return income_value
    else:
        raise ValueError("Statut du conjoint non reconnu. Utilisez 'employee' ou 'freelance'.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["employee", "freelance"], default="freelance")
    parser.add_argument("--regime", choices=["ir", "is"], default="ir")
    parser.add_argument("--brut", type=float)
    parser.add_argument("--spouse", choices=["employee", "freelance"], required=True)
    parser.add_argument("--spouse_income", type=float, required=True)
    parser.add_argument("--tjm", type=float, default=770)
    parser.add_argument("--jours", type=int, default=220)
    parser.add_argument("--frais", type=float, default=5000)
    parser.add_argument("--compta", type=float, default=2000)
    parser.add_argument("--rcpro", type=float, default=500)
    parser.add_argument("--salaire_brut", type=float, default=20000)
    parser.add_argument("--export", action="store_true")

    args = parser.parse_args()
    parts = 2
    conjoint_revenu_net = compute_spouse_income(args.spouse, args.spouse_income)

    if args.mode == "employee":
        if args.brut is None:
            raise ValueError("Argument --brut requis en mode 'employee'")
        net_salary = compute_net_salary(args.brut)
        total_net = net_salary + conjoint_revenu_net
        impots = compute_ir_employee(total_net, parts)
        after_tax = total_net - impots

        print("\n=== Salarié ===")
        print(f"Salaire net : {round(net_salary, 2)} €")
        print(f"Foyer net avant IR : {round(total_net, 2)} €")
        print(f"Impôt sur le revenu : {round(impots, 2)} €")
        print(f"Net final : {round(after_tax, 2)} €")

    else:
        charges_fixes = args.compta + args.rcpro

        if args.regime == "ir":
            result = estimate_sasu_ir_net_income(
                tjm=args.tjm,
                jours_facturés=args.jours,
                salaire_annuel=7000,
                charges_fixes=charges_fixes,
                frais_deductibles=args.frais,
            )
            total_net = result["revenu_net_avant_ir"] + conjoint_revenu_net
            impots, _ = compute_impot_revenu(total_net, parts)
            after_tax = total_net - impots

            print("\n=== SASU à l’IR ===")
            print(f"Revenu net avant IR (freelance) : {round(result['revenu_net_avant_ir'], 2)} €")
            print(f"Foyer net avant IR : {round(total_net, 2)} €")
            print(f"Impôt sur le revenu : {round(impots, 2)} €")
            print(f"Net final : {round(after_tax, 2)} €")

            if args.export:
                export_result_to_csv({
                    "revenu_net_avant_ir": result["revenu_net_avant_ir"],
                    "revenu_net_total_foyer": total_net,
                    "impot_revenu_total": impots,
                    "net_final_apres_ir": after_tax
                })
                export_result_to_excel(result)
                print("📁 Résultat exporté en CSV et Excel.")

        elif args.regime == "is":
            result = estimate_sasu_is_net_income_v3_with_ir(
                tjm=args.tjm,
                jours_facturés=args.jours,
                salaire_brut_annuel=args.salaire_brut,
                charges_fixes=charges_fixes,
                frais_deductibles=args.frais,
                revenu_conjoint_net=conjoint_revenu_net,
                parts_fiscales=parts
            )

            print("\n=== SASU à l’IS ===")
            print(f"Salaire net : {round(result['salaire_net'], 2)} €")
            print(f"Dividendes nets : {round(result['dividendes_nets'], 2)} €")
            print(f"Impôt sur le revenu : {round(result['impot_revenu_total'], 2)} €")
            print(f"TMI du foyer : {int(result['tmi'] * 100)} %")
            print(f"💶 Net final après tous impôts : {round(result['net_final_apres_ir'], 2)} €")

            if args.export:
                export_result_to_csv(result)
                export_result_to_excel(result)
                print("📁 Résultat exporté en CSV et Excel.")

if __name__ == "__main__":
    main()
