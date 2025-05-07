# 🌐 Social Pulse – AI-Powered Social Media Analyzer

**Live App:** [https://socialpulse2.streamlit.app](https://socialpulse2.streamlit.app)  
**Author:** Ximena Castaño

Social Pulse is a prototype app that analyzes Instagram activity using web scraping, machine learning, and interactive data visualization. Built as part of an AI educational initiative, this tool demonstrates how brands or researchers can explore engagement patterns and optimize content strategies.

---

## ✨ Features

- 🔍 Web scraping (Instagram profiles using BeautifulSoup/Selenium)
- 🧹 Data cleaning and preprocessing (pandas)
- 🤖 Machine Learning classification (scikit-learn, hyperparameter tuning)
- 📊 Visual dashboard with Streamlit
- 🗃️ Modular code for educational reuse

---

## 🚀 Getting Started

1. Clone the repository:

```bash
git clone https://github.com/ximenacastano/SocialPulse.git
cd SocialPulse
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

---

## 🧠 Educational Design

This project was designed with learning in mind. The app is structured in **modules**, and each core concept is explained with markdown and comments:
- Web scraping basics
- Feature engineering
- Model training and evaluation
- Visualization with feedback loops

Instructors and learners can adapt the code and documentation to their own datasets.

---

## 📸 Screenshots

### Dashboard Overview

![Dashboard](images/dashboard.png)

### Engagement Analysis

![Engagement](images/engagement.png)

> *(You can add your own screenshots in the `/images` folder.)*

---

## 🧾 File Structure

```
SocialPulse/
│
├── app.py                 # Main Streamlit app
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
├── /images/               # Screenshots for docs
├── /data/                 # Raw or cleaned data (optional)
└── /utils/                # Utility functions or modules (optional)
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙌 Contact

Have feedback or ideas for improvements? Reach out via [LinkedIn](https://www.linkedin.com/in/ximenacastano/) or create an issue in the repo.
