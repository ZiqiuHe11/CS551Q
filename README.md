# 🧝 Elven Archives of Time – CS551Q Individual Project

This is a Django-based web application for the **CS551Q Enterprise Software Development** individual assessment. It allows users to explore and "purchase" fictional time-travel experiences built on open data. The app demonstrates key features such as authentication, ordering, data visualization, testing, and deployment.

---

## 🌐 Live Demo

**Deployed on PythonAnywhere**:  
🔗 https://ZiqiuHe11.pythonanywhere.com

---

## ✨ Features

- 🔍 **Search & Filters**: Search by keyword, filter by category, location, or sort by price/date
- 🛒 **Ordering System**: Users can "purchase" time experiences
- 👥 **User Roles**:
  - Guest: can browse and search
  - Registered User: can place orders
  - Admin: can access dashboard and view data charts
- 📊 **Admin Dashboard**: View charts of orders and user activity
- 🧪 **Error Handling**: Custom 404, 500, and 403 pages
- 🧪 **Unit Tests**: Basic tests for models and views
- ☁️ **Cloud Deployment**: App is deployed and publicly accessible

---

## 🧩 Data

- 2,000+ fictional "timeslice" experiences generated using open data formats and Faker
- Each timeslice includes name, description, category, location, date, and price

---

## 🛠️ Tech Stack

- Python 3.10
- Django 4.x
- SQLite
- Faker (for fake user/orders)
- Bootstrap (light styling)
- Chart.js (for admin graphs)
- Git + GitHub
- Deployed on [PythonAnywhere](https://www.pythonanywhere.com)

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/ZiqiuHe11/CS551Q.git
cd CS551Q
