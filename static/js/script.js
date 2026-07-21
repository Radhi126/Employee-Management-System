// Search Employee
function searchEmployee() {

    let value = document.getElementById("searchInput").value.toLowerCase();

    let rows = document.querySelectorAll("#employeeTable tbody tr");

    rows.forEach(function(row) {

        let text = row.innerText.toLowerCase();

        if (text.includes(value)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }

    });
}

function editEmployee(id, name, age, gender, department, designation, salary, phone, email, address) {

    document.getElementById("emp_id").value = id;
    document.getElementById("emp_name").value = name;
    document.getElementById("age").value = age;
    document.getElementById("gender").value = gender;
    document.getElementById("department").value = department;
    document.getElementById("designation").value = designation;
    document.getElementById("salary").value = salary;
    document.getElementById("phone").value = phone;
    document.getElementById("email").value = email;
    document.getElementById("address").value = address;

    document.getElementById("submitBtn").textContent = "Update Employee";

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

function resetEmployeeForm() {

    document.querySelector(".employee-form form").reset();

    document.getElementById("emp_id").value = "";

    document.getElementById("submitBtn").textContent = "💾 Save Employee";

    document.getElementById("formTitle").textContent = "Add / Update Employee";
}

function editDepartment(id, name) {

    document.getElementById("dept_id").value = id;

    document.getElementById("dept_name").value = name;

    document.getElementById("deptSubmitBtn").textContent = "Update Department";

    document.getElementById("deptFormTitle").textContent = "Update Department";

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}

function searchDepartment() {

    let input = document.getElementById("departmentSearch").value.toLowerCase();

    let rows = document.querySelectorAll("#departmentTable tbody tr");

    rows.forEach(function(row) {

        let text = row.innerText.toLowerCase();

        if (text.includes(input)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }

    });

}

setTimeout(function(){

    let alerts = document.querySelectorAll(".alert");

    alerts.forEach(function(alert){

        alert.style.transition = "0.5s";
        alert.style.opacity = "0";

        setTimeout(function(){

            alert.remove();

        },500);

    });

},3000);
