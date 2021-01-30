let sio = io("http://127.0.0.1:5000/");
var sid = '';

sio.on("connect", (data) => {
	console.log("connected");
});

sio.on("disconnect", () => {
	console.log("disconnected");
});
