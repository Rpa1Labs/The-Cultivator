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
            scriptstat("vert", "Plante chargée", 2000);
        } else if (xhr.readyState == 4 && xhr.status != 200) {
            scriptstat("rouge", xhr.responseText, 0);
        }

    }

}
function launchPlantAcquisition(id) {
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
