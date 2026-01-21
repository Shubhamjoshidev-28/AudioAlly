# 🔊 Audioally — Vision to Voice Assistive System

Audioally is an **AI-powered vision-to-voice assistive system** designed to help **visually impaired individuals** navigate urban and indoor environments safely.  
It uses **real-time object detection** to identify obstacles, people, traffic elements, and hazards, and converts visual information into **audio feedback**.

> 🎯 *Our goal is to make everyday navigation safer, smarter, and more accessible.*

---

## 🚀 Key Features

- 🧠 **Real-time Object Detection** using YOLO
- 🔊 **Vision-to-Voice Conversion** for instant audio alerts
- 🚶 **Urban Navigation Assistance**
- ⚠️ **Safety-first Hazard Detection**
- 🇮🇳 **India-context Optimized Dataset**
- 💡 **Lightweight & Edge-friendly Models**

---

## 🧩 Problem Statement

Visually impaired individuals face daily challenges such as:
- Unnoticed obstacles (poles, walls, drains)
- Unsafe road crossings
- Crowded areas
- Animals and unexpected hazards
- Construction zones and uneven roads

Existing solutions are either:
- Too expensive  
- Not optimized for local environments  
- Not real-time  

**Audioally solves this gap using AI and computer vision.**

---

## 🛠️ Tech Stack

- **Programming Language:** Python  
- **Model:** YOLO (YOLOv8n / Nano)  
- **Libraries:** OpenCV, PyTorch, Pandas  
- **Annotation Format:** YOLO  
- **Dataset:** Custom + Urban Object Detection Dataset  
- **Platform:** Windows / Linux  

---

## 📦 Dataset Overview

Audioally uses a **39-class object detection dataset**, built by:
- Using a **base 26-class urban dataset**
- Extending it with **13 safety-critical assistive classes**

### 🟦 Base Dataset Classes (26)
Bench, Bicycle, Branch, Bus, Bushes, Car, Crosswalk, Door, Elevator,  
Fire Hydrant, Green Light, Gun, Motorcycle, Person, Pothole, Rat,  
Red Light, Scooter, Stairs, Stop Sign, Traffic Cone, Train, Tree,  
Truck, Umbrella, Yellow Light

### 🟩 Audioally Added Safety Classes (13)
Crowd, Pole, Wall, Open Drain, Water Puddle, Speed Breaker,  
Divider/Median, Fallen Object, Construction Area, Footpath,  
Road Edge, Stray Dog, Cow

📊 **Total Classes:** 39  
📸 **Total Images:** ~40,000+

---

## 📂 Project Structure

