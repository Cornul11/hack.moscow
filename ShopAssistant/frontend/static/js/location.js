let startPos;
let geoOptions = {
    enableHighAccuracy: true,
};

let geoSuccess = function (position) {
    startPos = position;
    document.getElementById('startLat').innerHTML = startPos.coords.latitude;
    document.getElementById('startLon').innerHTML = startPos.coords.longitude;
    const url = 'https://8c93ad47.ngrok.io/geostatus/post/';
    let dataToSend = {lon: startPos.coords.longitude, lat: startPos.coords.latitude};
    axios({
        method: 'post',
        url: url + '?lon=' + startPos.coords.longitude + '&lat=' + startPos.coords.latitude,
        data: ''
    })
        .then(data => console.log('sending: ', data))
};
let geoError = function (error) {
    console.log('Error occurred. Error code: ' + error.code);
    // error.code can be:
    //   0: unknown error
    //   1: permission denied
    //   2: position unavailable (error response from location provider)
    //   3: timed out
};

x = document.getElementsByTagName('body');
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(geoSuccess, geoError, geoOptions);
} else {
    x.innerHTML = "Geolocation is not supported by this browser.";
}

window.setInterval(function () {
        navigator.geolocation.getCurrentPosition(geoSuccess, geoError, geoOptions);
    }, 30000
);