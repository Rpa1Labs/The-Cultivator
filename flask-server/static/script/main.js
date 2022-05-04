function scriptstat(classes, message, temps) {
    var ligne = document.getElementById('contentnotifs').insertRow(0);
    ligne.innerHTML = '<tr><td><div onclick="statremove(this.parentNode.parentNode)" class="message ' + classes + '"><p class="contentmessage">' + message + '</p></div></td>';
    document.getElementById('contentnotifs').style.height = document.getElementById('contentnotifs').offsetHeight + ligne.firstChild.firstChild.firstChild.offsetHeight + 1;
    if (temps != 0) {
        setTimeout(function () { statremove(ligne); }, temps);
    }
    return ligne;
};


function statremove(element) {
    document.getElementById('contentnotifs').style.height = document.getElementById('contentnotifs').offsetHeight - element.firstChild.firstChild.firstChild.offsetHeight - 1;
    element.parentNode.removeChild(element)
};

function closemenu() {
    document.getElementsByClassName("header")[0].style = "";
}
function openmenu() {
    document.getElementsByClassName("header")[0].style.left = "0px";
}

function getPlantDetails(id) {
    // send xhr request to server with id of plant
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/webClientAPI", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        "action": "getPlantDetails",
        "id": id
    }));
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            // display data
            document.getElementById("pid").innerHTML = response["id"];
            document.getElementById("pcx").innerHTML = response["x"] + "mm";
            document.getElementById("pcy").innerHTML = response["y"] + "mm";
            document.getElementById("psa").innerHTML = response["surface"] + " pixels²";
            //if image is not null
            if (response["image"] != null) {
                document.getElementById("pimg").src = "data:image/jpeg;base64," + response["image"];
            }
            scriptstat("vert", "Plante chargée", 2000);
        } else if (xhr.readyState == 4 && xhr.status != 200) {
            scriptstat("rouge", xhr.responseText, 0);
        }

    }

}


function getPlantDetailsSettings(id) {
    // send xhr request to server with id of plant
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/webClientAPI", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        "action": "getPlantDetails",
        "id": id
    }));
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            // display data
            document.getElementById("pid").innerHTML = response["id"];
            document.getElementById("pcx").value = response["x"];
            document.getElementById("pcy").value = response["y"];
            document.getElementById("psa").innerHTML = response["surface"] + " pixels²";
            //if image is not null
            if (response["image"] != null) {
                document.getElementById("pimg").src = "data:image/jpeg;base64," + response["image"];
            }
            scriptstat("vert", "Plante chargée", 2000);
        } else if (xhr.readyState == 4 && xhr.status != 200) {
            scriptstat("rouge", xhr.responseText, 0);
        }

    }

}


function launchPlantAcquisition(id) {
    //get plant id
    id = document.getElementById("pid").innerHTML;

    //check if plant is a number
    if (isNaN(id)) {
        scriptstat("rouge", "Veuillez choisir une plante", 0);
        return;
    }

    //String to int
    id = parseInt(id);

    // send xhr request to server with id of plant
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/webClientAPI", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        "action": "launchPlantAcquisition",
        "id": id
    }));
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var data = JSON.parse(xhr.responseText);
            //get data status
            scriptstat("vert", "Aquisition lancée", 2000);

        }else if(xhr.readyState == 4 && xhr.status != 200){
            scriptstat("rouge", "Erreur: " + xhr.responseText, 0);
        }
    }
}
function launchAcquisition() {
    // send xhr request to server
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/webClientAPI", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        "action": "launchAcquisition"
    }));
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            scriptstat("vert", "Aquisition lancée", 2000);
        } else if (xhr.readyState == 4 && xhr.status != 200) {
            scriptstat("rouge", "Erreur: " + xhr.responseText, 0);
        }
    }

}


function deletePlant() {
    // get plant id
    var id = document.getElementById("pid").innerHTML;
    //check if plant is a number
    if (isNaN(id)) {
        scriptstat("rouge", "Veuillez choisir une plante", 0);
        return;
    }
    //String to int
    id = parseInt(id);
    // user confirmation
    if (!confirm("Voulez-vous vraiment supprimer cette plante ?")) {
        return;
    }
    // send xhr request to server with id of plant
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/webClientAPI", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        "action": "deletePlant",
        "id": id
    }));
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            scriptstat("vert", "Plante supprimée", 2000);
            // reload page
            location.reload();
        } else if (xhr.readyState == 4 && xhr.status != 200) {
            scriptstat("rouge", "Erreur: " + xhr.responseText, 0);
        }
    }
}

function addPlant() {
    // get x and y
    var x = document.getElementById("new_pcx").value;
    var y = document.getElementById("new_pcy").value;
    //check if x and y are numbers
    if (isNaN(x) || isNaN(y)) {
        scriptstat("rouge", "Veuillez choisir une position", 0);
        return;
    }
    //String to int
    x = parseInt(x);
    y = parseInt(y);
    // send xhr request to server with x and y
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/webClientAPI", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        "action": "addPlant",
        "x": x,
        "y": y
    }));
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            scriptstat("vert", "Plante ajoutée", 2000);
            // refresh page
            location.reload();
        } else if (xhr.readyState == 4 && xhr.status != 200) {
            scriptstat("rouge", "Erreur: " + xhr.responseText, 0);
        }
    }
}


function updatePlant(){
    // get plant id
    var id = document.getElementById("pid").innerHTML;
    //check if plant is a number
    if (isNaN(id)) {
        scriptstat("rouge", "Veuillez choisir une plante", 0);
        return;
    }
    //String to int
    id = parseInt(id);

    // get x and y
    var x = document.getElementById("pcx").value;
    var y = document.getElementById("pcy").value;
    //check if x and y are numbers
    if (isNaN(x) || isNaN(y)) {
        scriptstat("rouge", "Veuillez choisir une position", 0);
        return;
    }
    //String to int
    x = parseInt(x);
    y = parseInt(y);

    // send xhr request to server with x and y
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/webClientAPI", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        "action": "updatePlant",
        "id": id,
        "x": x,
        "y": y
    }));
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            scriptstat("vert", "Plante modifiée", 2000);
            // refresh page
            location.reload();
        } else if (xhr.readyState == 4 && xhr.status != 200) {
            scriptstat("rouge", "Erreur: " + xhr.responseText, 0);
        }
    }
}