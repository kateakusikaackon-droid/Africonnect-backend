# 🌍 AFRICONNECT BACKEND API
=========================

A production-ready Django REST API backend for Africonnect — a B2B platform connecting buyers and suppliers across Africa.  
Built for scalability, security, and real-time business workflows including authentication, supplier management, and product catalog.

=========================
# 🧰 🚀 TECH STACK
=========================

Django  
Django REST Framework  
PostgreSQL (NeonDB)  
JWT Authentication  
Gunicorn  
RESTful API Architecture  

=========================
# 📊 📌 PROJECT STATUS
=========================

Backend: Stable ✔  
Authentication: JWT implemented ✔  
Database: PostgreSQL (NeonDB) connected ✔  
API: Fully RESTful ✔  
Deployment: Ready for production ✔  

=========================
# ⚙️ 🔐 ENVIRONMENT VARIABLES
=========================

Create a `.env` file in the root directory:

SECRET_KEY=your-secret-key  
DEBUG=False  

ALLOWED_HOSTS=example.com,api.yourdomain.com  

DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST.neon.tech/DATABASE_NAME?sslmode=require  

FRONTEND_URL=https://your-frontend-domain.com  

=========================
# 📦 🛠️ SETUP INSTRUCTIONS
=========================

Clone repository:

git clone https://github.com/your-username/africonnect.git  
cd africonnect  

Create virtual environment:

python -m venv venv  
source venv/bin/activate  # macOS/Linux  
venv\Scripts\activate     # Windows  

Install dependencies:

pip install -r requirements.txt  

Run migrations:

cd africonnect  
python manage.py migrate  

Collect static files:

python manage.py collectstatic --noinput  

Run development server:

python manage.py runserver  

API Base URL:

http://127.0.0.1:8000/api/  

=========================
# 🔐 🛡️ AUTHENTICATION
=========================

JWT Authentication System  

Authorization Header:  
Authorization: Bearer <access_token>  

=========================
# 🚀 ⚙️ PRODUCTION START COMMAND
=========================

cd africonnect && gunicorn config.wsgi:application  

=========================
# 📌 ✨ FEATURES
=========================

Secure user authentication (JWT)  
Buyer & supplier dashboards  
Product management system  
REST API architecture for frontend integration  
Scalable backend design for SaaS expansion  

=========================
# 🛡️ ⚠️ IMPORTANT NOTES
=========================

Never commit `.env` file  
Always set DEBUG=False in production  
Keep SECRET_KEY secure  
Configure ALLOWED_HOSTS properly  
Use environment variables for all sensitive data  

=========================
# 🌐 🔗 BASE API URL
=========================

http://127.0.0.1:8000/api/