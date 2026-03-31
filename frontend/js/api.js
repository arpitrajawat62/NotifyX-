const API = "http://localhost:8000";

// Login form 
async function loginUser(username, password) {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const response = await fetch(API + "/auth/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData
    });

    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || `Login failed (${response.status})`);
    }

    return response.json();
}

// Register form 
async function registerUser(user) {
    const response = await fetch(API + "/auth/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user)
    });

    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(JSON.stringify(err)); 
    }

    return response.json();
}

// CreateAlert
async function createAlertAPI(data) {
    const token = localStorage.getItem("token");
    if (!token) throw new Error("Not logged in. Please login again.");

    const response = await fetch(API + "/alerts", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || "Failed to create alert");
    }

    return response.json();
}

//  Delete alert
async function deleteAlertAPI(alertId) {
    const token = localStorage.getItem("token");
    if(!token) throw new error("Not logges in");

    const response = await fetch(API + `/alerts/&{alertId}`,{
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if(!response.ok){
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || "Failed to delete alert");
    }
    return response.json();
    
}

async function deleteAlertAPI(alertId) {
    const token = localStorage.getItem("token");

    const response = await fetch(API + `/alerts/${alertId}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || "Failed to delete alert");
    }

    return response.json();
}


// Get current user info
async function getCurrentUserAPI() {
    const token = localStorage.getItem("token");
    if (!token) throw new Error("Not logged in");

    
    const response = await fetch(API + "/auth/me", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || "Failed to load user info");
    }
    return response.json();
}

// Get all alerts of current user
async function getUserAlertsAPI() {

    const token = localStorage.getItem("token");
    if (!token) throw new Error("Not logged in");

    const response = await fetch(API + "/alerts", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || "Failed to load user info");
    }
    return response.json(); 
 
}