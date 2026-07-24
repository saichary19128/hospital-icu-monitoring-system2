let liveData = {};

// ===============================
// UPDATE OCR
// ===============================
exports.updateOCR = (req, res) => {

  const { bedId, ocr } = req.body;

  // Store latest values
  liveData[String(bedId)] = {
    ...ocr,
    updatedAt: new Date(),
  };

  console.log("🔥 LIVE OCR:", liveData);

  // ===============================
  // Emit to all connected clients
  // ===============================
  const io = req.app.get("io");

  if (io) {
    io.emit("vitals", liveData);
  }

  res.json({
    success: true,
    message: "OCR updated successfully",
  });

};

// ===============================
// GET CURRENT OCR
// (kept for debugging)
// ===============================
exports.getOCR = (req, res) => {

  res.json(liveData);

};



// let liveData = {}; // 🔥 store OCR in memory

// exports.updateOCR = (req, res) => {
//   const { bedId, ocr } = req.body;

//   liveData[bedId] = {
//     ...ocr,
//     updatedAt: new Date(),
//   };

//   res.json({ msg: "OCR updated" });
// };

// exports.getOCR = (req, res) => {
//   res.json(liveData);
// };