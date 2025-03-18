

If you're using a **Windows system** and want to run **Milvus Standalone** in Docker you can use **Docker Desktop for Windows**, which integrates with WSL2 behind the scenes. 

#  Run Milvus Standalone in Docker on Windows

This guide explains how to set up and run **Milvus Standalone** in Docker on a **Windows system**. Docker Desktop for Windows will be used, which integrates with WSL2 for better performance.

## Prerequisites

1. **Windows 10 version 2004 or higher**, or **Windows 11**.
2. **WSL2** installed and enabled.
3. **Docker Desktop** installed and configured to use WSL2.

### Enable WSL2 and Install Docker Desktop


## Steps to Check if WSL2 Distro is Available in Docker

### 1. Verify WSL2 Installation

First, ensure that WSL2 is installed and enabled on your system.

1. Open PowerShell as an Administrator.
2. Run the following command to check the WSL version:

   ```powershell
   wsl --list --verbose
    ```
   This will list all installed WSL distributions along with their versions. Ensure that at least one distribution is set to WSL2 (version 2).

   Example output:

   ```
   NAME      STATE           VERSION
   * Ubuntu    Running         2
   ```

   If no distributions are listed or the version is not 2, you may need to install or upgrade WSL2.

### 2. Verify Docker Desktop WSL2 Integration

Next, ensure that Docker Desktop is configured to use WSL2.

1. Open Docker Desktop.
2. Go to **Settings** > **General**.
3. Ensure that the option **Use the WSL 2 based engine** is checked.
4. Go to **Settings** > **Resources** > **WSL Integration**.
5. Verify that your WSL2 distribution (e.g., Ubuntu) is enabled for integration with Docker.

## Troubleshooting

