# TravelGenie (AI-Powered Smart Travel Planning System)

## 1. Project Overview

TravelGenie is an intelligent travel planning system that generates personalized, structured, and optimized travel itineraries using a locally deployed Large Language Model.

The system combines:

* Structured dataset filtering
* Context-aware LLM generation
* GPU-accelerated inference

Users provide travel preferences, and the system produces a realistic, day-wise itinerary tailored to their inputs.

---

## 2. Core Functionality

TravelGenie allows users to specify:

* Destination
* Number of travel days
* Budget range
* Travel category (historical, religious, nature, etc.)

Based on these inputs, the system generates:

* Structured day-wise itinerary
* Contextual activity descriptions
* Climate information
* Budget-aligned recommendations

---

## 3. Key Features

### 3.1 Personalized Itinerary Generation

* Automatically generates structured travel plans divided by day.
* Logical sequencing of activities.

### 3.2 AI-Enhanced Content

* Uses Mistral 7B Instruct for contextual descriptions.
* Improves readability and recommendation quality.

### 3.3 Budget-Aware Filtering

* Filters destinations and activities based on price constraints.
* Ensures realistic recommendations.

### 3.4 City-Restricted Output

* Prevents cross-city or irrelevant suggestions.
* Strict dataset-based filtering before LLM generation.

### 3.5 Climate Summary Integration

* Includes climate data for selected destination.
* Assists in better travel preparation.

### 3.6 Editable Itinerary

* Users can modify generated plans.
* Supports customization after generation.

### 3.7 Local Storage Support

* Stores generated itineraries in browser localStorage.
* Allows session persistence without backend storage.

---

## 4. System Architecture

```
User Input
    ↓
React Frontend (Vite)
    ↓
Axios API Request
    ↓
FastAPI Backend
    ↓
CSV Dataset Filtering
    ↓
Structured Prompt Injection
    ↓
Mistral 7B Instruct (4-bit Quantized)
    ↓
GPU Accelerated Inference (RTX 4060, CUDA 12.7)
    ↓
Structured Day-wise Itinerary
    ↓
Frontend Rendering + Local Storage
```

---

## 5. System Workflow

1. User enters travel details in the React interface.
2. Axios sends request to FastAPI backend.
3. Backend reads and filters structured CSV dataset based on:

   * Destination
   * Budget
   * Category
   * Climate
4. Filtered structured data is embedded into the LLM prompt.
5. Mistral 7B Instruct generates a structured itinerary.
6. Backend returns formatted response.
7. Frontend renders itinerary dynamically.
8. Itinerary is optionally stored in localStorage.

---

## 6. Technology Stack

### 6.1 Frontend

* React.js (Vite)
* Axios (API communication)
* Dynamic Chat Interface
* localStorage for itinerary persistence

### 6.2 Backend

* FastAPI
* HuggingFace Transformers
* Accelerate
* Mistral 7B Instruct

### 6.3 AI Infrastructure

* 4-bit quantization
* NVIDIA RTX 4060 GPU
* CUDA 12.7
* Transformers + Accelerate pipeline

### 6.4 Data Layer

* Structured CSV dataset
* Cities from India, USA, and Iran
* Includes:

  * City name
  * Climate conditions
  * Pricing range
  * Category metadata

---

## 7. Project Structure

```
Travel_Genie-Inheritance-
│
├── frontend/
│   ├── src/
│   └── vite.config.js
│
├── backend/
│   ├── main.py
│   ├── model_loader.py
│   └── dataset.csv
│
├── requirements.txt
└── README.md
```

---

## 8. Installation Guide

### Step 1: Clone Repository

```
git clone https://github.com/YOUR_USERNAME/Travel_Genie-Inheritance-.git
cd Travel_Genie-Inheritance-
```

Replace `YOUR_USERNAME` with your GitHub username.

---

### Step 2: Backend Setup

```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

System Requirements:

* CUDA 12.7 installed
* NVIDIA GPU drivers configured
* PyTorch with CUDA support

---

### Step 3: Frontend Setup

```
cd frontend
npm install
npm run dev
```

---

## 9. Use Cases

* Personalized travel planning
* Budget-based itinerary generation
* Academic AI demonstration
* Local LLM deployment showcase
* Structured prompt engineering implementation

---

## 10. Future Improvements

* Real-time weather API integration
* Hotel and flight API integration
* Multi-city route optimization
* User authentication and cloud storage
* Cloud-based LLM deployment
* Vector database integration for scalable retrieval

