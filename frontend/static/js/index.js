let isLoading = false;
let isError = false;

// url to the backend server
const apiUrl = "http://localhost:82/appeal";

const redBored = "1px solid red";
const defaultBorder = "";
const emptyField = "";

window.onload = function () {
    const form = document.querySelector("#form");
    const dialog = document.querySelector("#dialog");
    const closeDialogBtn = document.querySelector("#dialog-btn");

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        if (isLoading) return;

        isLoading = true;

        const name = event.target.elements.name;
        const secondName = event.target.elements.secondName;
        const patronymic = event.target.elements.patronymic;
        const phone = event.target.elements.phone;
        const message = event.target.elements.message;

        const formFields = [name, secondName, patronymic, phone, message];

        const data = {
            last_name: secondName.value,
            first_name: name.value,
            patronymic: patronymic.value,
            phone_number: phone.value,
            message: message.value,
        };

        // validation
        formFields.forEach((field) => {
            if (field.value === emptyField) {
                field.style.border = redBored;
            } else {
                field.style.border = defaultBorder;
            }
        });

        const dataValues = Object.values(data);

        isError = dataValues.some((v) => v === "");

        if (isError) {
            isLoading = false;
            return;
        }

        // send to the backend
        fetch(apiUrl, {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json",
            },
            crossDomain: true,
        })
            .then((res) => {
                if (res.status) {
                    name.value = "";
                    secondName.value = "";
                    patronymic.value = "";
                    phone.value = "";
                    message.value = "";
                    dialog.style.display = "block";
                }
            })
            .catch((_ex) => {
                console.log("Error index.js: ", _ex);
            })
            .finally(() => (isLoading = false));
        return false;
    });

    closeDialogBtn.addEventListener("click", () => {
        dialog.style.display = "none";
    });
};
