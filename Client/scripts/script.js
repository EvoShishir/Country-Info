const API_BASE = "http://localhost:8000/api";
const token = localStorage.getItem("countries_token");
const headers = {
  Authorization: `Bearer ${token}`,
};

// DOM Elements
const tableBody = document.getElementById("countryTable");
const regionalList = document.getElementById("regionalList");
const languageList = document.getElementById("languageList");
const detailsModal = document.getElementById("detailsModal");

async function verifyToken() {
  if (!token) {
    alert("No token found. Please log in.");
    return redirectToLogin();
  }

  try {
    const res = await fetch(`${API_BASE}/token/verify`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token }),
    });

    if (!res.ok) {
      throw new Error("Invalid or expired token");
    }

    fetchCountries(); // Only fetch countries if token is valid
  } catch (err) {
    console.error("Token verification failed:", err);
    alert("Session expired. Please log in again.");
    localStorage.removeItem("countries_token");
    redirectToLogin();
  }
}

function redirectToLogin() {
  window.location.href = "login.html"; // Or your actual login page
}

function renderCountries(countries) {
  tableBody.innerHTML = "";

  countries.forEach((country) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${country.name}</td>
      <td>${country.cca2}</td>
      <td>${country.capital}</td>
      <td>${country.population.toLocaleString()}</td>
      <td>${country.timezone}</td>
      <td>${country.flag}</td>
      <td><button class="btn btn-sm btn-info" onclick="showDetails(${
        country.id
      })">Details</button></td>
    `;
    tableBody.appendChild(row);
  });
}

async function fetchCountries() {
  try {
    const res = await fetch(`${API_BASE}/countries`, { headers });
    const data = await res.json();
    renderCountries(data);
    console.log(data);
  } catch (err) {
    console.error("Error fetching countries:", err);
    alert("Failed to fetch countries.");
  }
}

async function handleSearch(query) {
  if (!query.trim()) return fetchCountries();

  try {
    const res = await fetch(`${API_BASE}/countries/search/?query=${query}`, {
      headers,
    });
    const data = await res.json();
    renderCountries(data);
  } catch (err) {
    console.error("Search failed:", err);
  }
}

async function showDetails(countryId) {
  try {
    const [regionRes, languageRes] = await Promise.all([
      fetch(`${API_BASE}/countries/${countryId}/regional-countries`, {
        headers,
      }),
      fetch(`${API_BASE}/countries/${countryId}/same-language`, { headers }),
    ]);

    const [regionalCountries, languageCountries] = await Promise.all([
      regionRes.json(),
      languageRes.json(),
    ]);

    regionalList.textContent = regionalCountries.Countries?.map(
      (country) => country.name
    ).join(", ");
    languageList.textContent = languageCountries.Countries?.map(
      (country) => country.name
    ).join(", ");
    detailsModal.classList.remove("d-none");
  } catch (err) {
    console.error("Error loading details:", err);
    alert("Failed to fetch details.");
  }
}

// Start by verifying the token
verifyToken();

// Close the modal and remove the blur effect from background
function closeModal() {
  detailsModal.classList.add("d-none");
  document.body.classList.remove("modal-open"); // Remove blur from background
}
