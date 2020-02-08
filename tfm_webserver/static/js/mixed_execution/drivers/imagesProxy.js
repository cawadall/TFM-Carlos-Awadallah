///////////////////////////////////////////////////////////////////////////////
//     C A M E R A      A C C E S S    T H R O U G H     W E B R T C         //
///////////////////////////////////////////////////////////////////////////////

function hasGetUserMedia() {
  return !!(navigator.getUserMedia || navigator.webkitGetUserMedia ||
            navigator.mozGetUserMedia || navigator.msGetUserMedia);
}

var errorCallback = function(e) {
    console.log('Rejected!', e);
    errorElement = document.getElementById('error');
    error.display = 'block';
};


function init() {

    // Normalize the various vendor prefixed versions of getUserMedia.
    navigator.getUserMedia = (navigator.getUserMedia ||
                            navigator.webkitGetUserMedia ||
                            navigator.mozGetUserMedia || 
                            navigator.msGetUserMedia);

    if (!hasGetUserMedia()) {
        alert('getUserMedia() is not supported in your browser');
    } else {
        videoElement = document.createElement('video');
        navigator.getUserMedia({video: true, audio: false}, function(localMediaStream) {
            videoElement.srcObject = localMediaStream;
            videoElement.muted = true;
            videoElement.play();
            videoElement.style = 'display:none';
            document.getElementById("videodiv").appendChild(videoElement);
            streamingOverWebsockets(); 
        }, errorCallback);
    }
}

/*function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}*/

var attempt = 0;
async function streamingOverWebsockets() {
            
    if ("WebSocket" in window) {
       //alert("WebSocket is supported by your Browser!");
       
       video = document.getElementsByTagName('video')[0];
       // returns a frame encoded in base64
       const getFrame = () => {
           const canvas = document.createElement('canvas');
           canvas.width = video.videoWidth;
           canvas.height = video.videoHeight;
           canvas.getContext('2d').drawImage(video, 0, 0);
           const data = canvas.toDataURL('image/png');
           //console.log(data);
           return data;
       }
       const WS_URL = 'ws://127.0.0.1:8889/';
       const FPS = 20;
       //var connected = false;
       var ws;
       //var attempt = 0;
       /*while (!connected) {
           if (attempt < 50) {
               ws = new WebSocket(WS_URL);
               console.log(ws.readyState);
               if (ws.readyState == 0 || ws.readyState == 3) {
                    attempt ++;
                    console.log('[WARNING] Unable to connect. Retrying...' + '[ ATTEMPT: ' + attempt + ' ]'); 
               } else {
                   console.log('tetas');
                   connected = true;
               }
           } else {
               alert('[ERROR] Images Server not Available');
               break;
           }
       }*/
       ws = new WebSocket(WS_URL);
           
       ws.onopen = function() {
           console.clear();
           console.log('Connected to ${WS_URL}');
           setInterval( function () {
               ws.send(getFrame());
           }, 1000 / FPS);
       }
           
       ws.onclose = async (event) => {
           attempt ++;
           console.clear();
           console.error(event);
           console.log('[WARNING] Unable to connect. Retrying... [ ATTEMPT: ' + attempt + ' ]');
           if (attempt != 50) {
               streamingOverWebsockets();
           } else {
               alert('[ERROR] Images Server not Available. Ensure you have run the exercise Configuration Cell');
               streamingOverWebsockets();
           }
       }

    } else {
       // The browser doesn't support WebSocket
       alert("WebSocket NOT supported by your Browser!");
    }
 }
