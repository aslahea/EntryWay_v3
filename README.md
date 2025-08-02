# EntryWay
A complete Django web application with a custom-built admin panel, secure user management, and PostgreSQL backend. Built with Bootstrap for UI and JavaScript for validation.

---

## 🌟 Main Features

- 🔐 **Admin Login System**
- 👤 **User Registration with Full Input Fields**
  - Username, Email, DOB, Gender, Marital Status, Terms checkbox
 
    
- ✅ **Client-Side + Server-Side Validation**
  - JavaScript-based validation
  - Django validation with error handling

    
- 🗃️ **Admin Panel Features**
  - List, search, filter, and paginate all users
  - Edit users with pre-filled forms
  - Soft delete with confirmation 
  - Status toggle

  
- 🧑‍💼 **Custom User Model**
  - Extends `AbstractUser` with fields like DOB, gender, marital status, terms
  - Includes soft-delete and override delete method

    
- 🔒 **Security**
  - CSRF protection, XSS-safe output
  - SQL injection-safe queries
  - Sessions and cookies handled securely

---

## 🛠 Technologies Used

- **Django** (with custom user model)
- **PostgreSQL** (as backend database)
- **HTML5 + Bootstrap 5** (for responsive design)
- **JavaScript** (for validation)
- **Session & Cookie Management**
- **CSRF Protection** (enabled by default)

---

## 🧠 Project Highlights

- No use of Django's default admin interface — everything built from scratch.
- Fully custom login, registration, and admin dashboard.
- Admin can:
  - Create new users
  - Edit or soft-delete users
  - Search/filter users by name, email, or date range
- Strong client-server validation system
- Minimal and clean Bootstrap UI with alerts for success/error messages.

---

## 🚀 How to Run

1. Clone the repository  
2. Create virtualenv and install requirements  
3. Configure PostgreSQL database  
4. Run migrations and start the server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
