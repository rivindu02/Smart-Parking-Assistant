
# Smart Parking Assistant 🚗


![UI Screenshot](ui-interface.jpg)

![PCB Hardware](pcb.jpg)

## Introduction
Parking congestion in urban environments has become a critical challenge due to rising vehicle density and inefficient space management. Prolonged searches for vacant spots, overcrowding, and suboptimal parking allocation lead to unnecessary fuel consumption, increased traffic congestion, and heightened frustration among drivers. The absence of automated monitoring exacerbates these inefficiencies, resulting in underutilized spaces and resource wastage.

To mitigate these challenges, we propose a smart parking system that integrates real-time vehicular identification, automated registration, and intelligent space optimization. By leveraging computational models and data-driven analytics, our solution aims to enhance parking efficiency, minimize congestion, and improve overall user experience.

---

## Problem Analysis
Parking inefficiencies significantly impact urban mobility, environmental sustainability, and infrastructure planning. The rising number of vehicles often exceeds available parking capacity, leading to excessive fuel consumption, increased traffic congestion, and higher carbon emissions. Traditional parking systems rely on manual monitoring or static assignments, resulting in poor space utilization and inefficient vehicle distribution.

IoT and AI-driven automation can increase the efficiency of parking management by enabling real-time space monitoring, predictive analytics, and optimized vehicle allocation. Automated vehicle recognition, smart sensors, and dynamic space allocation can minimize search time, reduce fuel wastage, and improve overall efficiency.

---

## Proposed Solution
### Product Overview
Our Smart Parking Optimization System leverages Machine Learning (ML) and rule-based algorithms to efficiently allocate parking spots based on multiple dynamic factors. The system addresses common challenges of inefficient parking allocation, congestion, and user dissatisfaction by providing real-time, data-driven recommendations for the best available parking spot.

#### How It Works
- **Optimized Parking Allocation:** ML assigns the most suitable parking spot based on proximity, vehicle size, duration, and user preferences.
- **Reduced Congestion:** Minimizes unnecessary vehicle movement by guiding drivers directly to an available spot.
- **Adaptive Learning:** Continuously improves predictions using historical data and real-time occupancy information.
- **Enhanced User Experience:** Offers premium and reserved parking options for frequent users or VIPs.

#### Key Features
- Real-Time Spot Allocation
- Predictive Parking Demand
- Vehicle Size & Duration Matching
- User Preferences & Premium Parking
- Integration with Sensors & Cameras
- Scalable & Adaptive System

---

## Uniqueness of the Solution
**License Plate Recognition (LPR) System:**
- AI-based computer vision detects and recognizes license plates.
- Integrates with a database to identify registered vehicles and their parking history.

**IoT-Enabled Parking Sensors:**
- Sensors in parking spots detect occupancy in real time and transmit data to a central server.

**Parking Spot Recommendation Engine:**
- Analyzes data from LPR and sensors to suggest the best available parking spot, considering vehicle size, parking duration, and user preferences.

**Mobile Application:**
- Provides real-time parking availability and navigation to the suggested spot.
- Allows users to reserve parking spots in advance.

**Data Analytics Dashboard:**
- Offers insights into parking patterns, peak hours, and space utilization.
- Enables predictive analytics for future parking demand.

---


## Technical Overview and Implementation

**Sensors & Hardware:**
- Ultrasonic or infrared sensors detect vehicle occupancy in real time.
- Cameras (with OpenCV) provide computer vision-based detection for license plate recognition and vehicle entry/exit.
- Custom PCB (see above) integrates sensor data and communicates with the server.
- Arduino boards handle sensor interfacing; Raspberry Pi boards process images and run AI models.

**Software & Communication:**
- Libraries: WiringPi (Raspberry Pi), Arduino IDE, OpenCV for image processing, scikit-learn/TensorFlow/PyTorch for ML.
- Data is transmitted via MQTT or HTTP protocols to the backend server.

**Algorithms:**
- Rule-based allocation (proximity, vehicle size, reservation status) using greedy algorithms or priority queues.
- As data grows, ML models (regression, time series) predict demand and optimize allocations.

**System Architecture:**
- Real-time guidance via mobile app or digital signage.
- Backend: Django or Node.js manages user data, reservations, and analytics.
- Cloud hosting (AWS/Google Cloud) for scalability and reliability.

**Security & Edge Cases:**
- LPR system checks for unauthorized vehicles and alerts staff.
- Emergency protocols provide real-time instructions for safe evacuation.

**Analytics:**
- Dashboard for operators shows parking patterns, peak hours, and utilization.
- Predictive analytics for future demand and operational planning.

---

## User Scenario
Sarah, a working professional, uses the Smart Parking app to check for available spots before visiting a busy shopping area. She reserves a spot, receives directions, and upon arrival, the LPR system scans her plate and opens the gate. Digital signs guide her to her spot, and sensors update the system in real time. She receives reminders as her reservation nears its end and can extend or end her stay seamlessly. Upon exit, the system charges her digitally and logs her parking history for future convenience.

---

## Updated UI Overview
The current UI features:
- A modern, responsive dashboard with a real-time parking map and spot status (available, occupied, reserved)
- Admin and guest user flows
- Real-time updates and notifications
- Reservation and login modals
- Visual map with draggable and editable parking slots (see screenshot above)

---


---

## Team

Team Name: **Sentinels**  
Category: University

![Our Team](team.jpg)

---

## License

This project is licensed under the MIT License.

---

## Contact

For any inquiries, feedback, or collaboration interests, please open an issue or contact the team via GitHub.


## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/rivindu02/Smart-Parking-Assistant.git
   ```
2. **Install dependencies**  
   (Refer to the documentation for your language/platform.)

3. **Run the application**
   ```bash
   # Example command
   python main.py
   ```
---

## 👨‍💻 Team

Meet the amazing team behind Smart Parking Assistant!

![Our Team](team.jpg)

---

## 📝 License

This project is licensed under the MIT License.

---

## 📫 Contact

For any inquiries, feedback, or collaboration interests, please open an issue or contact the team via GitHub.
