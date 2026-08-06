const express = require("express");
const cors = require("cors");
const http = require("http");
const { Server } = require("socket.io");
const { spawn } = require("child_process");
const path = require("path");

require("dotenv").config();

const connectDB = require("./config/db");

const authRoutes = require("./routes/authRoutes");
const bedRoutes = require("./routes/bedRoutes");
const ocrRoutes = require("./routes/ocrRoutes");
const hospitalRoutes = require("./routes/hospitalRoutes");

const app = express();
const server = http.createServer(app);

// =============================
// Socket.IO
// =============================
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
  },
});

// Make io available everywhere
app.set("io", io);

io.on("connection", (socket) => {
  console.log("🟢 Client Connected:", socket.id);

  socket.on("disconnect", () => {
    console.log("🔴 Client Disconnected:", socket.id);
  });
});

// =============================
// Database
// =============================
connectDB();

// =============================
// Middleware
// =============================
app.use(cors());
app.use(express.json());

// =============================
// Routes
// =============================
app.use("/api/auth", authRoutes);
app.use("/api/beds", bedRoutes);
app.use("/api", ocrRoutes);
app.use("/api/hospitals", hospitalRoutes);

app.get("/", (req, res) => {
  res.send("API Running 🚀");
});


const Bed = require("./models/Bed");
const {
  startWorker,
} = require("./workers/workerManager");
// =============================
// Start Flask Automatically
// =============================

const pythonPath = process.env.PYTHON_PATH;

console.log("Starting Flask...");
console.log("Python:", pythonPath);

const flask = spawn(
  pythonPath,
  ["app.py"],
  {
    cwd: path.join(__dirname, "YOLO_TEST"),
    shell: false,
  }
);

flask.stdout.on("data", (data) => {
  console.log(`[Flask] ${data.toString().trim()}`);
});

flask.stderr.on("data", (data) => {
  console.error(`[Flask Error] ${data.toString().trim()}`);
});

flask.on("close", (code) => {
  console.log(`Flask exited with code ${code}`);
});

flask.on("error", (err) => {
  console.error("Failed to start Flask:", err.message);
});

// =============================
// Close Flask when Node exits
// =============================
process.on("SIGINT", () => {
  console.log("\nStopping Flask...");
  flask.kill();
  process.exit();
});

process.on("SIGTERM", () => {
  flask.kill();
  process.exit();
});

// =============================
// Start Server
// =============================
const PORT = process.env.PORT || 5000;

server.listen(PORT, async () => {

  console.log(`🚀 Server running on ${PORT}`);

  try {

    const beds = await Bed.find();

    console.log(`Found ${beds.length} beds`);

    for (const bed of beds) {

      if (
        bed.cameraStatus === "online" &&
        bed.streamUrl &&
        bed.streamUrl.trim() !== ""
      ) {

        startWorker(bed);

      }

    }

  } catch (err) {

    console.log(err);

  }

});