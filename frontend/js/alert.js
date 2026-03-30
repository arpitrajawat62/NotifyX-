document.addEventListener("DOMContentLoaded", () => {

    const token = localStorage.getItem("token");
    if(!token){
        window.location.href = "login.html";
        return;
    }

    const form = document.getElementById('alertForm');

    if(!form){
        console.error("Form not found");
        return;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const query = document.getElementById("query").value.trim();
        const frequency = document.getElementById("frequency").value;

        if(!query){
            alert("Please enter a alert name!");
            return;
        }
        const data  = { query, frequency };

        try{
            await createAlertAPI(data);

            alert("Alert created successfully");
            window.location.href = "dashboard.html";

        } catch{
            console.error("Create alert error:", error);
            alert(error.message || "Could not create alert. Try again. ");
        }
    });
});