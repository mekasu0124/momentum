# Momentum

**Momentum** is a minimalist, cross-platform desktop application for journaling and task management, built with PySide6 (Qt for Python). It provides a clean, dark-themed interface to capture, track, and organize your daily tasks.

> ⚠️ **Note:** Momentum is currently in early development – expect frequent updates and improvements.

---

## ✨ Features

- **Add tasks** – quickly enter new tasks via a single input field.
- **View all tasks** – tasks are displayed in a scrollable list.
- **Mark as complete** – check a task to visually strike it through.
- **Delete tasks** – remove individual tasks with a single click.
- **Persistent storage** – tasks are saved locally in your home directory (`~/.momentum/tasks.json`).
- **Async operations** – all I/O runs in background threads to keep the UI responsive.
- **Dark theme** – a modern, purple‑accented dark theme that’s easy on the eyes.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- `uv` (recommended) or `pip` for package management

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/mek0124/momentum.git
   cd momentum
   ```

2. **Set up a virtual environment** (optional but recommended)

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

3. **Install the package in editable mode**

   ```bash
   uv pip install -e .
   # or, if using pip:
   pip install -e .
   ```

4. **Run the application**

   ```bash
   momentum
   ```

   On first launch, Momentum will ask for permission to read/write to its own storage directory. Grant it to proceed.

---

## 🧩 Usage

- **Add a task** – type your task in the input field at the bottom and press Enter or click **Save**.
- **Complete a task** – check the box next to a task to mark it as done (the text will be struck through).
- **Delete a task** – click the red **×** button next to any task to remove it permanently.
- **View all tasks** – the main window lists all saved tasks in reverse chronological order.

Tasks are automatically saved to `~/.momentum/tasks.json` – you can backup or migrate this file as needed.

---

## 🛠 Configuration

Momentum stores its configuration and data in:

- **App data**: `~/.momentum/`
- **Tasks file**: `~/.momentum/tasks.json`
- **Config file**: `~/.momentum/config.json` (stores user agreement preference)

No manual configuration is required – all settings are handled automatically.

---

## 📦 Project Structure

```
momentum/
├── pyproject.toml          # Project metadata and dependencies
├── README.md               # This file
├── src/
│   ├── __init__.py
│   ├── main.py             # Application entry point
│   ├── app/
│   │   └── app.py          # Main GUI (Momentum class)
│   ├── core/
│   │   ├── crud.py         # TaskRepository – file I/O
│   │   └── utils/
│   │       ├── async_helper.py
│   │       ├── async_worker.py
│   │       └── color_theme.py
│   ├── config.py           # Config class for user agreement
│   └── assets/
│       └── icon.png        # Application icon
└── .venv/                  # Virtual environment (not tracked)
```

---

## 🧪 Development

### Running tests

There are no automated tests yet – contributions to add test coverage are welcome!

### Building from source

To build a distributable wheel:

```bash
uv build
# or
python -m build
```

The wheel will be placed in `dist/`.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/mek0124/momentum).

Guidelines:

- Follow PEP 8 style.
- Ensure compatibility with Python 3.12+.
- Test your changes manually before submitting.

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

- **Author**: mekasu0124  
- **Email**: mek0124@proton.me  
- **Project Homepage**: [https://github.com/mek0124/momentum](https://github.com/mek0124/momentum)