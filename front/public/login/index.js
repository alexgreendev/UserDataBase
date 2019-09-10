const form = document.getElementById("form");
const submit = document.getElementById("submit");

submit.addEventListener('click', (e) => {
	e.preventDefault();

	const name = document.getElementById("username").value;
	const password = document.getElementById("password").value;

	postData('/api/v1/login/', { name, password })
	  .then(data => {
	    console.log(data)
	    if (data.success === true) {
	        const user = data.user;
	        localStorage.setItem("name", user.name);
	        localStorage.setItem("access_level", user.access_level);
	        localStorage.setItem("token", user.token);
	        location.href = "/";
	    } else {
			alert("incorrect login or password");
	    }
	  })
	  .catch(error => console.error(error));
});

function postData(url = '', data = {}) {
    return fetch(url, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
        body: JSON.stringify(data),
    })
    .then(response => response.json());
}