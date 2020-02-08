var session;
var files2delete = [];
function displayModal() {
    var modal = document.getElementById('myModal');
    modal.style.display = "block";
}

function closeModal() {
    var modal = document.getElementById('myModal');
    modal.style.display = "none";
}

function sleepFor( sleepDuration ){
    var now = new Date().getTime();
    while(new Date().getTime() < now + sleepDuration){ /* do nothing */ } 
}

function postNotebook() {
    
    var _ip = document.getElementById("jupyter").getAttribute("_ip");
    var _port = document.getElementById("jupyter").getAttribute("_port");
    var nbname = JSON.parse(document.getElementById("jupyter").getAttribute("nbcontent"))[0];
    var nbcontent = JSON.parse(document.getElementById("jupyter").getAttribute("nbcontent"))[1];

    files2delete.push(nbname);
    //var _token = document.getElementById("jupyter").getAttribute("_token");

    const url = 'http://'+_ip+':'+_port+'/api/contents/' + nbname;
    const data_put = ' {"type": "notebook","format": "json","content": ' + nbcontent + '} ';
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

function sendCode() {

    var codefile = document.getElementById("jupyter").getAttribute("codefile");
    var configfile = document.getElementById("jupyter").getAttribute("configfile");
    var _ip = document.getElementById("jupyter").getAttribute("_ip");
    var _port = document.getElementById("jupyter").getAttribute("_port");
    //var _token = document.getElementById("jupyter").getAttribute("_token");
    var assets = document.getElementById("jupyter").getAttribute("assets");
    var base64img = document.getElementById("jupyter").getAttribute("base64img");
    var files = [];
    if (codefile) {
        files.push([JSON.parse(codefile)[0],JSON.parse(codefile)[1]]);
    }
    if (configfile) {
        files.push([JSON.parse(configfile)[0],JSON.parse(configfile)[1]]);
    } 
    if (assets) {
        for (var a in JSON.parse(assets)) {       
            files.push([JSON.parse(assets)[a][0],JSON.parse(assets)[a][1]]);
        }
    } 

    for (var f in files) {
        var src = files[f][0];
        files2delete.push(src);
        if (src.split('.')[1] == 'py') {files2delete.push(src.split('.')[0]+'.pyc');}
        url = 'http://'+_ip+':'+_port+'/api/contents/'+src
        if (['png','jpg','jpeg','mat','TIF'].indexOf(src.split('.')[1]) >= 0) {
            data_put = ' {"type": "file","format": "base64","content": "' + files[f][1] + '"} '
        } else {
            data_put = ' {"type": "file","format": "text","content": ' + files[f][1] + '} '
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

}

function startKernel() {
    var _ip = document.getElementById("jupyter").getAttribute("_ip");
    var _port = document.getElementById("jupyter").getAttribute("_port");
    var nbname = JSON.parse(document.getElementById("jupyter").getAttribute("nbcontent"))[0];
    //var _token = document.getElementById("jupyter").getAttribute("_token");
    const url = 'http://'+_ip+':'+_port+'/api/sessions';
    const data_post = '{"name": "' + nbname + '","path":"' + nbname + '","type": "notebook","kernel": {"name": "python2"}}';
    const message = {
            headers:{'Content-Type':'application/json',
                     //'Authorization': 'token ' + _token,
                    },
            body:data_post,
            method:"POST"
    };
    fetch(url,message)
        .then(data=>{return data.json()})
        .then(res=>{
            session = res.id;
            document.getElementById('session').value = session;
        })
        .catch(error=>console.log(error))
}

postNotebook();
console.log("NOTEBOOK COPIED");
sleepFor(500);
sendCode();
console.log("CODE FILES SENT");
startKernel();
console.log("SESSION AND KERNEL STARTED");

//document.getElementById('ifr').src = 'http://'+document.getElementById("jupyter").getAttribute("_ip")+':'+document.getElementById("jupyter").getAttribute("_port")+'/notebooks/'+document.getElementById("jupyter").getAttribute("nbname")

function logout() {
    var _ip = document.getElementById("jupyter").getAttribute("_ip");
    var _port = document.getElementById("jupyter").getAttribute("_port");
    var nbname = JSON.parse(document.getElementById("jupyter").getAttribute("nbcontent"))[0];
    //var _token = document.getElementById("jupyter").getAttribute("_token");

    document.getElementById('files2delete').value = JSON.stringify(files2delete);
    console.log(files2delete);

    const url = 'http://'+_ip+':'+_port+'/api/contents/' + nbname;
    const message = {
            headers:{
                     //'Authorization': 'token ' + _token,
                    },
            method:"GET"
    };
    fetch(url,message)
        .then(data=>{return data.json()})
        .then(res=>{
            console.log(res);
            filled_notebook = res.content;
            console.log(filled_notebook);
            console.log(JSON.stringify(filled_notebook));
            document.getElementById('fillednb').value = JSON.stringify(filled_notebook);
        })
        .catch(error=>console.log(error))
}
