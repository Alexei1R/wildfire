
# 🌲🔥 Wildfire Detection and Prediction Project

## 🚀 Project Overview
This project, developed during a hackathon, addresses the critical challenge of detecting and predicting wildfires. By leveraging modern technology, including drones, infrared sensors, and machine learning models, we aim to enhance real-time detection and forecasting of wildfire risks. The ultimate goal is to mitigate the devastating impacts of wildfires on lives, ecosystems, and economies.

Our solution integrates a web interface, a Python backend, and a YOLO-based machine learning model that can be deployed on drones for wildfire detection.

---

## 🗂️ File Structure

Here’s a high-level view of the repository structure:

```plaintext
🚀 12:14:14 ❯ tree -L 2
├── api
│   ├── getimg.py
│   ├── main.py
│   ├── satellite_image.jpg
│   └── test.py
├── model
│   ├── data.yaml
│   ├── README.dataset.txt
│   ├── README.roboflow.txt
│   ├── runs
│   ├── test
│   ├── test.txt
│   ├── train
│   ├── valid
│   ├── yolo11n.pt
│   └── yolov8n.pt
├── wildfire
│   ├── eslint.config.js
│   ├── index.html
│   ├── node_modules
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   ├── src
│   └── vite.config.js
11 directories, 17 files
```

---

## 🖥️ How to Run the Project

### 🌐 Running the Web Application
1. Navigate to the root directory of the repository.
2. Install the required dependencies by running:
   ```bash
   npm install
   ```
3. Start the web application:
   ```bash
   npm run start
   ```
4. Open your browser and visit `http://localhost:3000` to access the web interface.

### 🐍 Running the Python Backend
1. Navigate to the `api` directory.
2. Run the Python backend:
   ```bash
   python main.py
   ```

### 🧠 Running the Model
1. Navigate to the `model` directory.
2. Run the model using:
   ```bash
   python main.py
   ```

The model is designed to be deployed on drones for real-time wildfire detection.

---

## 📂 Key Components

### `api`
- Contains Python scripts for the backend, including image processing (`getimg.py`) and the main server (`main.py`).
- Example image: `satellite_image.jpg`.

### `model`
- Includes training and validation datasets, YOLO model files (`yolo11n.pt` and `yolov8n.pt`), and instructions for working with the dataset.
- Configurable via `data.yaml`.

### `wildfire`
- Web application powered by `vite` for user interaction.
- JavaScript/Node.js setup with files like `package.json` and `vite.config.js`.

---

## 🚁 Features

- **Drone Integration**: Detect wildfires in real-time using a drone-mounted model.
- **Infrared Sensor Data**: Process satellite and drone imagery for accurate predictions.
- **Machine Learning**: YOLOv8 model trained for wildfire detection.
- **Web Dashboard**: Intuitive interface for monitoring and reporting.

---

## 🌍 Why It Matters
Wildfires devastate communities, wildlife, and ecosystems globally, causing billions in damages. This project provides a proactive approach to mitigating these risks through technology.

---

## 🤝 Contributors
This project was collaboratively developed during a hackathon to drive innovation and create impactful solutions. Special thanks to all team members for their contributions.

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).

---

🎉 Thank you for checking out the Wildfire Detection and Prediction Project! Together, we can make a difference. 🌱
