# Fonctionnement des modules

## Types de modules

### wireless
#### constructor(\<port>, \<vitesse>, \<région>, \<mode>, \<callback réception>)
- port: Le port sériel pour ce connecter au modem.
- vitesse: Vitesse de la connection sériel.
- région: La région pour la selection de fréquence.
- mode: Envoi (tx) ou Réception (rx)
- callback réception [ foo(msg_reçu) ]: Fonction à appeler avec les messages reçus, Null si mode envoi.
- module is initialised but not connected.

#### send_data(data)
- data: Les données à envoyer.
- retourne une erreur si le module n'est pas en mode envoi.

#### disconnect()
- ferme the module.

#### connect()
- démarre the module

#### configure(port=\<port>, rate=\<vitesse>, region=\<région>, mode=\<mode>, callback=\<callback réception>)
- tous les paramètres sont optionels.
- modifie la configuration du module (voir constructeur)