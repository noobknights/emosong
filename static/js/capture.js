var isCameraAllowed = false;
var imageData = '';
(function () {
	// The width and height of the captured photo. We will set the
	// width to the value defined here, but the height will be
	// calculated based on the aspect ratio of the input stream.

	var width = 300; // We will scale the photo width to this
	var height = 0; // This will be computed based on the input stream

	// |streaming| indicates whether or not we're currently streaming
	// video from the camera. Obviously, we start at false.

	var streaming = false;

	// The various HTML elements we need to configure or control. These
	// will be set by the startup() function.

	var video = null;
	var canvas = null;
	var photo = null;
	var startbutton = null;

	function startup() {
		video = document.getElementById("video");
		canvas = document.getElementById("canvas");
		photo = document.getElementById("photo");
		startbutton = document.getElementById("startbutton");

		navigator.mediaDevices
			.getUserMedia({ video: true, audio: false })
			.then(function (stream) {
				isCameraAllowed = true;
				video.srcObject = stream;
				video.play();
			})
			.catch(function (err) {
				isCameraAllowed = false;
				console.log("An error occurred: " + err);
			});

		video.addEventListener(
			"canplay",
			function (ev) {
				if (!streaming) {
					height = video.videoHeight / (video.videoWidth / width);

					// Firefox currently has a bug where the height can't be read from
					// the video, so we will make assumptions if this happens.

					if (isNaN(height)) {
						height = width / (4 / 3);
					}

					video.setAttribute("width", width);
					video.setAttribute("height", height);
					canvas.setAttribute("width", width);
					canvas.setAttribute("height", height);
					streaming = true;
				}
			},
			false
		);

		console.log({ isCameraAllowed });

		startbutton.addEventListener(
			"click",
			function (ev) {
				takepicture();
				ev.preventDefault();
			},
			false
		);
		clearphoto();
	}

	// Fill the photo with an indication that none has been
	// captured.

	function clearphoto() {
		var context = canvas.getContext("2d");
		context.fillStyle = "#AAA";
		context.fillRect(0, 0, canvas.width, canvas.height);

		var data = canvas.toDataURL("image/png");
		photo.setAttribute("src", data);
	}

	// Capture a photo by fetching the current contents of the video
	// and drawing it into a canvas, then converting that to a PNG
	// format data URL. By drawing it on an offscreen canvas and then
	// drawing that to the screen, we can change its size and/or apply
	// other changes before drawing it.

	function takepicture() {
		var context = canvas.getContext("2d");
		if (width && height) {
			canvas.width = width;
			canvas.height = height;
			context.drawImage(video, 0, 0, width, height);

			var data = canvas.toDataURL("image/png");
			imageData = data
			photo.setAttribute("src", data);
		} else {
			clearphoto();
		}
	}

	// Set up our event listener to run the startup process
	// once loading is complete.
	window.addEventListener("load", startup, false);
})();

function dataURLtoFile(dataurl, filename) {

	var arr = dataurl.split(','),
		mime = arr[0].match(/:(.*?);/)[1],
		bstr = atob(arr[1]),
		n = bstr.length,
		u8arr = new Uint8Array(n);

	while (n--) {
		u8arr[n] = bstr.charCodeAt(n);
	}

	return new File([u8arr], filename, { type: mime });
}