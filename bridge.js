const { Server } = require("socket.io");
const { createServer } = require("http");
const fs = require("fs");
const path = require("path");

const PORT = 5050;
const WEB_PORT = 8080;

const httpServer = createServer();
const io = new Server(httpServer, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

io.on("connection", (socket) => {
    console.log(`[Bridge] Client connected: ${socket.id}`);

    if (socket.handshake.query.client === "python-ear") {
        console.log("[Bridge] Python Ear Connected!");
    }

    socket.on("new-translation", (data) => {
        const payload = {
            type: "display-caption",
            original: data.original || "",
            translated: data.translated || "",
            timestamp: data.timestamp || Date.now()
        };

        io.emit("display-caption", payload);
        console.log(`[Bridge] Translation: "${data.translated}"`);
    });

    socket.on("disconnect", () => {
        console.log(`[Bridge] Client disconnected: ${socket.id}`);
    });
});

httpServer.listen(PORT, () => {
    console.log(`[Bridge] Socket.io server live on port ${PORT}`);
});

const mimeTypes = {
    ".html": "text/html",
    ".js": "application/javascript",
    ".css": "text/css",
    ".json": "application/json",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon"
};

const webServer = createServer((req, res) => {
    let urlPath = req.url.split('?')[0];
    let filePath = urlPath === "/" ? "/index.html" : urlPath;
    filePath = path.join(__dirname, filePath);

    const ext = path.extname(filePath);
    const contentType = mimeTypes[ext] || "text/plain";

    fs.readFile(filePath, (err, content) => {
        if (err) {
            if (err.code === "ENOENT") {
                res.writeHead(404, { "Content-Type": "text/html" });
                res.end("<h1>404 Not Found</h1>", "utf-8");
            } else {
                res.writeHead(500);
                res.end("Server Error");
            }
            return;
        }

        res.writeHead(200, { "Content-Type": contentType });
        res.end(content, "utf-8");
    });
});

webServer.listen(WEB_PORT, () => {
    console.log(`[Web] Overlay server running at http://localhost:${WEB_PORT}`);
    console.log(`[Web] Add this URL as an OBS Browser Source`);
});
