"""Demonstra o envio do relatorio Excel por e-mail via smtplib.

Modo padrao: dry-run (dry_run=True). O script apenas imprime o que seria
enviado - nenhum e-mail real e disparado. So envia de verdade quando
chamado com --send (ou dry_run=False diretamente) E as variaveis de
ambiente SMTP_HOST, SMTP_USER, SMTP_PASSWORD e REPORT_RECIPIENT estiverem
todas presentes. Sem isso, o envio real e recusado com uma mensagem clara.

Uso:
    python src/email_report.py                # dry-run (padrao, seguro)
    python src/email_report.py --send          # envio real (requer env vars)
"""
import argparse
import os
import smtplib
from email.message import EmailMessage

REQUIRED_ENV_VARS = ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "REPORT_RECIPIENT")


def send_report(attachment_path: str, dry_run: bool = True) -> None:
    subject = "Relatorio de Vendas"
    body = "Segue em anexo o relatorio de vendas gerado automaticamente."

    env = {var: os.environ.get(var) for var in REQUIRED_ENV_VARS}
    missing = [var for var, value in env.items() if not value]

    if dry_run:
        print("[DRY RUN] Nenhum e-mail sera enviado de verdade.")
        print(f"[DRY RUN] De: {env['SMTP_USER'] or '(SMTP_USER nao definido)'}")
        print(f"[DRY RUN] Para: {env['REPORT_RECIPIENT'] or '(REPORT_RECIPIENT nao definido)'}")
        print(f"[DRY RUN] Assunto: {subject}")
        print(f"[DRY RUN] Anexo: {attachment_path}")
        return

    if missing:
        raise RuntimeError(
            "Envio real solicitado, mas faltam variaveis de ambiente: "
            + ", ".join(missing)
            + ". Defina-as ou rode em modo dry-run."
        )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = env["SMTP_USER"]
    msg["To"] = env["REPORT_RECIPIENT"]
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=os.path.basename(attachment_path),
        )

    with smtplib.SMTP(env["SMTP_HOST"]) as smtp:
        smtp.starttls()
        smtp.login(env["SMTP_USER"], env["SMTP_PASSWORD"])
        smtp.send_message(msg)
    print(f"E-mail enviado para {env['REPORT_RECIPIENT']}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--send", action="store_true", help="Envia de verdade (padrao: dry-run).")
    parser.add_argument(
        "--attachment",
        default=os.path.join(os.path.dirname(__file__), "relatorio_vendas.xlsx"),
        help="Caminho do relatorio a anexar.",
    )
    args = parser.parse_args()
    send_report(args.attachment, dry_run=not args.send)


if __name__ == "__main__":
    main()
