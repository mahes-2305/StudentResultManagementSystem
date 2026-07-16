document.getElementById("addStudentBtn").addEventListener("click", async () => {

    const name = document.getElementById("name").value;
    const roll_no = document.getElementById("roll_no").value;
    const department = document.getElementById("department").value;
    const password = document.getElementById("password").value;

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/student",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    name,
                    roll_no,
                    department,
                    password
                })
            }
        );

        const data = await response.json();

        alert(data.message);

    } catch (error) {

        console.error(error);

        alert("Unable to connect to backend.");

    }

});