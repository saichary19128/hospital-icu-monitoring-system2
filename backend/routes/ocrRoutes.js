const express = require("express");
const router = express.Router();

const Bed = require("../models/Bed");
const { updateOCR, getOCR } = require("../controllers/ocrController");


// ✅ GET LIVE OCR DATA
router.get("/ocr", getOCR);


// ✅ RECEIVE OCR FROM PYTHON
router.post("/ocr", async (req, res) => {
  try {

    const { bedId, streamUrl, ocr } = req.body;

    let bed = await Bed.findOne({
      bedNumber: bedId,
    });

    // ✅ AUTO CREATE BED IF NOT EXISTS
    if (!bed) {

      bed = await Bed.create({
        bedNumber: bedId,
        patientName: `Patient ${bedId}`,
        hospital: "City Hospital",
        streamUrl:
          streamUrl || "",
        status: "monitoring",
        cameraStatus: "online",
      });

      console.log("✅ Auto-created bed:", bedId);
    }

    // ✅ STORE ONLY IN MEMORY
    req.body.bedId = bedId;

    updateOCR(req, res);

  } catch (err) {
    console.log(err);
    res.status(500).json({
      msg: err.message,
    });
  }
});

module.exports = router;

// const express = require("express");
// const router = express.Router();
// const Bed = require("../models/Bed");

// // 🔥 OCR UPDATE ROUTE
// router.post("/", async (req, res) => {
//   try {
//     const { bedNumber, streamUrl, ocr } = req.body;

//     let bed = await Bed.findOne({ bedNumber });

//     // 🔥 AUTO CREATE IF NOT EXISTS
//     if (!bed) {
//       bed = await Bed.create({
//         bedNumber,
//         patientName: "Unknown",
//         streamUrl,
//         hospital: "Auto Hospital",
//         cameraStatus: "online",
//       });

//       console.log("✅ Bed auto-created:", bedNumber);
//     }

//     // 🔥 UPDATE OCR DATA
//     bed.ocr = {
//       ...bed.ocr,
//       ...ocr,
//       updatedAt: new Date(),
//     };

//     await bed.save();

//     res.json({ msg: "OCR updated" });
//   } catch (err) {
//     res.status(500).json({ msg: err.message });
//   }
// });

// module.exports = router;

// const express = require("express");
// const router = express.Router();

// const { updateOCR, getOCR } = require("../controllers/ocrController");

// router.post("/ocr", updateOCR); // Python sends
// router.get("/ocr", getOCR);     // React fetches

// module.exports = router;