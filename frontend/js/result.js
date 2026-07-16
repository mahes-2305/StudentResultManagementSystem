const rollNo = localStorage.getItem("roll_no");

if (!rollNo) {
    alert("Please login first.");
    window.location.href = "index.html";
}

fetch(`http://127.0.0.1:5000/api/result/${rollNo}`)
    .then(response => response.json())
    .then(data => {

        if (!data.success) {
            alert(data.message);
            return;
        }

        document.getElementById("name").innerText = data.student.name;
        document.getElementById("roll").innerText = data.student.roll_no;
        document.getElementById("department").innerText = data.student.department;
        document.getElementById("total").innerText = data.total;
        document.getElementById("percentage").innerText = data.percentage;
        document.getElementById("grade").innerText = data.grade;

        const table = document.getElementById("marksTable");

        data.results.forEach(result => {

            table.innerHTML += `
                <tr>
                    <td>${result.subject}</td>
                    <td>${result.marks}</td>
                </tr>
            `;

        });

    })
    .catch(error => {
        console.error(error);
        alert("Unable to load result.");
    });