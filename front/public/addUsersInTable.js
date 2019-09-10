
const addUsersInTable = (() => {
	return (table, users, accessLevel, isIntenalUsers) => {
		for (let user of users) {
			const userTR = document.createElement("tr");
			userTR.setAttribute("id", user.name);

			const userID = document.createElement("td")
			userID.setAttribute("class", "pt-3-half userID");
			userID.setAttribute("contenteditable", false);
			userID.textContent = user.id;

			const userName = document.createElement("td")
			userName.setAttribute("class", "pt-3-half userName");
			userName.setAttribute("contenteditable", accessLevel > 1 && isIntenalUsers);
			userName.textContent = user.name;

			const userAccessLevel = document.createElement("td")
			userAccessLevel.setAttribute("class", "pt-3-half userAccessLevel");
			userAccessLevel.setAttribute("contenteditable", false);
			userAccessLevel.textContent = user.access_level || "-";

			const userType = document.createElement("td")
			userType.setAttribute("class", "pt-3-half userType");
			userType.setAttribute("contenteditable", false);
			userType.textContent = isIntenalUsers ? "Internal" : "External";

			const userPass = document.createElement("td")
			userPass.setAttribute("class", "pt-3-half userPass");
			userPass.setAttribute("contenteditable", false);
			userPass.textContent = "********";

			userTR.appendChild(userID);
			userTR.appendChild(userName);
			userTR.appendChild(userAccessLevel);
			userTR.appendChild(userType);
			userTR.appendChild(userPass);

			if (accessLevel > 2) {
				const removeTD = document.createElement("td");
				const removeSpan = document.createElement("span");
				removeSpan.setAttribute("class", "table-remove");

				if (isIntenalUsers) {
					const removeBtn = document.createElement("button");
					removeBtn.setAttribute("type", "button");
					removeBtn.setAttribute("class", "btn btn-danger btn-rounded btn-sm my-0");
					removeBtn.textContent = "Remove";
					removeSpan.appendChild(removeBtn);
				}

				removeTD.appendChild(removeSpan);
				userTR.appendChild(removeTD);
			}
			table.appendChild(userTR);
		}

		if (accessLevel > 2 && isIntenalUsers) {

			const addUserTR = document.createElement("tr");
			addUserTR.setAttribute("id", "addUser");

			const addUserID = document.createElement("td")
			addUserID.setAttribute("class", "pt-3-half");
			addUserID.setAttribute("contenteditable", false);
			addUserID.textContent = "auto";

			const addUserName = document.createElement("td")
			addUserName.setAttribute("class", "pt-3-half");
			addUserName.setAttribute("id", "addUserName");
			addUserName.setAttribute("contenteditable", true);
			addUserName.textContent = "";

			const addUserAccessLevel = document.createElement("td")
			addUserAccessLevel.setAttribute("class", "pt-3-half");
			addUserAccessLevel.setAttribute("id", "addUserAccessLevel");
			addUserAccessLevel.setAttribute("contenteditable", true);
			addUserAccessLevel.textContent = "";

			const addUserType = document.createElement("td")
			addUserType.setAttribute("class", "pt-3-half");
			addUserType.setAttribute("id", "addUserType");
			addUserType.setAttribute("contenteditable", false);
			addUserType.textContent = "Internal";

			const addUserPass = document.createElement("td")
			addUserPass.setAttribute("class", "pt-3-half");
			addUserPass.setAttribute("id", "addUserPass");
			addUserPass.setAttribute("contenteditable", true);
			addUserPass.textContent = "";

			addUserTR.appendChild(addUserID);
			addUserTR.appendChild(addUserName);
			addUserTR.appendChild(addUserAccessLevel);
			addUserTR.appendChild(addUserType);
			addUserTR.appendChild(addUserPass);

			const addTD = document.createElement("td");
			const addSpan = document.createElement("span");
			addSpan.setAttribute("class", "table");

			const addBtn = document.createElement("button");
			addBtn.setAttribute("type", "button");
			addBtn.setAttribute("class", "btn btn-info btn-rounded btn-sm my-0");
			addBtn.setAttribute("id", "addUserButton");
			addBtn.textContent = "Add";

			addSpan.appendChild(addBtn);
			addTD.appendChild(addSpan);
			addUserTR.appendChild(addTD);
			table.appendChild(addUserTR);
		}
	}
})();
