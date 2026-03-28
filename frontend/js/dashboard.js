document.addEventListener("DOMContentLoaded", async function () {

  // 🔐 Check login
  const token = localStorage.getItem("token");

  if (!token) {
    window.location.href = "index.html";
    return;
  }
  // Fetch user
  try {
    
    const user = await getCurrentUserAPI();

    document.getElementById("welcome-name").textContent = user.first_name;
    document.getElementById("user-username").textContent = user.username;
    document.getElementById("user-email").textContent = user.email;

    // Fetch alerts
    const alerts = await getUserAlertsAPI();
    showAlerts(alerts);

  } catch (error) {
    console.error("DASHBOARD ERROR:", error);

    alert("Session expired. Please login again.");

    logout();

  }

  // Logout
  const logoutBtn = document.getElementById("logout-btn");

  if (logoutBtn) {
    logoutBtn.addEventListener("click", logout) 
  }
});


// Render Alerts

function showAlerts(alerts) {
  const container = document.getElementById("alerts-list");

  if (!container) return;

  container.innerHTML = "";

  if (!alerts || alerts.length === 0) {
    container.innerHTML = `
      <p class="no-alerts">
        You don't have any alerts yet.<br>
        Click "Create New Alert" to start!
      </p>
    `;
    return;
  }

  const list = document.createElement("div");

  alerts.forEach(alert => {
    const card = document.createElement("div");
    card.className = "alert-card";

    card.innerHTML = `
       <div class="alert-item">
    
          <div class="alert-text">
            <h4>${alert.query}</h4>
            <p>${alert.frequency}</p>
          </div>
     
           <button class="delete-btn" onclick="handleDelete(${alert.id})">
             <span class="material-symbols-outlined">delete</span>
           </button>

        </div>
      `;

    list.appendChild(card);
  });

  container.appendChild(list);
}

async function handleDelete(alertId) {
  const confirmDelete = confirm("Are you sure you want to delete this alert?");
  if (!confirmDelete) return;

  try {
    await deleteAlertAPI(alertId);

    const alerts = await getUserAlertsAPI();
    showAlerts(alerts);

  } catch (error) {
    alert(error.message);
  }
}


//  Logout

function logout() {
  localStorage.removeItem("token");
  window.location.href = "index.html";
}