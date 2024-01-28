from flask import Flask, request, render_template_string

app = Flask(__name__)

# BMI Categories and Advice
categories = {
    (0, 18.4): ("Underweight", "Focus on increasing calorie intake through healthy and nutritious foods. Consult a doctor or registered dietitian for personalized guidance on weight gain."),
    (18.5, 24.9): ("Normal Weight", "Prioritize sustainable healthy habits like consuming a variety of nutrient-rich foods and engaging in regular physical activity."),
    (25, 29.9): ("Overweight", "Focus on maintaining a healthy weight through dietary changes like portion control and reducing processed foods. Regular physical activity is also crucial for managing weight and reducing health risks."),
    (30, 34.9): ("Obesity (Class 1)", "ncreased risk of health problems, but lifestyle changes can often manage them effectively."),
    (35, 39.9): ("Obesity (Class 2)", "Significantly higher risk of health complications. Medical intervention may be necessary alongside lifestyle changes."),
    (40, float('inf')): ("Obesity (Class 3)", "Very high risk of severe health problems. Medical intervention is usually required in addition to lifestyle changes."),
}

# Additional information for each BMI category
category_info = {
    "Underweight": "Being underweight can be caused by various factors like malnutrition, eating disorders, chronic diseases, or hyperthyroidism. It can lead to health problems like weakened immunity, osteoporosis, and fertility issues.",
    "Normal Weight": "This is considered a healthy weight range associated with lower risk of chronic diseases. Maintaining this range through a balanced diet and regular physical activity is recommended.",
    "Overweight": "While not directly linked to major health problems, this category indicates an increased risk of developing them later in life, such as type 2 diabetes, heart disease, and certain cancers.",
    "Obesity (Class 1)": "Obesity is a chronic disease associated with numerous health risks, including cardiovascular disease, stroke, type 2 diabetes, some cancers, and respiratory problems. ",
    "Obesity (Class 2)": "Obesity is a chronic disease associated with numerous health risks, including cardiovascular disease, stroke, type 2 diabetes, some cancers, and respiratory problems. ",
    "Obesity (Class 3)": "Obesity is a chronic disease associated with numerous health risks, including cardiovascular disease, stroke, type 2 diabetes, some cancers, and respiratory problems. "
}

