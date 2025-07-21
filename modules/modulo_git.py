import os
import subprocess

def salva_su_git(commit_msg="🔄 Aggiornamento automatico da WFL 9.0"):
    try:
        # Configura utente Git solo se non già configurato
        subprocess.run(["git", "config", "--global", "user.name", "wfl-bot"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "bot@wfl9.app"], check=True)

        # Verifica esistenza dei file prima di aggiungerli
        files_da_salvare = [
            "dati/storico.csv",
            "dati/diario.txt",
            "dati/memoria_errori.csv",
            "dati/memoria_successi.csv",
            "dati/entropie.csv"
        ]

        for file in files_da_salvare:
            if os.path.exists(file):
                subprocess.run(["git", "add", file], check=True)

        # Commit (solo se ci sono modifiche)
        subprocess.run(["git", "diff", "--cached", "--quiet"])
        if subprocess.call(["git", "diff", "--cached", "--quiet"]) != 0:
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        else:
            print("ℹ️ Nessuna modifica da committare.")
            return True

        # Recupera il token GitHub dalle variabili d'ambiente
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("❌ TOKEN mancante. Imposta GITHUB_TOKEN tra le variabili d’ambiente.")
            return False

        # Ottiene URL remoto e inietta il token
        repo_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode().strip()
        auth_url = repo_url.replace("https://", f"https://{token}@")

        # Push
        subprocess.run(["git", "push", auth_url], check=True)

        print("✅ Salvataggio completato su GitHub.")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Errore Git (comando): {e}")
        return False

    except Exception as e:
        print(f"❌ Errore generale: {e}")
        return False
