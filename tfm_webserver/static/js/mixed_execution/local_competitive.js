var CODEFILE, CONFIGFILE;
var ASSETS = [];
var files2delete = [];

function sleepFor( sleepDuration ){
    var now = new Date().getTime();
    while(new Date().getTime() < now + sleepDuration){ /* do nothing */ } 
}

function sendNotebook(f) {
    
    // Get IP address and port of the Notebook Server
    var _ip = document.getElementById("jupyter").getAttribute("_ip");
    var _port = document.getElementById("jupyter").getAttribute("_port");
    
    // List the files to be deleted after the session
    files2delete.push(f[0]);

    // Send the notebook of the exercise to the Notebook Server
    const url = 'http://'+_ip+':'+_port+'/api/contents/' + f[0];
    const data_put = ' {"type": "notebook","format": "json","content": ' + f[1] + '} ';
    const message = {
            headers:{'Content-Type':'application/json',
                     //'Authorization': 'token ' + _token,
                    },
            body:data_put,
            method:"PUT"
    };
    fetch(url,message)
        .then(data=>{return data.json()})
        .then(res=>{console.log(res)})
        .catch(error=>console.log(error))

}

function sendFile(f) {

    // Get IP address and port of the Notebook Server
    var _ip = document.getElementById("jupyter").getAttribute("_ip");
    var _port = document.getElementById("jupyter").getAttribute("_port");

    // List the files to be deleted after the session
    var src = f[0];
    files2delete.push(src);
    if (src.split('.')[1] == 'py') {files2delete.push(src.split('.')[0]+'.pyc');}

    // Send an auxiliary file or image to the Notebook Server
    url = 'http://'+_ip+':'+_port+'/api/contents/'+src
    if (['png','jpg','jpeg','mat','TIF'].indexOf(src.split('.')[1]) >= 0) {
        data_put = ' {"type": "file","format": "base64","content": "' + f[1] + '"} '
    } else {
        data_put = ' {"type": "file","format": "text","content": ' + f[1] + '} '
    }
    const message = {
            headers:{'Content-Type':'application/json',
                     //'Authorization': 'token ' + _token,
                    },
            body:data_put,
            method:"PUT"
    };
    fetch(url,message)
        .then(data=>{return data.json()})
        .then(res=>{console.log(res)})
        .catch(error=>console.log(error))
}

var CODEFILE = document.getElementById("jupyter").getAttribute("codefile");
var CONFIGFILE = document.getElementById("jupyter").getAttribute("configfile");
var ASSETS = document.getElementById("jupyter").getAttribute("assets");

// Send the back-end files of the exercise to the Notebook Server
if (ASSETS) {
    for (var a in JSON.parse(ASSETS)) {       
        sendFile([JSON.parse(ASSETS)[a][0],JSON.parse(ASSETS)[a][1]]);
    }
}
if (CODEFILE) {
    sendFile([JSON.parse(CODEFILE)[0],JSON.parse(CODEFILE)[1]]);
}


// Function to Select one of the codes to run
function player1Selected(username) {
    
    // Player 1
    if (username == "" || username == " ") {
        txtarea = document.getElementById('player1_username');
        txtarea.style = "background:#f39478;" ;
        txtarea.placeholder = "Introduce a valid username!";
    } else {
        // hide modal
        $('#modal_player1').modal('hide');
        // check if user exists in DDBB: AJAX
        $.ajax({
            url: '/validate_username/',
            data: {
              'username': username,
              'exercise_id': document.getElementById("jupyter").getAttribute("exercise")
            },
            dataType: 'json',
            success: function (data) {
              if (data.is_taken) {
                //If the user exists, get its code
                var nbname = JSON.parse(data.notebook)[0];
                var nbcontent = JSON.parse(data.notebook)[1];

                // Rename Notebook (code)
                nbname = 'player1_' + nbname;
                // change topics to connect to the first robot in CONFIGFILE and rename
                var configfile_player1 = JSON.parse(CONFIGFILE)[1];
                configfile_player1 = configfile_player1.replace(/BASETOPIC/g, document.getElementById("jupyter").getAttribute("tpc1"));
                var configfile_player1_name = 'player1_' + JSON.parse(CONFIGFILE)[0];
                // change 'cfgfile' variable in the notebook
                nbcontent = nbcontent.replace("cfgfile = '"+JSON.parse(CONFIGFILE)[0]+"'", "cfgfile = '"+configfile_player1_name+"'");
                nbcontent = nbcontent.replace("nodename = '" + document.getElementById("jupyter").getAttribute("nodename") + "'", "nodename = 'player1'");

                // send new Notebook parameterized for player 1
                sendNotebook([nbname,nbcontent]);
                sendFile([configfile_player1_name,configfile_player1]);

                // Send request of the session (and the notebook) for player 1 to the Notebook Server
                sleepFor(500);
                document.getElementById('ifr1').src = 'http://'+document.getElementById("jupyter").getAttribute("_ip")+':'+document.getElementById("jupyter").getAttribute("_port")+'/notebooks/'+nbname
              } else {
                // if the user doesn't exist in DDBB, display an alert
                Swal.fire({
                    type: 'error',
                    text: 'Oops...',
                    title: 'The user you requested does not exist!',
                });
              }
            }
          });
    }
}

