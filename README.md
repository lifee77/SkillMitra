# SkillMitra

SkillMitra is a web-based platform that helps users explore vocational training courses. The app synchronizes course data between a local and cloud database, allowing offline access and real-time updates when reconnected.

## 🚀 Features

- **Vocational Course Listing:** Browse a list of skill-based courses.
- **Offline Functionality:** Access stored courses without an internet connection.
- **Cloud Synchronization:** Sync locally added courses with the cloud when online.
- **User-Friendly Interface:** View course details in an easy-to-read tabular format.
- **SQLite Integration:** Uses SQLite for both local and cloud databases.

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Database:** SQLite (Local & Cloud)
- **Frontend:** HTML, CSS (Basic Styling)
- **Deployment:** Can be extended to Docker/AWS/GCP in future versions

---

## 📂 Project Structure

```
SkillMitra/
│── app.py              # Main Flask app
│── local.db            # Simulated local database
│── cloud.db            # Simulated cloud database
│── templates/
│   ├── index.html      # Web UI template (Rendered using Flask)
│── static/
│   ├── styles.css      # CSS styles (Optional)
│── README.md           # Documentation
```

---

## 💾 Installation & Setup

### 🔹 Prerequisites
Make sure you have the following installed:
- Python 3.x
- Flask (`pip install flask`)

### 🔹 Clone the Repository

```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/SkillMitra.git
cd SkillMitra
```

### 🔹 Run the App

```sh
python app.py
```

### 🔹 Access the App
Open your browser and visit:
```
http://127.0.0.1:5000/
```

---

## 🎯 Usage

1. **View Vocational Courses**  
   - Courses are displayed in two tables:  
     - **Local Database** (Offline Storage)  
     - **Cloud Database** (Online Backup)  

2. **Syncing Data**
   - New course data added offline is synced with the cloud database once reconnected.

---

## 🧪 Running Tests

SkillMitra includes unit tests to verify database synchronization:

```sh
python -m unittest app_test.py
```

---

## 🚀 Future Enhancements

- ✅ **User Authentication** (Allow users to track courses)
- ✅ **Course Filtering & Search**
- ✅ **Integration with Google Drive for Cloud Storage**
- ✅ **Mobile App Development (React Native or Flutter)**
- ✅ **Real-time Notifications for Course Updates**

---

## 🤝 Contributing

We welcome contributions! To get started:

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```sh
   git clone https://github.com/YOUR_GITHUB_USERNAME/SkillMitra.git
   ```
3. **Create a feature branch:**
   ```sh
   git checkout -b feature-new-functionality
   ```
4. **Commit your changes** and **push**:
   ```sh
   git commit -m "Add new feature"
   git push origin feature-new-functionality
   ```
5. **Create a pull request** on GitHub.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Jeevan Bhatta**  
📧 Email: jeevanbhattacs@gmail.com  
🌐 GitHub: [lifee77](https://github.com/lifee77)  

---

## ⭐ Acknowledgments

A special thanks to all contributors, testers, and advisors who helped make SkillMitra possible!
