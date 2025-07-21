import os
import subprocess

def salva_su_git(commit_msg="🔄 Aggiornamento automatico da WFL 9.0"):
    try:
        # Configura utente Git
        subprocess.run(["git", "config", "user.name", "wfl-bot"], check=True)
        subprocess.run(["git", "config", "user.email", "bot@wfl9.app"], check=True)

        # Aggiunge i file modificati
        subprocess.run(["git", "add", "dati/storico.csv"], check=True)
        subprocess.run(["git", "add", "dati/diario.txt"], check=True)
        subprocess.run(["git", "add", "dati/memoria_errori.csv"], check=True)
        subprocess.run(["git", "add", "dati/memoria_successi.csv"], check=True)
        subprocess.run(["git", "add", "dati/entropie.csv"], check=True)

        # Commit
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)

        # Recupera token e URL remoto
        token = os.getenv("GITHUB_TOKEN")
        repo_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode().strip()
        auth_url = repo_url.replace("https://", f"https://{token}@")

        # Push su GitHub
        subprocess.run(["git", "push", auth_url], check=True)

        print("✅ Salvataggio automatico su GitHub completato.")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Errore Git: {e}")
        return False

    except Exception as e:
        print(f"❌ Errore generale: {e}")
        return False
