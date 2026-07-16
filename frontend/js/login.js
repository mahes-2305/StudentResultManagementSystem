const loginBtn = document.getElementById("loginBtn");

loginBtn.addEventListener("click", async function () {

    const userType = document.getElementById("userType").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    let url;
    let body;

    if (userType === "student") {

        url = "http://127.0.0.1:5000/api/student/login";

        body = {
            roll_no: username,
            password: password
        };

    } else {

        url = "http://127.0.0.1:5000/api/admin/login";

        body = {
            username: username,
            password: password
        };

    }

    console.log("Sending request...");
    console.log(url);
    console.log(body);

    try {

        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        console.log("Status:", response.status);

        const data = await response.json();

        console.log(data);

        if (data.success) {

    if (userType === "student") {

        localStorage.setItem("roll_no", data.student.roll_no);

        window.location.href = "result.html";

    } else {

        window.location.href = "admin.html";

    }

} else {

    alert(data.message);

}

    } catch (error) {

        console.error(error);
        alert("Cannot connect to backend");

    }

});