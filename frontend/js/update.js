document.getElementById("updateBtn").addEventListener("click", async () => {

    const roll_no = document.getElementById("roll_no").value;
    const subject = document.getElementById("subject").value;
    const marks = Number(document.getElementById("marks").value);

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/marks",
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    roll_no,
                    subject,
                    marks
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
