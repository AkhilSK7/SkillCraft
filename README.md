#  SkillCraft – Online Learning Platform 

SkillCraft is a Django-based online learning platform where students can enroll in courses, watch course content, leave reviews, and communicate with tutors through a secure real-time chat system.

---

##  Features

###  Student Features
- User authentication (email & Google login)
- Browse available courses
- Enroll in paid courses
- Watch video and document-based lessons
- Leave reviews and ratings for courses
- **Chat with tutors (only after enrollment)**

###  Tutor Features
- Tutor dashboard
- Create and manage courses
- Upload chapters and modules
- View enrolled students
- **Private real-time chat with enrolled students**

---

##  Real-Time Chat System (Key Feature)

SkillCraft includes a **secure one-to-one chat system** built using **Django Channels and Redis**.

### Chat Highlights
- Private chat rooms between **student and tutor**
- Real-time messaging using WebSockets
- Messages are stored and reloaded on page refresh
- Tutors can see a list of students who started chats
- **Enrollment-based access control**
  - Only students enrolled in a course can start a chat
- Secure access (users cannot access others’ chat rooms by URL guessing)

---

##  Tech Stack

###  Backend
- Python
- Django
- Django REST Framework
- Django Channels
- PostgreSQL

###  Frontend
- HTML
- CSS
- Bootstrap
- JavaScript

###  Real-Time & Infrastructure
- Redis (for channel layer)
- WebSockets
- ASGI & Daphne
- Docker (for Redis)

###  Authentication & Payments
- Google OAuth
- Razorpay




