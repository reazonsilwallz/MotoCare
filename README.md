# 🏍️ MotoCare — Vehicle Maintenance Tracker

A personal vehicle maintenance tracking application built with Python and Streamlit. MotoCare helps car and motorcycle owners stay on top of their service history and costs across multiple vehicles.

---

## 📸 Preview

> Dashboard · Cost Comparison · Edit & Delete Records · About Us

---

## 🚀 Features

- **Full CRUD** — Add, view, edit and delete vehicles and maintenance records
- **Dashboard** — KPI cards, cumulative cost line chart, category pie chart and monthly spend bar chart
- **Cost Comparison** — Compare maintenance spend across all vehicles side by side
- **Edit & Delete Records** — Filter, update and remove any record with CSV export
- **About Us** — App info, tech stack and team details
- **100% Offline** — All data stored locally in a JSON file
- **Navy Blue & White Theme** — Clean professional UI using Streamlit config

---

## 🗂️ Project Structure

```
motocare_app.py          # Main entry point — page config and routing
helpers.py               # Shared data functions and constants
motocare_data.json       # Local data storage (auto created on first run)
LICENSE                  # MIT License
README.md                # This file

assets/
├── logo.png             # Sidebar logo
└── icon.png             # Browser tab icon

.streamlit/
└── config.toml          # Navy blue and white theme config

pages_/
├── __init__.py          # Makes pages_ a Python package
├── dashboard.py         # Dashboard page
├── select_vehicle.py    # Select a Vehicle page
├── cost_comparison.py   # Cost Comparison page
├── edit_delete.py       # Edit and Delete Records page
└── about.py             # About Us page
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core programming language |
| Streamlit | Web UI framework |
| Altair / Vega-Lite | Interactive charts |
| Pandas | Data manipulation |
| JSON | Local data storage |
| UUID | Unique ID generation |
| PIL | Image loading for page icon |

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/motocare.git
cd motocare
```

### 2. Install dependencies
```bash
pip install streamlit pandas altair pillow
```

### 3. Run the app
```bash
streamlit run motocare_app.py
```

### 4. Open in browser
```
http://localhost:8501
```

---

## 📖 How to Use

### Step 1 — Add a Vehicle
- Go to **Select a Vehicle** in the sidebar
- Click **➕ Add Vehicle** tab
- Fill in year, make, model, plate, mileage and color
- Click **ADD VEHICLE**

### Step 2 — Add Maintenance Records
- Go to **Select a Vehicle → Add Maintenance Record** tab
- Select your vehicle from the dropdown
- Fill in date, category, description, cost and mileage
- Click **SAVE RECORD**

### Step 3 — View Dashboard
- Go to **Dashboard**
- Select your vehicle from the dropdown
- View KPI cards, charts and recent services table

### Step 4 — Compare Vehicles
- Go to **Cost Comparison**
- View fleet totals, cost per vehicle and category breakdown

### Step 5 — Edit or Delete Records
- Go to **Edit & Delete Records**
- Select your vehicle
- Use tabs to view, edit or delete any record
- Export filtered records as CSV

---

## 🗃️ Data Structure

All data is stored in `motocare_data.json`:

```json
{
  "vehicles": {
    "uuid": {
      "year": 2023,
      "make": "Yamaha",
      "model": "R6",
      "plate": "YMH-2023",
      "vin": "JYARJ18E23A000123",
      "mileage": 18500,
      "color": "Midnight Black",
      "created_at": "2024-01-01 00:00:00"
    }
  },
  "records": [
    {
      "id": "uuid",
      "vehicle_id": "uuid",
      "date": "2024-01-10",
      "category": "Oil Change",
      "description": "Full synthetic oil change",
      "cost": 55.0,
      "mileage": 1000,
      "created_at": "2024-01-10 00:00:00"
    }
  ]
}
```

---

## 🎨 Theme

Configured in `.streamlit/config.toml`:

```toml
[theme]
base = "light"
primaryColor = "#1a3a6b"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#e8eef7"
textColor = "#1a1a1a"
```

---

## 📦 Service Categories

- Oil Change
- Tire Services
- Brake Services
- Battery Services
- Engine Tune-Up
- Others

---

## 🚗 Sample Vehicles Included

| Vehicle | Color | Records |
|---|---|---|
| 2023 Yamaha R6 | Midnight Black | 10 |
| 2021 Toyota Camry | Pearl White | 12 |
| 2020 Honda Civic | Lunar Silver | 12 |
| 2022 Ford Mustang | Race Red | 10 |
| 2019 Kawasaki Ninja ZX6R | Lime Green | 10 |

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

| Role | Contribution |
|---|---|
| Developer | Built the entire app from data layer to UI |
| Designer | Designed the navy blue and white theme |
| Tester | Tested all CRUD operations and chart accuracy |

---

## 🤝 Contributing

Feel free to fork this project, open issues and submit pull requests. All contributions are welcome.

---

*MotoCare · v1.0.0 · Built using Python and Streamlit*