# Yandex Eats Backend  

## Overview  
### English (ENG):  
**Yandex Eats Backend Replica**  
This project is a backend replica of Yandex Eats, built using Django. It replicates core functionalities, including user roles, restaurant management, branch-specific menus, proximity-based branch discovery, order processing, and delivery logistics. The project emphasizes scalability, efficiency, and clean API design.  

### Russian (RUS):  
**Реплика бекенда Yandex Eats**  
Этот проект представляет собой реплику бекенда Yandex Eats, разработанную на Django. Он воспроизводит основные функции: управление ролями пользователей, ресторанами, меню для филиалов, определение ближайших филиалов, обработку заказов и логистику доставки. Проект направлен на масштабируемость, эффективность и чистый дизайн API.  

### Uzbek (UZB):  
**Yandex Eats Backend Nusxasi**  
Ushbu loyiha Yandex Eats platformasining backend nusxasini yaratish uchun Django'dan foydalanilgan. Unda foydalanuvchilar rollari, restoranlarni boshqarish, filiallarga xos menyular, eng yaqin filialni aniqlash, buyurtmalarni qayta ishlash va yetkazib berish logistikasini ta'minlash funksiyalari mavjud. Loyiha kengaytiriluvchanlik, samaradorlik va toza API dizayniga e'tibor qaratadi.  

---

## Technologies  
- **Framework:** Django  
- **Database:** PostgreSQL with PostGIS for geospatial data  
- **Language:** Python  
- **API Documentation:** Swagger / DRF Schema  

---

## Key Features  
### Core Functionalities:  
- **User Management:**  
  - **Roles:** Super Admin, Company Manager, Branch Manager, Client, and Delivery Personnel.  
  - Authentication using JWT.  

- **Restaurant and Branch Management:**  
  - Super Admin creates companies and assigns Company Managers.  
  - Company Managers manage branches and their managers.  
  - Each branch can have unique menus and location-specific services.  

- **Proximity-Based Ordering:**  
  - Users see and order from the closest branch based on their geolocation.  

- **Menu Management:**  
  - Branch Managers curate branch-specific menus with unique offerings.  

- **Order and Delivery Management:**  
  - Handle order creation, updates, and tracking.  
  - Assign delivery personnel dynamically based on branch proximity.  

### Advanced Functionalities:  
- **Geospatial Capabilities:**  
  - Branch location stored using latitude and longitude.  
  - Nearest branch calculated using geospatial queries (PostGIS).  

- **Delivery Logistics:**  
  - Real-time driver availability and status updates.  

---

## Database Structure  
The backend relies on a robust and scalable database design tailored to simulate the functionalities of Yandex Eats. The structure includes user roles, branch locations, menu management, orders, and delivery tracking.

![Yandex Eats Database Structure](https://github.com/user-attachments/assets/cb5e0a47-9938-4e48-99b9-eb2d6ee3f7f4)


---

## Installation  
### Prerequisites  
- Python 3.10+  
- PostgreSQL 13+ with PostGIS  
- Git  

### Steps  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/yandex-eats-backend.git
   cd yandex-eats-backend

