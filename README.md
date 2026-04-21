## **Déploiement rapide d'une IA locale avec accès aux moteurs de recherche**


- **A QUOI CA SERT ?**

	- Ca sert à avoir des modèles d'IA open source en local capables de rechercher des infos sur internet, gratuitement, sans trop se fatiguer et en toute indépendance

	- Le moteur de recherche sera accessible indépendamment sur : http://localhost:8888 (ou n'importe quelle IP de votre réseau interne)  
		![](/img/1.png)
	- L'interface de chat IA sera accessible sur : http://localhost:8080 (ou n'importe quelle IP de votre réseau interne)  
		![](/img/2.png)


- **PREREQUIS :**
	- Avoir Docker installé : https://www.docker.com/
	- des modèles à placer dans le répertoire ```/models``` que vous pouvez trouver :
		- ici :  https://huggingface.co/prism-ml/collections
		- là : https://huggingface.co/mistralai/collections
		- où la (hop?) : https://huggingface.co/unsloth/collections


- **INITIALISATION :**
 	- Lorsque vous avez téléchargé vos modèles dans ```/models```, éditez le fichier ```/config/preset.ini``` pour faire correspondre les modèles avec leur mmproj (quand ils en ont un) afin de charger leur module vision
(c'est simple, vous leur donnez un petit nom d'alias et vous copiez/collez le nom des fichiers correspondant)  
![](/img/3.png)


- **INSTALLATION :**  
	 ```docker-compose up -d```


- **PARAMETRAGE :**
	- Dans les paramétrages accessibles par votre interface de chat IA, allez dans MCP > Add MCP Serveur et entrez l'adresse http://localhost:8000/mcp  
	![](/img/4.png)


- **MAINTENANCE :**
	- A chaque ajout/suppression de modèles, redémarrez le serveur avec la commande  
	 ```docker restart llama-serveur```


- **NOTE :**
	- Cette version fait tourner llama-server sur les GPU nvidia avec CUDA 13.1
vous pouvez adapter selon votre configuration (Mac OS, Linux, Windows) en choisissant ce qu'il vous plaît
	ici : https://github.com/ggml-org/llama.cpp/blob/master/docs/docker.md
	et en éditant la ligne ```image: ghcr.io/ggml-org/llama.cpp:server-cuda13``` du fichier ```docker-compose.yml```


- **TODO :**
	- Faire plus compliqué pour faire plus simple, comme un bon technocrate en technocratie