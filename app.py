from flask import Flask, render_template, request

import pkg_resources
installed_packages = pkg_resources.working_set
print([f"{i.key}=={i.version}" for i in installed_packages])

app = Flask(__name__)

# Custom Knapsack Function
def knapsack(values, weights, capacity):
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]
    
    # Find the items to select
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]
    
    return selected

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get budget from user input
        budget = int(request.form.get("budget"))

        # Menu items (value and price)
        menu_items = [
            {"name": "1pc Chickenjoy", "value": 100, "price": 84},
            {"name": "2pc Chickenjoy", "value": 180, "price": 180},
            {"name": "Jolly Spaghetti", "value": 120, "price": 70},
        ]

        # Extract values and prices
        values = [item["value"] for item in menu_items]
        prices = [item["price"] for item in menu_items]

        # Solve the knapsack problem
        selected_indices = knapsack(values, prices, budget)
        selected = [menu_items[i] for i in selected_indices]

        # Calculate total value and price
        total_value = sum(menu_items[i]["value"] for i in selected_indices)
        total_price = sum(menu_items[i]["price"] for i in selected_indices)

        return render_template(
            "results.html", budget=budget, selected=selected, total_value=total_value, total_price=total_price
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

app.run(debug=True)
