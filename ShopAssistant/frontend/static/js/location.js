/*

button.onclick = function () {
    let startPos;

    let geoSuccess = function (position) {
        // Do magic with location
        startPos = position;
        document.getElementById('startLat').innerHTML = startPos.coords.latitude;
        document.getElementById('startLon').innerHTML = startPos.coords.longitude;
    };
    let geoError = function (error) {
        switch (error.code) {
            case error.TIMEOUT:
                // The user didn't accept the callout
                console.log('DENIED!');
                break;
        }
    };

    navigator.geolocation.getCurrentPosition(geoSuccess, geoError);
};
*/
button = document.getElementById("mainButton");

let startPos;
let geoOptions = {
    enableHighAccuracy: true,
    maximumAge: 60 * 1000, // get new position data every minute
};

let geoSuccess = function (position) {
    startPos = position;
    console.log('updated pos');
    document.getElementById('startLat').innerHTML = startPos.coords.latitude;
    document.getElementById('startLon').innerHTML = startPos.coords.longitude;
    const url = 'fillin';
    const params = {
        lon: startPos.coords.latitude,
        lat: startPos.coords.longitude,
    };
    axios({
        method: 'post',
        url: url,
        data: {
            params
        }
    })
        .then(data=>console.log(data))
        .catch(err=>console.log(err));


};
let geoError = function (error) {
    console.log('Error occurred. Error code: ' + error.code);
    // error.code can be:
    //   0: unknown error
    //   1: permission denied
    //   2: position unavailable (error response from location provider)
    //   3: timed out
};

let watchId = navigator.geolocation.watchPosition(geoSuccess, geoError, geoOptions);