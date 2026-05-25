# 🛠️ Homepage Config Manager

Eine leichtgewichtige, sichere Webanwendung, die mit Python und Flask entwickelt wurde, um Konfigurationsdateien für das [Homepage Dashboard](https://github.com/gethomepage/homepage) zu verwalten, zu bearbeiten und zu orchestrieren. Sie bietet sowohl eine ansprechende, visuelle Rasterdarstellung deines Setups als auch schnelle Aktionen, um Konfigurationen anzupassen, ohne die Strukturen zu beschädigen.

## ✨ Features

* 🗂️ **Multi-Datei-Verwaltung:** Nahtloser Wechsel zwischen `services`, `settings`, `widgets`, `bookmarks`, `docker`, `kubernetes` und `proxmox`.
* 🪄 **Intelligente Vorlagen:** Integrierte Dropdown-Menüs mit offiziellen Code-Vorlagen, um Nodes (Knotenpunkte) sofort und ohne Syntaxfehler hinzuzufügen.
* 📝 **Custom Assets Editor:** Direkte Textgestaltung über integrierte Editoren für `custom.css` und `custom.js`.
* 🔒 **Sicherheitsebene:** Integrierter Authentifizierungsmechanismus, um unbefugte Änderungen an den Konfigurationsdateien zu verhindern.
* 🐳 **Docker Native:** Vollständig containerisierte Architektur, die darauf ausgelegt ist, direkt neben deinem aktiven Homepage-Container zu laufen.

## 🚀 Schnellstart

### 1. Dateistruktur
Stelle sicher, dass dein Bereitstellungsverzeichnis die erforderlichen Anwendungskomponenten enthält:

```text
homepage-manager/
├── app.py
├── Dockerfile
├── docker-compose.yml
└── templates/
    ├── index.html
    └── login.html
```

### 2. Docker Compose Deployment
Nutze das untenstehende Bereitstellungs-Snippet, um den Manager zu starten. Achte darauf, den Pfad zu deinem tatsächlichen Homepage-Konfigurationsverzeichnis korrekt zuzuordnen.

```yaml
services:
  homepage-manager:
    image: paquele/homepage-manager:latest
    container_name: homepage-manager
    ports:
      - "3335:3335"
    volumes:
      - /path/to/homepage/config:/app
    working_dir: /app
    environment:
      - APP_USER=admin
      - APP_PASS=changeme
      - SECRET_KEY=change_this_to_a_random_string
    restart: unless-stopped
```

## ⚙️ Umgebungsvariablen

| Variable | Beschreibung | Standardwert |
| :--- | :--- | :--- |
| `APP_USER` | Der Benutzername, der für die Anmeldung auf der Weboberfläche erforderlich ist. | `admin` |
| `APP_PASS` | Das Passwort, das für die Anmeldung auf der Weboberfläche erforderlich ist. | `changeme` |
| `SECRET_KEY` | Verschlüsselungszeichenfolge, die zur Sicherung der Sitzungsdaten verwendet wird. | `change_this_to_a_random_string` |

## 📂 Volume-Zuweisung

| Container-Pfad | Host-Pfad | Zweck |
| :--- | :--- | :--- |
| `/app` | `/path/to/homepage/config` | Enthält die aktiven `.yaml`, `.css` und `.js` Homepage-Dateien. |

## 🛠️ Lokale Build-Anleitung

Wenn du es vorziehst, den Container lokal aus den Quelldateien zu erstellen, anstatt ihn vom Docker Hub zu ziehen, verwende:

```bash
docker compose up -d --build
``` 
   

 ---

# 🛠️ Homepage Config Manager

A lightweight, secure web application built with Python and Flask to manage, edit, and orchestrate configuration files for the [Homepage Dashboard](https://github.com/gethomepage/homepage). It provides both a beautiful visual grid representation of your setup and quick actions to modify configs without breaking structures.

## ✨ Features

* 🗂️ **Multi-File Management:** Seamlessly switches between `services`, `settings`, `widgets`, `bookmarks`, `docker`, `kubernetes`, and `proxmox`.
* 🪄 **Smart Templates:** Built-in dropdown menus with official code templates to instantly add nodes without syntax errors.
* 📝 **Custom Assets Editor:** Direct text styling via integrated editors for `custom.css` and `custom.js`.
* 🔒 **Security Layer:** Built-in authentication mechanism to prevent unauthorized modification of configuration files.
* 🐳 **Docker Native:** Fully containerized architecture designed to run directly alongside your active homepage container.

## 🚀 Quick Start

### 1. File Structure
Ensure your deployment directory contains the necessary application components:

```text
homepage-manager/
├── app.py
├── Dockerfile
├── docker-compose.yml
└── templates/
    ├── index.html
    └── login.html
```

### 2. Docker Compose Deployment
Use the deployment snippet below to run the manager. Make sure to map the path to your actual homepage configuration directory.

```yaml
services:
  homepage-manager:
    image: paquele/homepage-manager:latest
    container_name: homepage-manager
    ports:
      - "3335:3335"
    volumes:
      - /path/to/homepage/config:/app
    working_dir: /app
    environment:
      - APP_USER=admin
      - APP_PASS=changeme
      - SECRET_KEY=change_this_to_a_random_string
    restart: unless-stopped
```

## ⚙️ Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `APP_USER` | The username required to log into the web interface. | `admin` |
| `APP_PASS` | The password required to log into the web interface. | `changeme` |
| `SECRET_KEY` | Encryption string used to secure session data. | `change_this_to_a_random_string` |

## 📂 Volume Mapping

| Container Path | Host Path | Purpose |
| :--- | :--- | :--- |
| `/app` | `/path/to/homepage/config` | Contains live `.yaml`, `.css`, and `.js` homepage files. |

## 🛠️ Local Build Instructions

If you prefer to build the container locally from the source files instead of pulling from Docker Hub, use:

```bash
docker compose up -d --build
```