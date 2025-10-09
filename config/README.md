# ⚙️ **Configuration File — `config.yaml`**

This YAML file defines all **project-level configuration parameters** used across the **MLOps Hotel Reservation Prediction** pipeline.
It keeps key settings such as data ingestion details, preprocessing rules, and feature selection thresholds separate from the code — allowing for simple updates and consistent experiment tracking.

All values are read dynamically at runtime using the helper function `read_yaml()` from `utils/common_functions.py`.

## 📁 **File Overview**

```
mlops-hotel-reservation-prediction/
├── config/
│   └── config.yaml
```

## 🧩 **Purpose**

`config.yaml` provides a **single source of truth** for data and preprocessing configuration.
Changing dataset parameters or feature lists requires no code modification — only a quick YAML edit.

## 🧠 **Example Usage**

```python
from utils.common_functions import read_yaml

cfg = read_yaml("config/config.yaml")
print(cfg["data_ingestion"]["bucket_name"])
```

## 🧾 **Key Sections**

| Section             | Description                                                                              |
| ------------------- | ---------------------------------------------------------------------------------------- |
| **data_ingestion**  | Contains GCP bucket name, dataset filename, and train/test split ratio.                  |
| **data_processing** | Lists categorical and numerical columns, skewness threshold, and number of top features. |

## 🧱 **Example Content**

```yaml
# Configuration File — config/config.yaml
# Stores project-level configuration parameters for each pipeline stage.

data_ingestion:
  bucket_name: "mlops-hotel-reservation-prediction-bucket"    # GCP bucket name
  bucket_file_name: "Hotel_Reservations.csv"                  # Dataset file name
  train_ratio: 0.8                                            # Train/test split ratio

data_processing:
  categorical_columns:
    - type_of_meal_plan
    - required_car_parking_space
    - room_type_reserved
    - market_segment_type
    - repeated_guest
    - booking_status

  numerical_columns:
    - no_of_adults
    - no_of_children
    - no_of_weekend_nights
    - no_of_week_nights
    - lead_time
    - arrival_year
    - arrival_month
    - arrival_date
    - no_of_previous_cancellations
    - no_of_previous_bookings_not_canceled
    - avg_price_per_room
    - no_of_special_requests

  skewness_threshold: 5                                       # Threshold for log1p transform
  no_of_features: 10                                          # Number of top features to retain
```

## ✅ **Design Highlights**

* **Readable and Modular:** Keeps configuration separate from logic for transparency.
* **Easily Extensible:** Add new parameters (e.g., feature engineering settings, model configs) without code changes.
* **Reproducible:** Enables version-controlled experiment management.
* **Portable:** Adapt quickly for deployment across different cloud or local environments.