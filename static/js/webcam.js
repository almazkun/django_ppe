const video = document.getElementById('webcam');

navigator.mediaDevices.getUserMedia({ video: true })
.then(function(stream){
    video.srcObject = stream;
})
.catch(function(error) {
    console.error('Error accessing webcam: ', error);
});