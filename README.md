# 🧠 **Inference Stage — Flask Application for Hotel Reservation Prediction**

This branch introduces the **Flask-based inference layer**, transforming the trained model into a **live, interactive web application** that allows users to make hotel reservation predictions in real time.

It bridges the gap between **model training** and **end-user interaction**, deploying a simple yet elegant web interface that takes input features, runs the trained model, and returns the predicted outcome instantly.

---

## 🧾 **What’s New in This Stage**

* 🆕 **`app.py`** — Flask application that loads the trained model and exposes a prediction route.

* 🎨 **`templates/index.html`** — Responsive, emoji-enhanced HTML form for feature input.

* 💅 **`static/style.css`** — Modern UI design with clean, accessible styling and responsive layout.

* 🎬 **Interactive Flask App Demo:**

  ![Hotel Reservation App Demo](img/flask_app/hotel_reservation_app.gif)

* 🔍 **Predictive Workflow**

  * Users input booking details such as `lead_time`, `avg_price_per_room`, and `room_type_reserved`.
  * Flask collects the inputs, formats them as a NumPy array, and passes them to the loaded model.
  * The app returns whether the reservation is likely to be **cancelled** or **honoured**.

---

## ⚙️ **How to Run the Flask Application**

After activating your virtual environment and ensuring all dependencies are installed:

```bash
python app.py
```

Then open your browser and navigate to:

```
http://127.0.0.1:8080
```

or simply:

```
http://localhost:8080
```

You’ll see the interactive form to input reservation details and view instant predictions.

---

## 🗂️ **Updated Project Structure**

```
mlops-hotel-reservation-prediction/
├── artifacts/
│   ├── raw/
│   ├── processed/
│   └── models/
│       └── lgbm_model.pkl
├── config/
│   ├── config.yaml
│   ├── paths_config.py
│   └── model_params.py
├── src/
│   ├── data_ingestion.py
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── logger.py
│   ├── custom_exception.py
│   └── __init__.py
├── utils/
│   └── common_functions.py
├── pipeline/
│   └── training_pipeline.py
├── templates/
│   └── index.html                     # 🆕 Flask HTML interface
├── static/
│   └── style.css                      # 🆕 UI styling
├── img/
│   ├── model_training/
│   │   ├── mlflow_experiment.png
│   │   └── mlflow_run.png
│   └── flask_app/
│       └── hotel_reservation_app.gif  # 🖼️ Demo of the web interface
├── notebooks/
│   └── notebook.ipynb
├── app.py                             # 🆕 Flask inference application
├── requirements.txt
├── setup.py
└── README.md
```

---

## 🧩 **Key Components**

| File / Folder                       | Description                                                             |
| ----------------------------------- | ----------------------------------------------------------------------- |
| `app.py`                            | Core Flask app handling requests, input parsing, and model inference.   |
| `templates/index.html`              | User-facing HTML form to collect reservation data.                      |
| `static/style.css`                  | Modern CSS for consistent, responsive design.                           |
| `artifacts/models/lgbm_model.pkl`   | Trained LightGBM model used for predictions.                            |
| `logger.py` / `custom_exception.py` | Unified logging and error handling modules reused from previous stages. |

---

## 🚀 **Next Stage — CI/CD with Jenkins & Google Cloud Run**

The next branch will implement **Continuous Integration and Continuous Deployment (CI/CD)** for this Flask application using:

* 🧩 **Jenkins** — to automate build, test, and deployment pipelines.
* ☁️ **Google Cloud Run** — to deploy the containerised Flask app as a scalable, serverless API service.

This will mark the project’s transition from local inference to **production-grade model deployment** in the cloud.