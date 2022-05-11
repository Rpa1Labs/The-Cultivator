# The Cultivator

## INSTALLATION

---
### Nvidia Jetson Nano

---

Programmes requis:
```
g++
python3
python2
sudo

python2-pip
python3-pip
```


Librairies python 3 requises:
```
python-socketio
board
adafruit_bme680
adafruit_seesaw
```

Librairies python 2 requises:
```
cv2
```

Librairies C++ requises:
```
JetsonGPIO.h
```

Copiez-la dans le fichier `config-sample.json` et renommez-le en `config.json`

Complétez le fichier `config.json` avec les informations suivantes:
 - l'url de votre serveur web

Exécutez la commande suivante dans le dossier Jetson:
```sh
./install.sh
```

---

## Serveur Web

---

Programmes requis:
```
python3
screen
influxdb
sudo

python3-pip
```

Librairies python 3 requises:
```
influxdb_client
flask-socketio
flask
sqlite3
```

Sur influxdb, créez les buckets suivants:
```
Environnement_measures
Image
```

Ensuite, récupérez la clé API de votre compte influxdb

Copiez-la dans le fichier `config-sample.json` et renommez-le en `config.json`

Complétez le fichier `config.json` avec les informations suivantes:
 - la clé API de votre base InfluxDB (token)
 - l'url de votre base InfluxDB
 - le nom de l'organisation de votre base InfluxDB

Enfin, exécutez les commandes suivantes dans le dossier flask-server:
```sh
screen
sudo python3 serveur.py
``` 