@app.route('/', methods=['GET', 'POST'])
def bmi_calculator():
    weight_error_message = ""
    height_error_message = ""

    if request.method == 'POST':
        unit = request.form['unit']
        weight = request.form['weight']
        height = request.form['height']

        try:
            weight = float(weight)
        except ValueError:
            weight_error_message = "Please enter a valid numeric value for weight."

        try:
            height = float(height)
        except ValueError:
            height_error_message = "Please enter a valid numeric value for height."

        if not weight_error_message and not height_error_message:
            if unit == 'metric':
                if weight <= 0 or height <= 0:
                    weight_error_message = "Weight must be positive values."
                    height_error_message = "Height must be positive values."
                else:
                    bmi = weight / ((height / 100) ** 2)
            else:
                if weight <= 0 or height <= 0:
                    weight_error_message = "Weight must be positive values."
                    height_error_message = "Height must be positive values."
                else:
                    # Convert height to inches
                    height_in_inches = height * 12
                    bmi = (weight / (height_in_inches ** 2)) * 703

            if not weight_error_message and not height_error_message:
                category, advice = get_bmi_category_and_advice(bmi)
                info = category_info.get(category, "")

                return render_template_string(
                    '''
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>WeightMeter: BMI Calculator</title>
                        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                        <style>
                            body {
                                background-color: #f0f0f0;
                                font-family: Arial, sans-serif;
                                margin: 90px;
                            }
                            .container {
                                background-color: #fff;
                                padding: 20px;
                                border-radius: 5px;
                                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                            }
                            .category-highlight {
                                background-color: #f7dc6f;
                            }
                            table {
                                width: 100%;
                                border-collapse: collapse;
                            }
                            table, th, td {
                                border: 1px solid #ddd;
                            }
                            th, td {
                                padding: 8px;
                                text-align: left;
                            }
                            h2 {
                                font-size: 20px;
                                font-weight: bold;
                                margin-top: 15px;
                                margin-bottom: 20px;
                                color: #333;
                            }
                            h1 {
                                font-weight: bold;
                                margin-top: 10px;
                                font-size: 40px;
                                text-align: center;
                                color: #fff;
                            }
                            .form-group {
                                margin-bottom: 15px;
                            }
                            label {
                                font-weight: bold;
                            }
                            .btn-primary {
                                background-color: #17179c;
                                color: #fff;
                            }
                            .btn-primary:hover {
                                background-color: #17179c;
                            }
                            .btn-secondary {
                                background-color: #6c757d;
                                color: #fff;
                            }
                            .btn-secondary:hover {
                                background-color: #565e64;
                            }
                            .error-message {
                                color: red;
                            }
                            .header {
                                background-color: #17179c;
                                color: white;
                                padding: 10px;
                                border-radius: 5px 5px 5px 5px;
                            }
                            .result {
                                background-color: #f5f5f5;
                                padding: 15px;
                                border-radius: 0 0 5px 5px;
                            }
                        </style>
                        <script>
                            function isNumeric(value) {
                                return !isNaN(parseFloat(value)) && isFinite(value);
                            }
                        </script>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <h1>WeightMeter: BMI Calculator - Result</h1>
                            </div>
                            <div class="result">
                                <h2>For your information entered:</h2>
                                <p>Weight: <span>{{ weight }}</span> {% if unit == 'metric' %} kilograms {% else %} pounds {% endif %}</p>
                                <p>Height: <span>{{ height }}</span> {% if unit == 'metric' %} centimeters {% else %} feet {% endif %}</p>
                                <p>Your BMI is: <span style="font-weight: bold;">{{ bmi }}</span></p>
                                <p>Category: <span style="font-weight: bold;">{{ category }}</span></p>
                                <p><strong>Information:</strong> {{ info }}</p>
                                <p><strong>Advice:</strong> {{ advice }}</p>
                                <h2>BMI Classification</h2>
                                <table>
                                    <tr>
                                        <th>BMI Range</th>
                                        <th>Category</th>
                                    </tr>
                                    <tr>
                                        <td>0 - 18.4</td>
                                        <td style="background-color: #F1948A;">Underweight</td>
                                    </tr>
                                    <tr>
                                        <td>18.5 - 24.9</td>
                                        <td style="background-color: #82E0AA;">Normal Weight</td>
                                    </tr>
                                    <tr>
                                        <td>25 - 29.9</td>
                                        <td style="background-color: #FAD02E;">Overweight</td>
                                    </tr>
                                    <tr>
                                        <td>30 - 34.9</td>
                                        <td style="background-color: #F7DC6F;">Obesity (Class 1)</td>
                                    </tr>
                                    <tr>
                                        <td>35 - 39.9</td>
                                        <td style="background-color: #F5B041;">Obesity (Class 2)</td>
                                    </tr>
                                    <tr>
                                        <td>40 and above</td>
                                        <td style="background-color: #EC7063;">Obesity (Class 3)</td>
                                    </tr>
                                </table>
                                <div style="margin-top: 30px;"> 
                                    <a class="btn btn-primary" href="/">Calculate Again</a>
                                </div>
                                </div>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    ''',
                    bmi=round(bmi, 1), category=category, advice=advice, info=info, weight=round(weight), height=round(height), unit=unit
                )

    return render_template_string(
        '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>WeightMeter: BMI Calculator - Result </title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <style>
                body {
                    background-color: #f0f0f0;
                    font-family: Arial, sans-serif;
                    margin: 90px;
                }
                .container {
                    background-color: #fff;
                    padding: 25px;
                    border-radius: 5px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                }
                .category-highlight {
                    background-color: #f7dc6f;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                table, th, td {
                    border: 1px solid #ddd;
                }
                th, td {
                    padding: 8px;
                    text-align: left;
                }
                h2 {
                    font-size: 22px; 
                }
                h1 {
                    font-weight: bold;
                    margin-top: 10px;
                    font-size: 42px
                }
                .form-group {
                    margin-bottom: 15px;
                }
                label {
                    font-weight: bold;
                }
                .btn-primary {
                    background-color: #17179c;
                    color: #fff;
                }
                .btn-secondary {
                    background-color: #6c757d;
                    color: #fff;
                }
                .btn-secondary:hover {
                    background-color: #565e64;
                }
                .error-message {
                    color: red;
                }
                .header {
                    background-color: #17179c;
                    color: white;
                    padding: 10px;
                    border-radius: 5px 5px 5px 5px;
                }
                .result {
                    background-color: #f5f5f5;
                    padding: 15px;
                    border-radius: 0 0 5px 5px;
                }
            </style>
            <script>
                function isNumeric(value) {
                    return !isNaN(parseFloat(value)) && isFinite(value);
                }

                function updatePlaceholders() {
                    var unit = document.getElementById('unit').value;
                    var weightInput = document.getElementById('weight');
                    var heightInput = document.getElementById('height');

                    if (unit === 'metric') {
                        weightInput.placeholder = "Enter weight in kg (e.g., 70)";
                        heightInput.placeholder = "Enter height in cm (e.g., 170)";
                    } else {
                        weightInput.placeholder = "Enter weight in lb (e.g., 154)";
                        heightInput.placeholder = "Enter height in ft (e.g., 5.6)";
                    }
                }

                // Call updatePlaceholders when the page loads and when unit selection changes
                window.onload = updatePlaceholders;
            </script>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 class="text-center">WeightMeter: BMI Calculator</h1>
                </div>
                <div style="margin-top: 30px;"> 
                <h2>Body Mass Index (BMI)</h2>
                <p style="text-align: justify;">BMI is a measure of body fat based on height and weight. It is used to estimate whether an individual is underweight, normal weight, overweight, or obese. It is commonly used by healthcare professionals and researchers as a preliminary screening tool that is widely used to measure and provides an indication of an individual's body composition in relation to their height and weight.</p>
                <form method="POST">
                    <div class="form-group">
                        <label for="unit">Choose a unit:</label>
                        <select class="form-control" name="unit" id="unit" onchange="updatePlaceholders()">
                            <option value="metric">Metric</option>
                            <option value="standard">Standard</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="weight">Weight:</label>
                        <input type="text" class="form-control" name="weight" id="weight"  required oninput="this.setCustomValidity(isNumeric(this.value) ? '' : 'Please enter a valid numeric value for weight.');">
                        <p class="error-message">{{ weight_error_message }}</p>
                    </div>
                    <div class="form-group">
                        <label for="height">Height:</label>
                        <input type="text" class="form-control" name="height" id="height" required oninput="this.setCustomValidity(isNumeric(this.value) ? '' : 'Please enter a valid numeric value for height.');">
                        <p class="error-message">{{ height_error_message }}</p>
                    </div>
                    <button type="submit" class="btn btn-primary">Calculate BMI</button>
                    <button type="reset" class="btn btn-secondary">Clear</button>
                </form>
                </div>
                </div>
            </div>
        </body>
        </html>
        ''',
        weight_error_message=weight_error_message, height_error_message=height_error_message
    )

def get_bmi_category_and_advice(bmi):
    for (lower, upper), (category, advice) in categories.items():
        if lower <= bmi <= upper:
            return category, advice

if __name__ == '__main__':
    app.run(debug=True)