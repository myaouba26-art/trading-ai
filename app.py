from quotexpy import Quotex

# Connexion en mode démo (attention : change email et mot de passe par un compte démo !)
email = "ton_email_demo@exemple.com"
password = "ton_mot_de_passe_demo"

try:
    qx = Quotex(email, password)
    qx.connect()
    
    if qx.check_connect():
        print("✅ Connexion réussie au compte Quotex (mode démo).")
    else:
        print("❌ Échec de connexion.")
except Exception as e:
    print("Erreur :", e)