// Function to Select the other code to run
function player2Selected(username) {
    
    // Player 2
    if (username == "" || username == " ") {
        txtarea = document.getElementById('player2_username');
        txtarea.style = "background:#f39478;" ;
        txtarea.placeholder = "Introduce a valid username!";
    } else {
        // hide modal
        $('#modal_player2').modal('hide');
        // check if user exists in DDBB: AJAX
        $.ajax({
            url: '/validate_username/',
            data: {
              'username': username,
              'exercise_id': document.getElementById("jupyter").getAttribute("exercise")
            },
            dataType: 'json',
            success: function (data) {
              if (data.is_taken) {
                //If the user exists, get its code
                var nbname = JSON.parse(data.notebook)[0];
                var nbcontent = JSON.parse(data.notebook)[1];

                // Rename Notebook (code)
                nbname = 'player2_' + nbname;
                // change topics to connect to the first robot in CONFIGFILE and rename
                var configfile_player2 = JSON.parse(CONFIGFILE)[1];
                configfile_player2 = configfile_player2.replace(/BASETOPIC/g, document.getElementById("jupyter").getAttribute("tpc2"));
                var configfile_player2_name = 'player2_' + JSON.parse(CONFIGFILE)[0];

                // change 'cfgfile' variable in the notebook
                nbcontent = nbcontent.replace("cfgfile = '"+JSON.parse(CONFIGFILE)[0]+"'", "cfgfile = '"+configfile_player2_name+"'");
                nbcontent = nbcontent.replace("nodename = '" + document.getElementById("jupyter").getAttribute("nodename") + "'", "nodename = 'player2'");

                // Send request of the session (and the notebook) for player 1 to the Notebook Server
                sendNotebook([nbname,nbcontent]);
                sendFile([configfile_player2_name,configfile_player2]);
                
                sleepFor(500);
                document.getElementById('ifr2').src = 'http://'+document.getElementById("jupyter").getAttribute("_ip")+':'+document.getElementById("jupyter").getAttribute("_port")+'/notebooks/'+nbname
              } else {
                // if the user doesn't exist in DDBB, display an alert
                Swal.fire({
                    type: 'error',
                    text: 'Oops...',
                    title: 'The user you requested does not exist!',
                });
              }
            }
          });
    }  
}

// Set Coordinator in charge of coordinate the starting of the codes
var url = document.getElementById("jupyter").getAttribute("coordinator_url");
// Open a WS connection with the Coordinator Server
var coordinator_ws = new WebSocket(url);
// Set event handlers.
coordinator_ws.onopen = function() {
    console.log("Coordinator WebSocket connection opened");
    setInterval(function(){ coordinator_ws.send("Keep_Alive"); console.log("[Coordinator] Keep Alive to server")}, 1000);

};

coordinator_ws.onclose = function() {
     console.log("[Coordinator] WebSocket connection closed");
};

coordinator_ws.onerror = function(e) {
    console.log("[Coordinator] Coordinator WebSocket Error:" + e)
};
    
function Coordinate_Start(url) {
    /// Send start order to Coordinator Server, which will distribute it to connected clients
    console.log("[Coordinator] Starting...");
    coordinator_ws.send("Start");
}

