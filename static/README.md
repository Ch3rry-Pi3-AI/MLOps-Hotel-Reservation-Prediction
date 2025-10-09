# 🎨 **Frontend Styling — `style.css`**

This stylesheet defines the **visual design system** for the **Hotel Reservation Prediction** web interface.
It applies a **clean, modern, and responsive layout** that aligns with professional web app standards, ensuring usability and clarity across devices.

The file is located under the Flask project’s `static/` directory and is linked to the template `index.html` using Jinja2:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```



## 🧱 **Purpose**

The `style.css` file is responsible for:

* Establishing consistent **theme variables** (colours, shadows, spacing, radii).
* Designing a **two-column grid** for the prediction form.
* Styling input fields, buttons, and responsive layouts.
* Providing **visual feedback** for model predictions (✅ success / ❌ cancellation).
* Ensuring a **mobile-friendly** experience.



## 🗂️ **File Location**

```
mlops-hotel-reservation-prediction/
├── app.py
├── templates/
│   └── index.html
└── static/
    └── style.css   # 🎨 This file
```



## 🧩 **Core Design Sections**

The stylesheet is organised into logical sections separated by comment banners for clarity:

| Section                | Description                                                        |
| ---------------------- | ------------------------------------------------------------------ |
| **Design Tokens**      | Defines reusable colour palette, shadows, and border radii.        |
| **Global Reset**       | Normalises box-sizing and removes default browser margins/padding. |
| **Base**               | Sets up page background, typography, and flex layout for centring. |
| **Container & Header** | Styles the main content card and title area.                       |
| **Form Layout**        | Builds a responsive two-column grid with consistent spacing.       |
| **Inputs & Selects**   | Customises input elements with focus states and shadow effects.    |
| **Buttons**            | Creates accent-coloured buttons with hover and click feedback.     |
| **Prediction Result**  | Displays model output messages with success/danger colours.        |
| **Responsive Rules**   | Ensures smooth scaling on tablet and mobile devices.               |



## 🎨 **Design Tokens**

At the top of the file, **CSS custom properties** (`:root`) define a central theme for easy colour and layout adjustments:

```css
:root {
    --bg: #f6f8fa;
    --card-bg: #ffffff;
    --text: #333333;
    --muted: #555555;

    --accent: #0077b6;   /* primary accent */
    --accent-2: #0096c7; /* hover */
    --border: #e5e7eb;

    --success: #2b9348;
    --danger: #d90429;

    --shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    --radius-sm: 6px;
    --radius-md: 8px;
    --radius-lg: 12px;
}
```

These tokens allow global theme control — for instance, switching brand colours only requires updating one variable.



## 🧩 **Form Layout and Inputs**

The form uses a **CSS Grid** system:

```css
.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 28px;
}
```

Each input is styled for clarity and accessibility:

```css
input[type="number"],
select {
    padding: 12px;
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}
```

* **Focus states** highlight active fields with the primary accent colour.
* **Spinner controls** on number inputs are removed for cleaner UI.
* Inputs and dropdowns maintain consistent spacing and typography.



## 🧭 **Buttons**

The “Predict” button is styled for prominence and interactivity:

```css
.btn-submit {
    background: var(--accent);
    color: #fff;
    padding: 12px 28px;
    border-radius: var(--radius-md);
    font-weight: 600;
    transition: background 0.25s ease, transform 0.06s ease;
}
.btn-submit:hover {
    background: var(--accent-2);
}
```

This ensures visual feedback when hovered or clicked.



## ✅ **Prediction Result Styling**

The result block changes colour dynamically based on model output:

```css
.result .cancel {
    color: var(--danger);
}

.result .no-cancel {
    color: var(--success);
}
```

These correspond to:

* **❌ Cancellation Likely** → Red text (`--danger`)
* **✅ Honoured Booking** → Green text (`--success`)



## 📱 **Responsive Design**

Two breakpoints enhance usability on smaller screens:

| Breakpoint         | Adjustment                                       |
| ------------------ | ------------------------------------------------ |
| `max-width: 900px` | Reduces container padding                        |
| `max-width: 720px` | Stacks grid columns vertically for mobile layout |

This ensures smooth scaling on tablets and phones.



## 🌈 **Design Principles**

* **Simplicity:** Clean spacing, minimal shadows, and muted tones.
* **Accessibility:** Large form controls and colour contrast for readability.
* **Consistency:** Token-based theme ensures visual coherence.
* **Responsiveness:** Grid-based design adapts across screen sizes.



## 🧠 **Technologies Used**

| Tool / Concept              | Purpose                    |
| --------------------------- | -------------------------- |
| **CSS3 Custom Properties**  | Reusable theme tokens      |
| **Flex & Grid Layouts**     | Modern layout architecture |
| **Media Queries**           | Responsive scaling         |
| **Box Shadows & Radii**     | Subtle depth and polish    |
| **Hover/Focus Transitions** | Smooth visual feedback     |



## 🧾 **Example Customisation**

To change the primary accent colour (blue → orange), simply modify the token:

```css
:root {
    --accent: #ff8800;
    --accent-2: #ffaa33;
}
```

All buttons, highlights, and focus rings update automatically.



## 🖼️ **Preview Suggestion**

You can add a preview image for documentation clarity:

```markdown
![UI Styling Preview](img/style_preview.png)
```

*(Optional visual placeholder for project README or portfolio)*