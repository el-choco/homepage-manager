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