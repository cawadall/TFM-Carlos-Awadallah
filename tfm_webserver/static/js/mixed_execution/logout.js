
function del_code(ip,port,src) { //(ip,port,token,src) {
    // Eliminar un fichero del Notebook Server
    src_del='http://' + ip + ':' + port + '/api/contents/' + src
    const message = {
            headers:{
                     //'Authorization': 'token ' + token,
                    },
            method:"DELETE"
    };
    fetch(src_del,message)
        .then(data=>{return data.json()})
        .then(res=>{console.log(res)})
        .catch(error=>console.log(error))
}

function deleteKernel() {
    var _ip = document.getElementById("jupyter").getAttribute("_ip");
    var _port = document.getElementById("jupyter").getAttribute("_port");
    //var _token = document.getElementById("jupyter").getAttribute("_token");
    var _session = document.getElementById("jupyter").getAttribute("_session");
    var code_files = document.getElementById("jupyter").getAttribute("_files");
    var code_files_list = JSON.parse(code_files);
    
    // Eliminar Session y Kernel
    const src_session='http://' +_ip + ':' +_port + '/api/sessions/' + _session
    const message = {
            headers:{
                     //'Authorization': 'token ' + _token,
                    },
            method:"DELETE"
    };
    fetch(src_session,message)
        .then(data=>{return data.json()})
        .then(res=>{console.log(res)})
        .catch(error=>console.log(error))
    // Eliminar código
    for (var f in code_files_list) {
        del_code(_ip,_port,code_files_list[f]); //del_code(_ip,_port,_token,code_files[f]);
        console.log("DELETED "+code_files_list[f]);
    }
      
}

deleteKernel();
