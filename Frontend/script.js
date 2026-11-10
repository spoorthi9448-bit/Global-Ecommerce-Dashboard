// ==========================================
// GLOBAL E-COMMERCE DASHBOARD
// Connect charts to Flask backend
// ==========================================

const API_URL = "http://127.0.0.1:5000";

// Store chart instances
let categoryChartInstance;
let salesChartInstance;
let profitChartInstance;
let topProductsChartInstance;



// ==========================================
// 1. SALES BY CATEGORY
// ==========================================

categoryChartInstance = new Chart(
    document.getElementById("categoryChart"),
    {
        type: "bar",
        data: {
            labels: [],
            datasets: [{
                label: "Sales",
                data: [],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    }
);


// ==========================================
// 2. MONTHLY SALES TREND
// ==========================================

salesChartInstance = new Chart(
    document.getElementById("salesChart"),
    {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Monthly Sales",
                data: [],
                borderWidth: 2,
                fill: false,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    }
);


// ==========================================
// 3. PROFIT BY CATEGORY
// ==========================================

profitChartInstance = new Chart(
    document.getElementById("profitChart"),
    {
        type: "bar",
        data: {
            labels: [],
            datasets: [{
                label: "Profit",
                data: [],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    }
);


// ==========================================
// 4. TOP 10 PRODUCTS BY SALES
// ==========================================

topProductsChartInstance = new Chart(
    document.getElementById("topProductsChart"),
    {
        type: "bar",
        data: {
            labels: [],
            datasets: [{
                label: "Sales",
                data: [],
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { beginAtZero: true }
            }
        }
    }
);


// ==========================================
// 5. SALES BY REGION
// ==========================================

// ==========================================
// 5. INTERACTIVE 3D WORLD GLOBE
// ==========================================


function renderWorldGlobe(countryData) {

    const globe = document.getElementById("worldGlobe");

    if (!countryData || countryData.length === 0) {
        globe.innerHTML = "No country sales data available.";
        return;
    }

    const countries = countryData.map(item => item.Country);
    const sales = countryData.map(item => item.sales);

    const globeData = [{
        type: "choropleth",
        locationmode: "country names",
        locations: countries,
        z: sales,
        text: countries,
        colorscale: "Viridis",
        colorbar: { title: "Sales" },
        customdata: countryData.map(item => [
            item.profit,
            item.orders
        ]),
        hovertemplate:
            "<b>%{location}</b><br>" +
            "Total Sales: $%{z:,.2f}<br>" +
            "Total Profit: $%{customdata[0]:,.2f}<br>" +
            "Total Orders: %{customdata[1]}<extra></extra>"
    }];

    const layout = {
        title: "Global Sales Distribution",
        geo: {
            projection: { type: "orthographic" },
            showland: true,
            landcolor: "#e5e7eb",
            showocean: true,
            oceancolor: "#dbeafe",
            showcountries: true,
            countrycolor: "#ffffff"
        },
        margin: { t: 50, b: 10, l: 10, r: 10 }
    };

    Plotly.react(globe, globeData, layout, { responsive: true })
        .then(() => {

            globe.removeAllListeners("plotly_click");

            globe.on("plotly_click", async function(eventData) {

                const countryName = eventData.points[0].location;
                const details = document.getElementById("countryDetails");

                details.innerHTML = "<h2>Loading country details...</h2>";

                try {
                    const response = await fetch(
                        `${API_URL}/api/country?country=${encodeURIComponent(countryName)}`
                    );

                    const data = await response.json();

                    if (!response.ok) {
                        throw new Error(data.error || "Unable to load details.");
                    }

                    function createTable(title, rows) {
                        if (!rows || rows.length === 0) {
                            return `<h3>${title}</h3><p>No data available.</p>`;
                        }

                        const columns = Object.keys(rows[0]);

                        let html = `<h3>${title}</h3>
                            <div style="overflow-x:auto;">
                            <table border="1" cellpadding="8"
                            cellspacing="0"
                            style="width:100%;border-collapse:collapse;margin-bottom:20px;">
                            <tr>`;

                        columns.forEach(column => {
                            html += `<th>${column}</th>`;
                        });

                        html += "</tr>";

                        rows.forEach(row => {
                            html += "<tr>";

                            columns.forEach(column => {
                                html += `<td>${row[column] ?? ""}</td>`;
                            });

                            html += "</tr>";
                        });

                        html += "</table></div>";
                        return html;
                    }

                    details.innerHTML = `
                        <h2>🌎 ${data.country} - Complete Details</h2>
                        <p><strong>Region:</strong> ${data.region}</p>

                        ${createTable("1. Sales Summary", [data.summary])}
                        ${createTable("2. Category Details", data.categories)}
                        ${createTable("3. All Product Details", data.products)}
                        ${createTable("4. Top 10 Products", data.top_products)}
                        ${createTable("5. Customer Details", data.customers)}
                        ${createTable("6. Order Details", data.orders)}
                    `;

                } catch (error) {
                    details.innerHTML = `<h2>Error: ${error.message}</h2>`;
                    console.error(error);
                }
            });
        });
}

// ==========================================
// 6. FETCH LIVE DATA FROM FLASK
// ==========================================

async function loadDashboardData() {
    try {
        const response = await fetch(`${API_URL}/api/dashboard`);

        if (!response.ok) {
            throw new Error("Unable to load dashboard data.");
        }

        const data = await response.json();

        // Update Sales by Category
        categoryChartInstance.data.labels =
            data.category_sales.labels;

        categoryChartInstance.data.datasets[0].data =
            data.category_sales.values;

        categoryChartInstance.update();


        // Update Monthly Sales Trend
        salesChartInstance.data.labels =
            data.monthly_sales.labels.map(month => {
                const [year, monthNumber] = month.split("-");
                const date = new Date(
                    Number(year),
                    Number(monthNumber) - 1
                );

                return date.toLocaleDateString("en-US", {
                    month: "short",
                    year: "numeric"
                });
            });

        salesChartInstance.data.datasets[0].data =
            data.monthly_sales.values;

        salesChartInstance.update();


        // Update Profit by Category
        profitChartInstance.data.labels =
            data.category_profit.labels;

        profitChartInstance.data.datasets[0].data =
            data.category_profit.values;

        profitChartInstance.update();


        // Update Top 10 Products
        topProductsChartInstance.data.labels =
            data.top_products.labels;

        topProductsChartInstance.data.datasets[0].data =
            data.top_products.values;

        topProductsChartInstance.update();


        // Update Sales by Region
       // Update Interactive World Globe

        // Update Interactive World Globe
        renderWorldGlobe(data.countries);

        console.log("Dashboard data loaded successfully!", data);

    } catch (error) {
        console.error("Dashboard loading error:", error);

        alert(
            "Unable to load dashboard data. " +
            "Please check that the Flask backend is running."
        );
    }
}

// Load the charts when the page opens
loadDashboardData();


// ==========================================
// 7. INTERACTIVE CHAT ANALYTICS
// ==========================================

async function askQuestion() {
    const questionInput = document.getElementById("question");
    const originalQuestion = questionInput.value.trim();

    if (originalQuestion === "") {
        alert("Please enter a question.");
        return;
    }

    const chatBox = document.querySelector(".chat-box");

    // Display the user's question safely
    const userMessage = document.createElement("div");
    userMessage.className = "bot-message";

    const userHeading = document.createElement("strong");
    userHeading.textContent = "You";

    const userText = document.createElement("p");
    userText.textContent = originalQuestion;

    userMessage.append(userHeading, userText);
    chatBox.appendChild(userMessage);

    // Display a temporary message
    const botMessage = document.createElement("div");
    botMessage.className = "bot-message";

    const botHeading = document.createElement("strong");
    botHeading.textContent = "Analytics Assistant";

    const botText = document.createElement("p");
    botText.textContent = "Analyzing your question...";

    botMessage.append(botHeading, botText);
    chatBox.appendChild(botMessage);

    try {
        const response = await fetch(`${API_URL}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: originalQuestion
            })
        });

        if (!response.ok) {
            throw new Error("The backend returned an error.");
        }

        const data = await response.json();
        botText.textContent = data.answer;

    } catch (error) {
        botText.textContent =
            "Unable to connect to the analytics backend.";

        console.error("Chat error:", error);
    }

    questionInput.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;
}