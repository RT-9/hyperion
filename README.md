
# Hyperion – A reactive, MCP, open-source DMX orchestrator.

![GitHub License](https://img.shields.io/github/license/Arian-Ott/hyperion)
[![Made with Python](https://img.shields.io/badge/Python->=3.14-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")
![Static Badge](https://img.shields.io/badge/mariadb-%3E%3D11.4-blue?logo=mariadb)
![Static Badge](https://img.shields.io/badge/redis-%3E%3D8.2.2-red?logo=redis)
![Frontend](https://img.shields.io/badge/frontend-Svelte-orange)
![Status](https://img.shields.io/badge/status-Alpha-red)

## The Why

The lighting control industry is currently dominated by expensive, proprietary ecosystems that often enforce artificial limitations through hardware dongles and closed-source software. Many existing solutions are built upon legacy architectural patterns—monolithic C++ codebases that have been ported forward for decades without rethinking the underlying data flow.

**Hyperion** was developed to apply modern backend engineering principles to DMX512, shifting away from "black box" controllers towards a transparent, reactive engine that prioritises data integrity and architectural freedom.

## The Problem: Proprietary Lock-in & Legacy Loops

* Hardware Entrapment: Most entry-level controllers are non-functional without specific, vendor-locked interfaces, creating a "pay-to-play" barrier for creators. If the vendor discontinues the proprietary software, your physical device is electric trash.
* Architectural Opacity: Proprietary software and the lack of APIs prevents you to use your DMX devices outside the scope of lighting consoles without expensive inefficient tweaks.
* Limited amount of customisation: Once you buy a lightning console or software, you have a very outdated complicated UI which requires a lot of effort to learn. Customising the UI or behaviour of the console to your workflow is only possible to some extend. 
* Super expensive hardware: Mid-level lightning controllers cost around 700-2000€. High-End controllers can cost well above 65.000€ (excluding shipping, ofc :D ). Cheaper options below 700€ exists but they come with massive drawbacks and limitations which make them less attractive to use at a party or small event.

## The Solution: A Reactive Orchestrator

Hyperion was born to prove that building a lighting software does not require expensive tech. 





## ✨ Features

* **Modern Interface:** Touch-first web UI built with Svelte & Vite.
* **Distributed Architecture:** Run the backend on your laptop and the DMX output on a Raspberry Pi over the network.
* **Hardware Agnostic:** Supports ArtNet, sACN, USB-DMX (Enttec/uDMX), and direct GPIO (Raspberry Pi).
* **API First:** Full control via REST API and WebSockets (FastAPI).

## 🚀 Architecture

Hyperion consists of two main components:

1.  **Core (Brain):** Manages the database, API, and lighting logic.
2.  **Node (Runner):** A lightweight service that receives frame data and outputs DMX signals.

## 🛠️ Installation (Development)

### Prerequisites
* Python 3.14+
* Node.js & npm
* uv or standard pip

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
pip install .

```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev

```

## 📄 License

Hyperion is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License version 3** or (at your option) any later version.

See [LICENSE](https://www.google.com/search?q=LICENSE) for more details.

## FAQ

### 1 Why Python 3.14?

Why not? Running $\pi$ on a Pi is just fun.



## 💬 Community & Support

* **Found a bug?** Open an [Issue](https://github.com/Arian-Ott/hyperion/issues).
* **Have a feature request?** Start a [Discussion](https://github.com/Arian-Ott/hyperion/discussions).
* **Security vulnerability?** See [SECURITY.md](SECURITY.md).