import os
import subprocess
from datetime import datetime

def salva_su_git(commit_msg="🔄 Aggiornamento automatico da WFL 9.0"):
    try:
        # Configura Git (solo se non già configurato)
        subprocess.run(["git", "config", "--global", "user.name", "wfl-bot"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "bot@wfl9.app"], check=True)

        # Aggiunge tutti i file nella cartella dati/
        for file in os.listdir("dati"):
            filepath = os.path.join("dati", file)
            if os.path.isfile(filepath):
                subprocess.run(["git", "add", filepath], check=True)

        # Verifica se ci sono modifiche
        modifiche = subprocess.call(["git", "diff", "--cached", "--quiet"])
        if modifiche != 0:
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        else:
            print("ℹ️ Nessuna modifica da committare.")
            return True

        # Prende il token da variabili d’ambiente
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("❌ TOKEN mancante. Imposta GITHUB_TOKEN tra le variabili d’ambiente.")
            return False

        # Recupera URL e inietta token
        repo_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode().strip()
        if not repo_url.startswith("https://"):
            print("❌ Il repository deve usare HTTPS, non SSH.")
            return False
        auth_url = repo_url.replace("https://", f"https://{token}@")

        # Esegue push
        subprocess.run(["git", "push", auth_url], check=True)

        # Scrive log nel diario
        log_entry = f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] ✅ Dati salvati su GitHub con commit: \"{commit_msg}\"\n"
        with open("dati/diario.txt", "a", encoding="utf-8") as f:
            f.write(log_entry)

        print("✅ Salvataggio completato su GitHub.")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Errore Git (comando fallito): {e}")
        return False

    except Exception as e:
        print(f"❌ Errore generale: {e}")
        return False
