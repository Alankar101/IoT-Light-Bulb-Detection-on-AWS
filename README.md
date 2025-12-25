# 🚀 IoT Light Bulb Detection Web Application (Demo Only)

---

### 📌 **Project Goal (Demo Purpose Only):**

This project demonstrates how to deploy a **Python Flask–based IoT application** on an **AWS EC2 instance**.
It focuses on **application deployment, process management, and basic cloud hosting**, not on production readiness.

> ⚠️ **This project is strictly for demo / learning purposes only.**

---

### 🔑 **Prerequisites**

Before running this project, ensure you have:

✅ AWS Account
✅ EC2 Instance (Amazon Linux / Ubuntu)
✅ SSH access to EC2
✅ Python 3 installed
✅ Basic Linux command knowledge

---

### 📁 **Project Structure**

```
iot-light-bulb-detection/
├── app.py
├── light_detector.py
├── requirements.txt
├── templates/
├── static/
├── README.md
```

---

### ⚙️ **Technologies Used**

* **Python 3**
* **Flask**
* **OpenCV**
* **Gunicorn**
* **Linux**
* **AWS EC2**

---

### 🔧 **Setup Instructions**

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/USERNAME/iot-light-bulb-detection.git
cd iot-light-bulb-detection
```

---

#### 2️⃣ Create Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

#### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### ▶️ **Run the Application**

#### Option 1: Run normally (demo / testing)

```bash
python app.py
```

Access the application at:

```
http://<EC2_PUBLIC_IP>:5000
```

---

#### Option 2: Run in background using `nohup`

```bash
nohup python3 app.py > output.log 2>&1 &
```

Check logs:

```bash
tail -f output.log
```

---

#### Option 3: Run using Gunicorn (recommended demo setup)

```bash
gunicorn --bind 0.0.0.0:5000 app:app --daemon
```

---

### 🔐 **AWS Security Group Configuration**

Allow the following inbound rules:

| Type       | Port | Source    |
| ---------- | ---- | --------- |
| SSH        | 22   | Your IP   |
| Custom TCP | 5000 | 0.0.0.0/0 |

---

### ⚠️ **Important Notes (Demo Limitations)**

* AWS EC2 **does not have a physical camera**
* OpenCV camera detection (`VideoCapture(0)`) **will not work on EC2**
* This project is intended to:

  * Demonstrate Flask deployment
  * Show background execution (`nohup`, `gunicorn`)
  * Practice cloud hosting concepts

For full functionality, run this project on:

* Local machine
* System with webcam
* IP camera–enabled environment

---

### 🧹 **.gitignore (Recommended)**

```
venv/
myenv/
__pycache__/
*.pyc
nohup.out
output.log
```

---

### ✅ **Validation Checklist**

* [x] Flask app starts without errors
* [x] Application accessible via EC2 public IP
* [x] Background execution works
* [x] Gunicorn process running

---

### 📬 **Author**

**Alankar Tatyasaheb Jadhav**
Aspiring Cloud & Java Developer

---

### 📄 **Disclaimer**

This project is created **for demonstration, training, and interview discussion purposes only**.
It is **not intended for production use**.

---