- **WSL2 Not Installed**: If WSL2 is not installed, follow the [official Microsoft guide](https://docs.microsoft.com/en-us/windows/wsl/install) to install it.
- **Docker Desktop Not Using WSL2**: Ensure that Docker Desktop is configured to use the WSL2 backend in the settings.
- **Docker Command Not Found in WSL2**: Ensure that Docker Desktop is running and that the WSL2 integration is enabled for your distribution.

## Conclusion

By following these steps, you should be able to verify if a WSL2 distribution is available and properly configured for use with Docker on your PC. If everything is set up correctly, you can now use Docker seamlessly within your WSL2 environment.

For further assistance, refer to the official documentation:

- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [Docker Desktop WSL2 Backend](https://docs.docker.com/docker-for-windows/wsl/)


2. **Install Docker Desktop**:
   - Download Docker Desktop from the [official website](https://www.docker.com/products/docker-desktop).
   - During installation, ensure that the option **Use the WSL 2 based engine** is checked.
   - After installation, open Docker Desktop and go to **Settings** > **Resources** > **WSL Integration**.
   - Enable integration with your WSL2 distribution (e.g., Ubuntu).

3. **Verify Docker Installation**:
   - Open PowerShell or Command Prompt and run:
     ```powershell
     docker --version
     
   - This should display the Docker version installed.

---

## Steps to Run Milvus Standalone in Docker

### 1. Pull the Milvus Standalone Docker Image

1. Open PowerShell or Command Prompt.
2. Pull the Milvus Standalone Docker image:
   ```powershell
   docker pull milvusdb/milvus:v2.3.3
   ```
   > Replace `v2.3.3` with the latest version of Milvus if needed.

### 2. Run the Milvus Standalone Container

1. Run the Milvus Standalone container:
   ```powershell
   docker run -d --name milvus-standalone `
     -p 19530:19530 `
     -p 9091:9091 `
     milvusdb/milvus:v2.3.3
   ```
   - `-d`: Runs the container in detached mode.
   - `--name milvus-standalone`: Names the container.
   - `-p 19530:19530`: Exposes the Milvus service port.
   - `-p 9091:9091`: Exposes the metrics port.

2. Verify that the container is running:
   ```powershell
   docker ps
   ```
   You should see the `milvus-standalone` container in the list.

---

### 3. Access Milvus Standalone

1. Milvus will be accessible on `localhost:19530` from your Windows system.
2. You can use tools like **Postman** or any Milvus client SDK to interact with the Milvus service.

---

### 4. Stop and Remove the Container (Optional)

If you need to stop or remove the container:

1. Stop the container:
   ```powershell
   docker stop milvus-standalone
   ```

2. Remove the container:
   ```powershell
   docker rm milvus-standalone
   ```

---

## Troubleshooting

- **Docker Desktop Not Running**: Ensure Docker Desktop is running in the background.
- **Port Conflicts**: Ensure ports `19530` and `9091` are not in use by other applications.
- **WSL2 Not Enabled**: If WSL2 is not enabled, follow the [official Microsoft guide](https://docs.microsoft.com/en-us/windows/wsl/install) to enable it.

---

## Conclusion

You have successfully set up and run **Milvus Standalone** in Docker on your Windows system. This setup leverages Docker Desktop's integration with WSL2 for optimal performance.

For more information, refer to the official documentation:

- [Milvus Documentation](https://milvus.io/docs)
- [Docker Desktop for Windows](https://docs.docker.com/docker-for-windows/)

### Key Changes for Windows:
1. Removed the need to explicitly use WSL2 Ubuntu terminal.
2. Used PowerShell commands for Docker operations.
3. Emphasized Docker Desktop's integration with WSL2 for seamless performance.
4. Simplified the setup process for Windows users.




---
# ---- Code Quality Guidelines ----

## Overview

This repository is designed to maintain **production-grade quality** with a strong emphasis on:

- **Explicit Error Handling**: No silent failures; all errors should be handled appropriately.
- **Performance Logging**: Use a structured logger to track execution time and system performance.
- **Best Practices**: Follow industry standards for maintainability, readability, and scalability.



## Code Quality Standards

### 1. Explicit Error Handling

- Always **catch and handle** exceptions explicitly.
- Use **custom error classes** where applicable.
- Avoid **empty except blocks**; log meaningful messages instead.
- Use **context managers** (e.g., `with open() as file:`) to prevent resource leaks.
- Raise specific exceptions rather than generic ones (e.g., `ValueError`, `KeyError` instead of `Exception`).

---

### 2. Performance Logging

- Use a **dedicated logger** (use `logger` module from utils).
- Log execution time for performance-critical functions.
- Use **structured logging** to allow filtering and analysis.
- Avoid excessive logging in high-frequency code paths.


### 3. General Best Practices

- **Code Style**: Follow [PEP 8](https://peps.python.org/pep-0008/) for Python, or relevant style guides for other languages.
- **Type Hints**: Use type annotations for clarity (`def func(x: int) -> str:`).
- **Unit Tests**: Maintain **high test coverage** using `pytest` or similar frameworks.
- **Modular Code**: Follow **Single Responsibility Principle (SRP)**.
- **requirements file** : write all the libraries installed in `requirements.txt` file. (eg. `langchain=0.4.38`)
- **Documentation**: Every function should have a clear docstring.
- **Security**: Avoid hardcoded secrets; use environment variables instead.

---

## Recommended Tools

- **Linters & Formatters**: `black`, `flake8`, `pylint` (for Python)
- **Logging Frameworks**: use `logger` from the utils (`.error` for error logging , `log` for success logging)
- **Performance Monitoring**: `cProfile`, `Prometheus`, `New Relic`
- **Testing**: `pytest` idk how to use this but we will figure it out.
- **Static Analysis**: `mypy` (for type checking)

---

## ------------- Contribution Guidelines -------------

1. Follow the **coding standards** mentioned above.
2. Ensure all changes are **well-tested** before submitting PRs.
3. Provide **clear commit messages** and **meaningful comments**.
4. Run linters and formatters before pushing code.




# Project Setup Guide

## Prerequisites

Before running this project, make sure you have the following installed:

- **Python 3.10.11** (Check version: `python --version`)
- **pip (Python package manager)** (Check version: `pip --version`)
- **Virtual Environment (Recommended)**

---

## 1. Install Dependencies

It's recommended to use a virtual environment to keep dependencies isolated.

### Using `venv`
```sh
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

---

## 2. Setup Environment Variables

This project uses environment variables to manage sensitive information.  
A sample `.env_example` file is provided—copy it and rename it to `.env`:

```sh
cp .env_example .env
```

### Editing the `.env` file

Open `.env` in a text editor and replace placeholder values with actual configuration.

Example `.env_example`:
```ini
# Database Configurations
DB_HOST=localhost
DB_PORT=5432
DB_USER=username
DB_PASSWORD=password
DB_NAME=my_database

# Secret Keys
SECRET_KEY=your_secret_key_here

```

Make sure **not to commit the `.env` file** to version control.

---

## 3. Running the Project

After setting up dependencies and environment variables, you can run the project:

```sh
there is still no starting point will update it soon
```

---

## 4. Additional Tools

- **Managing Dependencies**:  
  To update `requirements.txt` after adding new dependencies:
  ```sh
  pip freeze > requirements.txt
  ```
- **Environment Management**:  
  Use `direnv` or `dotenv` to automatically load environment variables.

---

## 5. Troubleshooting

- If dependencies fail to install, ensure you have the correct Python version.
- If `.env` variables are not being loaded, install `python-dotenv`:
  ```sh
  pip install python-dotenv
  ```
- Use `print(os.getenv("VARIABLE_NAME"))` to debug missing environment variables.

---




---

# ------- Contribution Guidelines -------------

## 🔹 Git Workflow
To maintain **code quality and stability**, follow this Git workflow:

# ------- MUST READ -------------
1. **No direct commits to the `main` branch** 🚫  
2. **Create your own branch** from `develop`  
3. **Always create a feature branch** from the develop branch using the format:` user/feature_name` (e.g., **ajmeer/milvus_dbinsertion**).
3. **Always create a feature branch** from the develop branch using the format:` user/test/test_feature` (e.g., **ajmeer/test/milvus_dbinsertion**).
3. **if it is a bug fix create a branch** from the develop branch using the format:` user/bugfix/bugname` (e.g., **ajmeer/bugfix/milvus_connection**).
4. **This branch is dedicated** to writing code for the specific **feature** mentioned in its name. (eg: `ajmeer/milvus_insetion`  in this you will only write code related to milvus_insertion)
5. **Commit after implementing each function** for better tracking  
6. **Once the feature** is completed, push the branch to the remote repository.
7. **Create a Pull Request (PR)** to merge the feature branch into `develop`.
8. **After merging** do not modify the old branch—consider it finalized.
9. **Start a new feature** by creating a fresh branch from develop
5. **After testing is completed**, it will be merged into `main`  

---

## 🔹 How to Contribute

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/WhiteboxHub/milvus_custom_retriver.git
cd milvus_custom_retriver
```

### 2️⃣ Create a New Branch (from `develop`)
```sh
git checkout develop
git pull origin develop  # Ensure it's up to date
git checkout -b user/my-new-feature
```

### 3️⃣ Commit After Each Function Implementation
```sh
git add my_file.py
git commit -m "Added function X to handle Y"
git push origin user/my-new-feature
```

### 4️⃣ Create a Pull Request (PR)
- Open a PR **from your branch → `develop` branch**  
- Wait for **code review and testing**  
- Once approved, it will be merged into `main` after validation ✅  

---

## 🔹 Additional Guidelines

- **Write meaningful commit messages** (e.g., `Fixed bug in X` instead of `Fixed something`)
- **Run tests before pushing your code**
- **Use feature branches** (e.g., `user/add-login`, `user/bugfix/fix-db-connection`)
- **Keep PRs small & focused** (avoid merging too many changes at once)
- **One feature in one PR** every `PR` should only contain one feature or one Bug solution. if there are more then one feature in a `PR` it will rejected.

---

## 🔹 Example Workflow

```sh
# Step 1: Switch to testing branch & pull latest changes
git checkout testing
git pull origin testing

# Step 2: Create a new feature branch
git checkout -b feature/improve-logging

# Step 3: Write code and commit after each function
git add logging_utils.py
git commit -m "Added structured logging for API requests"

# Step 4: Push your branch
git push origin feature/improve-logging

# Step 5: Open a Pull Request (PR) to `testing`
```

---

Following this workflow ensures **clean version control, better testing, and high-quality production code**. 🚀  

Happy coding! 🎉  




---

# Testing Instructions

## 1️⃣ Preparing for the Test

Before running the test, ensure you follow these steps:

- **Uncomment lines 87 and 88** in `src/milvus_client.py`
- **Clear logs** from the `log/` folder
- **Start Milvus using Docker** (for the first test)

---

## 2️⃣ Running the Test

### ✅ **Test with Milvus Running**
1. **Start Milvus with Docker**  
   If Milvus is not already running, start it with:
   ```sh
   docker run -d --name milvus \
     -p 19530:19530 \
     milvusdb/milvus:v2.3.4
   ```
   
2. **Run the Milvus Client**
   ```sh
   python src/milvus_client.py
   ```
   
3. **Check the Log File**  
   - Navigate to the `log/` folder
   - Open the latest log file  
   - Confirm that the **connection to Milvus is logged**

---

### ❌ **Test with Milvus Stopped**
1. **Stop the Milvus Docker Container**  
   ```sh
   docker stop milvus && docker rm milvus
   ```
   
2. **Run the Milvus Client Again**
   ```sh
   python src/milvus_client.py
   ```

3. **Check the Log File**  
   - Verify that the log **records the connection failure** properly.

---

## 3️⃣ Expected Results

| Scenario                 | Expected Log Output |
|--------------------------|--------------------|
| ✅ Milvus Running | `"Connected to Milvus at <IP>:19530"` |
| ❌ Milvus Stopped | `"Failed to connect to Milvus"` |

**If the expected logs do not appear**, check the following:
- Ensure logging is enabled in `src/milvus_client.py`
- Verify that lines 87 and 88 are uncommented
- Run the script in a **virtual environment** with dependencies installed (`pip install -r requirements.txt`)

---

Following this process ensures that the **Milvus client is properly logging connection attempts**. 🚀  
Let me know if you want to modify or add anything! 😊  

