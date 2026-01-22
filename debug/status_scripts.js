// Script 0


// Script 1


// Script 2


// Script 3


// Script 4


// Script 5

function display_motd() {
var all_motds = Array.from(document.getElementsByClassName('input_motd'));
for (element of all_motds) {
initParser(element.id, element.id);
};
}
function update_one_server_status(server) {
/* Normal Screen view */
server_players = document.getElementById('server_players_' + server.id);
server_motd = document.getElementById('server_motd_' + server.id);
server_version = document.getElementById('server_version_' + server.id);
server_online_status = document.getElementById('server_online_status_' + server.id);
/* Small Screen view */
m_server_players = document.getElementById('m_server_players_' + server.id);
m_server_motd = document.getElementById('m_server_motd_' + server.id);
m_server_version = document.getElementById('m_server_version_' + server.id);
m_server_online_status = document.getElementById('m_server_online_status_' + server.id);
/* TODO Update each element */
if (server.running) {
/* Update Players */
if (server.max != 0) {
server_players.innerHTML = server.online + ` / ` + server.max + ` Max<br />`
}
/* Update Motd */
var motd = "";
if (server.desc) {
if (server.icon) {
img_motd = `<img src="data:image/png;base64,` + server.icon + `" alt="icon" /> `;
m_motd = `<img src="data:image/png;base64,` + server.icon + `" alt="icon" /> `;
}
else {
img_motd = `<img src="/static/assets/images/pack.png" alt="icon" /> `;
m_motd = `<img class="w-25 mr-3" src="/static/assets/images/pack.png" alt="icon" /> `;
}
var desc_motd = `<span id="input_motd_` + server.id + `" class="input_motd align-middle">` + `Loading MOTD` + `</span> <br />`;
m_motd = m_motd + `<div class="media-body"><span id="m_input_motd_` + server.id + `" class="input_motd align-middle">` + `Loading MOTD` + `</span></div>`;
motd = `<div class="row"><div class="col-auto">` + img_motd + `</div><div class="col-auto text-left align-items-center align-content-center">` + desc_motd + `</div></div>`;
server_motd.innerHTML = motd;
m_server_motd.innerHTML = m_motd;
var server_input_motd = document.getElementById('input_motd_' + server.id);
var m_server_input_motd = document.getElementById('m_input_motd_' + server.id);
server_input_motd.innerText = server.desc;
m_server_input_motd.innerText = server.desc;
}
/* Version */
if (server.version) {
server_version.innerHTML = server.version;
m_server_version.innerHTML = server.version;
}
}
else {
server_players.innerHTML = `<span class="text-warning"><i class="fas fa-exclamation-triangle"></i></span>`;
server_motd.innerHTML = `<span class="text-warning"><i class="fa-solid fa-link-slash"></i> </span>`;
server_version.innerHTML = `<span class="text-warning"><i class="fas fa-question"></i></i></span>`;
m_server_motd.innerHTML = `<span class="text-warning"><i class="fas fa-exclamation-triangle"></i> <i class="fa-solid fa-link-slash"></i> </span>`;
}
/* Update Online Status */
var online_status = "";
if (server.running) {
online_status = `<span class="text-success"><i class="fas fa-signal"></i> Online</span>`;
m_online_status = `<span class="text-success"><i class="fas fa-signal"></i>` + server.online + ` / ` + server.max + `</span>`;
}
else {
online_status = `<span class="text-danger"><i class="fas fa-ban"></i> Offline</span>`;
m_online_status = `<span class="text-danger"><i class="fas fa-ban"></i> Offline</span>`;
}
server_online_status.innerHTML = online_status;
m_server_online_status.innerHTML = m_online_status;
}
function update_servers_status(data) {
console.log("update servers");
data.forEach(server => {
console.log(server);
update_one_server_status(server);
});
display_motd();
}
function refreshStatus() {
let xmlHttp = new XMLHttpRequest();
xmlHttp.onreadystatechange = function () {
if (this.readyState == 4 && this.status == 200) {
var myData = JSON.parse(this.responseText);
update_servers_status(myData.data);
}
};
xmlHttp.open('GET', '/api/v2/servers/status', true);
xmlHttp.send();
setTimeout(refreshStatus, 30000);
}
$(document).ready(function () {
console.log("ready!");
refreshStatus();
}());


