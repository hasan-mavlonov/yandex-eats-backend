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

![Untitled (1)](https://github.com/user-attachments/assets/fe7f33ab-7926-436a-8f4d-35a1e1f0111f)



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


## User Management

The project defines five distinct user roles, each with specific responsibilities and privileges:

### 1. Super Admin
- **Overview:** The highest-level user with complete control and administrative privileges.
- **Responsibilities:**
  - Create and manage **Company Managers**.
  - Create and manage **Companies**.
    - A company cannot be created without assigning a **Company Manager**.
  - View and modify information for all users, including **Company Managers**, **Branch Managers**, **Clients**, and **Delivery Personnel**.
- **Authority:** Acts as the "God" user with the ability to intervene in all aspects of the system.

---

### 2. Company Manager
- **Overview:** Manages a company’s operations and personnel.
- **Responsibilities:**
  - Create and manage:
    - **Branches** (must have an assigned **Branch Manager**).
    - **Branch Managers**.
    - **Delivery Personnel** (not tied to specific branches).
  - Oversee company-wide structure and ensure operational readiness.
- **Delivery Flexibility:** While **Delivery Personnel** are created by a specific **Company Manager**, they can deliver orders from any branch in the company.

---

### 3. Branch Manager
- **Overview:** Oversees branch-specific operations and inventory.
- **Responsibilities:**
  - Create and manage:
    - **Menus** tailored to the branch.
    - **Food Items** within the menu.
  - Ensure smooth branch-level operations.

---

### 4. Client
- **Overview:** End-users who interact with the platform to place orders.
- **Responsibilities:**
  - View menus from the nearest branch based on geolocation (latitude and longitude).
  - Create and manage orders.
  - Interact with the company’s offerings based on proximity.

---

### 5. Delivery Personnel
- **Overview:** Facilitates order delivery and manages order statuses.
- **Responsibilities:**
  - Deliver orders dynamically from any branch within the company.
  - Update the **Order Status**:
    - `Pending` → `Preparing` → `Completed` → `Cancelled`.
  - Maintain real-time availability and status updates.
- **Flexibility:** Can operate across multiple branches under the same company.

---
