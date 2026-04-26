// history.js — Fetch and display prediction history (Flask + SQLite)

// --------------------
// AUTH CHECK
// --------------------
requireAuth(); // Ensure the global auth guard is called

const API_BASE = "http://127.0.0.1:5000";

// IMPORTANT: matches history.html
const itemsContainer = document.getElementById("history-list");
const clearBtn = document.getElementById("clear-history");

// Get logged-in user
const user = JSON.parse(localStorage.getItem("wheatshield_user"));

/** * FIX: Check if the user object exists. 
 * We use the email as a fallback if 'id' is missing to prevent unnecessary logouts.
 */
if (!user || (!user.id && !user.email)) {
  alert("Session expired. Please login again.");
  window.location.href = "login.html";
}

// Set a reliable ID for the API requests
const currentUserId = user.id || user.email;

// --------------------
// FETCH HISTORY
// --------------------
// Use 'currentUserId' instead of 'user.id'
fetch(`${API_BASE}/history?user_id=${currentUserId}`)
  .then(res => {
    if (!res.ok) throw new Error("Failed to fetch history");
    return res.json();
  })
  .then(rows => {
    if (!rows || rows.length === 0) {
      itemsContainer.innerHTML =
        `<p style="color:var(--muted)">No history available yet.</p>`;
      return;
    }

    // Create table
    const table = document.createElement("table");
    table.style.width = "100%";
    table.style.borderCollapse = "collapse";

    table.innerHTML = `
      <thead>
        <tr style="text-align:left;border-bottom:1px solid #e6f0ea">
          <th style="padding:10px">Date</th>
          <th style="padding:10px">Disease</th>
          <th style="padding:10px">Confidence</th>
          <th style="padding:10px">Severity</th>
        </tr>
      </thead>
      <tbody></tbody>
    `;

    const tbody = table.querySelector("tbody");

    rows.forEach(item => {
      const confPct = Math.round(item.confidence * 100);

      const tr = document.createElement("tr");
      tr.style.borderBottom = "1px solid #f0f0f0";

      let sevColor = "#27ae60";
      if (item.severity.toLowerCase().includes("medium")) sevColor = "#f39c12";
      if (item.severity.toLowerCase().includes("high")) sevColor = "#e74c3c";

      tr.innerHTML = `
        <td style="padding:10px">${item.created_at}</td>
        <td style="padding:10px"><strong>${item.disease}</strong></td>
        <td style="padding:10px">${confPct}%</td>
        <td style="padding:10px; color:${sevColor}; font-weight:600">
          ${item.severity}
        </td>
      `;

      tbody.appendChild(tr);
    });

    itemsContainer.innerHTML = "";
    itemsContainer.appendChild(table);
  })
  .catch(err => {
    console.error(err);
    itemsContainer.innerHTML =
      `<p style="color:#b00020">Failed to load history. Make sure the backend is running.</p>`;
  });

// --------------------
// CLEAR HISTORY
// --------------------
clearBtn.addEventListener("click", async () => {
  if (!confirm("Are you sure you want to clear all history?")) return;

  try {
    const res = await fetch(`${API_BASE}/history/clear`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: currentUserId }) // Updated to use currentUserId
    });

    if (res.ok) {
      itemsContainer.innerHTML =
        `<p style="color:var(--muted)">History cleared.</p>`;
    } else {
      alert("Failed to clear history.");
    }
  } catch (err) {
    console.error(err);
    alert("Network error. Could not clear history.");
  }
});