# 🚀 CRM Tool

A modern, full-stack Customer Relationship Management (CRM) application built with **FastAPI** (Python) and **React** (Vite). This tool helps you manage contacts, track deals through a sales pipeline, and organize tasks efficiently.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![React](https://img.shields.io/badge/React-19.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

---

## ✨ Features

### 📇 **Contact Management**
- Create, view, update, and delete contacts
- Store essential contact details (name, email, phone, company, position)
- Unique email enforcement, clean table view
- Deleting a contact keeps its deals (they are simply unlinked)

### 💼 **Deals Pipeline**
- Visual Kanban-style deal tracking
- Pipeline stages: **New** → **Negotiation** → **Won** / **Lost**
- Link deals to contacts
- Track deal values and expected close dates
- Move deals between stages from the card's stage dropdown

### 📊 **Dashboard**
- Live totals: contacts, open pipeline value, won revenue, open tasks, deals per stage

### ✅ **Task Management**
- Create and track tasks with due dates
- Task descriptions for detailed context
- One-click completion toggle
- Link tasks to deals or contacts

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | Modern, high-performance Python web framework |
| **SQLAlchemy + SQLite** | Persistent storage (`backend/crm.db`, created automatically) |
| **Pydantic** | Data validation and serialization |
| **pytest** | API tests (`cd backend && pytest`) |
| **Uvicorn** | ASGI server for FastAPI |
| **Python 3.10+** | Runtime environment |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 19** | UI library for building interfaces |
| **Vite** | Fast build tool and dev server |
| **Tailwind CSS** | Utility-first CSS framework |
| **React Router v7** | Client-side routing |
| **Axios** | HTTP client for API requests |
| **Lucide React** | Beautiful icon library |
| **Framer Motion** | Animation library |

---

## 📁 Project Structure

```
CRM Tool/
├── backend/                    # FastAPI Backend
│   ├── main.py                # API endpoints and app configuration
│   ├── schemas.py             # Pydantic models for validation
│   ├── database.py            # SQLAlchemy engine/session (SQLite)
│   ├── models.py              # ORM tables
│   ├── tests/                 # pytest API tests
│   ├── crud.py                # CRUD operations
│   ├── requirements.txt       # Python dependencies
│   └── venv/                  # Virtual environment
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   │   ├── Layout.jsx     # App layout wrapper
│   │   │   └── Sidebar.jsx    # Navigation sidebar
│   │   ├── pages/             # Page components
│   │   │   ├── Dashboard.jsx  # Main dashboard
│   │   │   ├── Contacts.jsx   # Contact management
│   │   │   ├── Deals.jsx      # Deals pipeline
│   │   │   └── Tasks.jsx      # Task management
│   │   ├── lib/
│   │   │   └── api.js         # Axios API configuration
│   │   ├── App.jsx            # App routing setup
│   │   ├── main.jsx           # Entry point
│   │   └── index.css          # Global styles
│   ├── package.json           # Node.js dependencies
│   ├── tailwind.config.js     # Tailwind configuration
│   └── vite.config.js         # Vite configuration
│
├── start_app.sh               # Startup script for both servers
└── README.md                  # This file
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** installed
- **Node.js 18+** and npm installed

### One-Command Start
Run both backend and frontend with a single command:

```bash
./start_app.sh
```

This script will:
1. Start the FastAPI backend on `http://localhost:8000`
2. Start the Vite dev server on `http://localhost:5173`

### Manual Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the tests (optional)
pytest

# Start the server
uvicorn main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## 📡 API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### API Endpoints

#### Health Check
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Check service status |

#### Contacts
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/contacts/` | List all contacts |
| `POST` | `/contacts/` | Create a new contact |
| `GET` | `/contacts/{id}` | Get a specific contact |
| `PUT` | `/contacts/{id}` | Update a contact |
| `DELETE` | `/contacts/{id}` | Delete a contact |

#### Deals
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/deals/` | List all deals |
| `POST` | `/deals/` | Create a new deal |
| `GET` | `/deals/{id}` | Get a specific deal |
| `PUT` | `/deals/{id}` | Update a deal |
| `DELETE` | `/deals/{id}` | Delete a deal |

#### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/tasks/` | List all tasks |
| `POST` | `/tasks/` | Create a new task |
| `GET` | `/tasks/{id}` | Get a specific task |
| `PUT` | `/tasks/{id}` | Update a task |
| `DELETE` | `/tasks/{id}` | Delete a task |

---

## 🎨 Screenshots

### Dashboard
The main dashboard provides a quick overview of your CRM data.

### Contacts Page
Manage all your business contacts in a clean, organized table view with the ability to add new contacts.

### Deals Pipeline
Visual Kanban board to track deals through different stages of your sales pipeline.

### Tasks
Simple task management with due dates and completion tracking.

---

## 📊 Data Models

### Contact
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "company": "Acme Corp",
  "position": "CEO"
}
```

### Deal
```json
{
  "id": 1,
  "title": "Big Sale",
  "value": 10000.0,
  "stage": "Lead",
  "contact_id": 1
}
```

**Deal Stages**: `Lead`, `Contacted`, `Negotiation`, `Closed Won`, `Closed Lost`

### Task
```json
{
  "id": 1,
  "title": "Follow up call",
  "description": "Discuss contract details",
  "status": "To Do",
  "due_date": "2026-02-15",
  "related_deal_id": 1,
  "related_contact_id": 1
}
```

**Task Statuses**: `To Do`, `In Progress`, `Done`

---

## 🔧 Configuration

### Backend CORS
The backend is configured to accept requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (alternative dev server)
- `http://127.0.0.1:5173`

### Environment Variables
Currently, the app uses default configurations. For production, consider adding:
- Database connection strings
- Secret keys for authentication
- API rate limiting

---

## 🧪 Development

### Running Tests
```bash
# Backend tests (if implemented)
cd backend
pytest

# Frontend linting
cd frontend
npm run lint
```

### Building for Production
```bash
# Frontend build
cd frontend
npm run build
```

---

## 📝 Future Enhancements

- [x] Persistent database (SQLite)
- [ ] User authentication and authorization
- [ ] Export contacts/deals to CSV
- [ ] Email integration
- [ ] Dashboard analytics and charts
- [ ] Drag-and-drop for deals pipeline
- [ ] Search and filter functionality
- [ ] Mobile responsive design improvements
- [ ] Activity logging and history

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Parva Shah**

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - UI Library
- [Tailwind CSS](https://tailwindcss.com/) - CSS Framework
- [Lucide](https://lucide.dev/) - Beautiful icons
- [Vite](https://vitejs.dev/) - Next generation frontend tooling
