const sio = io("http://127.0.0.1:5000/");
var sid = '';

sio.on("connect", (data) => {
	console.log("connected");
	if (userName) {
		sio.emit("message", userName);
	}
});

sio.on("disconnect", () => {
	console.log("disconnected");
});

sio.on('reply', (data) => {
	console.log(data);
	if (sid != data['sid']) {
		console.log(data);
	}
})