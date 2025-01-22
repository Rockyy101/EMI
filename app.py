from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def loan_calculator():
    if request.method == "POST":
        # Get user inputs
        principle = float(request.form["principle"])
        rate_of_interest = float(request.form["rate_of_interest"])
        months = int(request.form["months"])
        
        # Convert annual rate to monthly rate
        monthly_rate = (rate_of_interest / 12) / 100
        
        # Calculate EMI
        emi = principle * monthly_rate * ((1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)
        
        # Loan breakdown
        breakdown = []
        remaining_principle = principle
        for i in range(1, months + 1):
            interest = remaining_principle * monthly_rate
            principal_component = emi - interest
            remaining_principle -= principal_component
            breakdown.append({
                "month": i,
                "interest": round(interest, 2),
                "principal": round(principal_component, 2),
                "remaining": round(remaining_principle, 2)
            })

        return render_template("results.html", emi=round(emi, 2), breakdown=breakdown)

    return render_template("index.html", emi=None, breakdown=None)

if __name__ == "__main__":
    app.run(debug=True)
