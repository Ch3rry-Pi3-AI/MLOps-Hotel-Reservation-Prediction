# 🏨 **Hotel Reservation Prediction — Web Interface (index.html)**

This HTML file defines the **frontend interface** for the **Hotel Reservation Prediction** web application.
It provides a clean, responsive, and user-friendly form that allows users to input hotel booking details and receive a **real-time cancellation prediction**.

The page is rendered dynamically using **Flask’s Jinja2 templating engine**, and styled with a separate CSS file (`static/style.css`).



## 🎯 **Purpose**

This page acts as the **main entry point** for end-users.
It captures booking features (such as lead time, meal plan, and room type) and sends them to the Flask backend via an HTTP **POST request** for model inference.

Once the backend processes the data and generates a prediction, the result is displayed directly below the form:

* ✅ **Booking likely to be honoured**
* ❌ **Booking likely to be cancelled**



## 🧩 **Template Integration**

The `index.html` file uses **Jinja2 syntax** to integrate seamlessly with Flask:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

* `{{ url_for('static', filename='style.css') }}` dynamically links to the CSS file from the Flask `static/` folder.
* `{% for i in range(1, 32) %}` generates dynamic `<option>` values for arrival dates.
* `{% if prediction is not none %}` conditionally renders the result section after prediction.



## 🖼️ **UI Layout**

The layout follows a **two-column responsive grid**, making it clear and easy to use:

| Section            | Description                                                         |
| ------------------ | ------------------------------------------------------------------- |
| **Header**         | Displays project title and subtitle                                 |
| **Left Column**    | Lead time, special requests, average room price, arrival month/date |
| **Right Column**   | Market segment, meal plan, room type, number of nights              |
| **Submit Button**  | Triggers prediction request                                         |
| **Result Section** | Displays model output (cancel / no-cancel)                          |



## 🧱 **File Structure**

```
mlops-hotel-reservation-prediction/
├── app.py                          # Flask backend (handles POST requests and predictions)
├── templates/
│   └── index.html                  # 🏨 Main frontend interface
└── static/
    └── style.css                   # 🎨 Styling for form layout and buttons
```



## ⚙️ **How It Works**

1. The user fills in the **form fields** and clicks **Predict**.
2. Flask receives the form data via `POST` and sends it to the trained ML model.
3. The model predicts whether the booking will be cancelled or honoured.
4. Flask renders `index.html` again, injecting the prediction result dynamically into the `{% if prediction %}` block.

Example (simplified Flask route):

```python
@app.route('/', methods=['GET', 'POST'])
def predict():
    prediction = None
    if request.method == 'POST':
        data = [float(request.form[key]) for key in request.form.keys()]
        prediction = model.predict([data])[0]
    return render_template('index.html', prediction=prediction)
```



## 💡 **Form Inputs Summary**

| Feature                 | Input Type | Description                                             |
| ----------------------- | ---------- | ------------------------------------------------------- |
| `lead_time`             | Number     | Days between booking and arrival                        |
| `no_of_special_request` | Number     | Count of customer special requests                      |
| `avg_price_per_room`    | Float      | Average nightly rate per room                           |
| `arrival_month`         | Dropdown   | Month of arrival (1–12)                                 |
| `arrival_date`          | Dropdown   | Day of arrival (1–31)                                   |
| `market_segment_type`   | Dropdown   | Booking channel type (Online, Offline, Corporate, etc.) |
| `no_of_week_nights`     | Number     | Weeknight stays                                         |
| `no_of_weekend_nights`  | Number     | Weekend stays                                           |
| `type_of_meal_plan`     | Dropdown   | Chosen meal plan (1–3 or Not Selected)                  |
| `room_type_reserved`    | Dropdown   | Reserved room category (1–7)                            |



## ✨ **Prediction Output**

After submission:

| Output Value | Display Message                                            |
| ------------ | ---------------------------------------------------------- |
| `0`          | ❌ The customer is **likely to cancel** this reservation.   |
| `1`          | ✅ The customer is **unlikely to cancel** this reservation. |

The output is styled via CSS to visually distinguish between outcomes (e.g., red for cancellations, green for confirmations).



## 🧠 **Technologies Used**

| Component            | Purpose                                   |
| -------------------- | ----------------------------------------- |
| **HTML5 / CSS3**     | Page structure and styling                |
| **Flask (Jinja2)**   | Dynamic rendering and routing             |
| **Python (Backend)** | ML model integration and prediction logic |



## 🚀 **Example Workflow**

1. Launch the Flask app:

   ```bash
   python app.py
   ```
2. Open a browser and visit:

   ```
   http://127.0.0.1:5000/
   ```
3. Fill in form values and click **Predict**.
4. The prediction result will appear instantly below the form.
