let startPos;
let geoOptions = {
    enableHighAccuracy: true,
    maximumAge: 60 * 1000, // get new position data every minute
};

let geoSuccess = function (position) {
    startPos = position;
    document.getElementById('startLat').innerHTML = startPos.coords.latitude;
    document.getElementById('startLon').innerHTML = startPos.coords.longitude;
    const url = 'https://8c93ad47.ngrok.io/geostatus/post/';
    const params = {
        lon: startPos.coords.latitude,
        lat: startPos.coords.longitude,
    };
    dataToSend = {lon: startPos.coords.longitude, lat: startPos.coords.latitude};
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
    navigator.geolocation.getCurrentPosition(geoSuccess);
} else {
    x.innerHTML = "Geolocation is not supported by this browser.";
}

navigator.geolocation.getCurrentPosition(geoSuccess, geoError, geoOptions);
let watchId = navigator.geolocation.watchPosition(geoSuccess, geoError, geoOptions);