# 🌍✈️ Weather Prediction & Flight Optimization System  

A **machine learning-based system** that predicts **weather conditions** and **optimizes flight paths** using real-time and historical weather data.  

---

## 📌 Project Overview  

This project integrates **weather prediction** and **flight path optimization** to enhance **aviation safety and efficiency**. It combines **machine learning models** for weather forecasting with **real-time flight tracking** to suggest optimized flight routes.  

### 🔹 Key Features  
✅ **Real-time Weather Tracking** 🌦  
✅ **Historical Weather Prediction** 📅  
✅ **Live Flight Tracking & Route Optimization** ✈️  
✅ **Machine Learning-based Forecasting** using **Random Forest** 📊  
✅ **Interactive Map Visualization** using **React Leaflet** 🗺  

---

## 🗂 Dataset Details  

The dataset consists of **historical weather data** from multiple cities in **India**.  

### 📌 **Cities Included:**  
- **Bengaluru, Delhi, Hyderabad, Jaipur, Kanpur, Nagpur, Pune**  

### 📌 **Weather Parameters:**  
- **Temperature** (°C)  
- **Humidity** (%)  
- **Wind Speed** (km/h)  
- **Pressure** (mb)  
- **UV Index**  
- **Air Quality (PM2.5, PM10)**  
- **Latitude, Longitude** (Geo-coordinates)  

### 📌 **Dataset Size:**  
- **Before Data Augmentation**: ~253 images  
- **After Data Augmentation**: ~2065 images  

### 📌 **Flight Data Source:**  
- **AviationStack API** for **live flight tracking**  

---

## 🧠 Model Architecture  

The **weather prediction model** is built using **Random Forest Regressor** and trained on historical weather data.  

### 🔹 **Model Pipeline**  
1️⃣ **Data Preprocessing**  
   - Normalization & Feature Engineering  
   - Handling missing values  
   - Data Augmentation  

2️⃣ **Feature Selection**  
   - Selecting important features affecting weather conditions  
   - Handling categorical variables  

3️⃣ **Machine Learning Model: Random Forest**  
   - Trained on **multi-city weather dataset**  
   - Predicts **temperature, wind speed, humidity, pressure**  
   - Evaluated using **R² Score & RMSE**  

---

## 📌 Implementation Details  

### 🔹 **1️⃣ Backend - Weather Prediction API (Flask & ML Model)**  
✅ **Data Collection**: Fetches **real-time** weather data via **OpenWeather API**  
✅ **Model Training**: **Random Forest Regressor** trained on **historical weather data**  
✅ **Prediction Endpoint**: Flask API to serve **weather forecasts**  

### 🔹 **2️⃣ Frontend - Interactive Flight & Weather Map (React & Leaflet)**  
✅ **Live Weather Display**: Shows real-time weather conditions using **OpenWeather API**  
✅ **Future Weather Prediction**: Users select a **date & time** to view predicted weather  
✅ **Flight Tracking**: Integrates **AviationStack API** for **live flights**  

### 🔹 **3️⃣ Flight Route Optimization**  
✅ **Uses real-time & predicted weather conditions** to optimize flight routes  
✅ **Suggests alternative paths** based on **wind speed, storms, air pressure**  

---

## 📊 Results & Model Performance  

### ✅ **Model Accuracy (Random Forest Regressor)**  

| Dataset | Temperature (R²) | Wind Speed (R²) | Humidity (R²) | Pressure (R²) |  
|---------|-----------------|-----------------|---------------|---------------|  
| **Train Set** | 94% | 91% | 89% | 96% |  
| **Test Set** | 88% | 85% | 83% | 92% |  

### ✅ **Example Prediction for Delhi (2025-01-30 15:00)**  

- 🔹 **Temperature**: 28.5°C  
- 🔹 **Wind Speed**: 12.3 km/h  
- 🔹 **Humidity**: 67%  
- 🔹 **Pressure**: 1012 mb  

---

## 🛠 Tech Stack & Dependencies  

### 🔹 **Backend (Flask API & Machine Learning) 📊**  
- **Python** (pandas, NumPy, scikit-learn, Flask)  
- **Machine Learning**: **Random Forest Regressor**  
- **OpenWeather API** (Weather Data)  
- **AviationStack API** (Flight Data)  

### 🔹 **Frontend (React & Leaflet) 🌍**  
- **React.js** (Frontend UI)  
- **React-Leaflet** (Interactive Map)  
- **Bootstrap** (UI Components)  

---

## ⚡ How to Run the Project  

### **1️⃣ Backend - Flask Server**  
```sh
cd backend
pip install -r requirements.txt
python server.py
📌 API runs on http://localhost:5001
```
### **2️⃣ Frontend - React App**  
```sh
cd frontend
npm install
npm start
📌 UI runs on http://localhost:3000
```

---

## 👨‍💻 Contributing

Contributions are welcome! 🎉 If you'd like to improve the model or UI, feel free to:
✅ Fork the repository
✅ Create a new branch
✅ Submit a Pull Request

---

## 📜 License

This project is open-source under the MIT License.

---

## 📞 Contact

For queries or collaborations, feel free to reach out!
📧 Email: nitinpeter147@gmail.com

---


