const express = require("express");
const router = express.Router();

const Bed = require("../models/Bed");
const auth = require("../middlewares/authMiddleware");
const isAdmin = require("../middlewares/isAdmin");

// ✅ GET BEDS (WITH HOSPITAL FILTER)
router.get("/", auth, async (req, res) => {
  try {
    const { hospital } = req.query;

    let filter = {};

    if (hospital && hospital.trim() !== "") {
      filter.hospital = hospital.trim();
    }

    const beds = await Bed.find(filter);

    console.log("FETCH BEDS:", beds); // DEBUG

    res.json(beds);
  } catch (err) {
    res.status(500).json({ msg: err.message });
  }
});

// ✅ ADD BED (ADMIN ONLY)
router.post("/", auth, isAdmin, async (req, res) => {
  try {
    let { bedNumber, patientName, streamUrl, hospital } = req.body;

    if (!hospital || hospital.trim() === "") {
      return res.status(400).json({ msg: "Hospital is required" });
    }

    hospital = hospital.trim();

    const exists = await Bed.findOne({
      bedNumber,
      hospital,
    });

    if (exists) {
      return res
        .status(400)
        .json({ msg: "Bed already exists in this hospital" });
    }

    const bed = await Bed.create({
      bedNumber: Number(bedNumber),
      patientName,
      streamUrl,
      hospital,
      cameraStatus: "online",
    });

    console.log("BED SAVED:", bed); // DEBUG

    res.json(bed);
  } catch (err) {
    console.log(err);
    res.status(500).json({ msg: err.message });
  }
});

// ✅ DELETE BED
router.delete("/:id", auth, isAdmin, async (req, res) => {
  try {
    await Bed.findByIdAndDelete(req.params.id);
    res.json({ msg: "Bed removed" });
  } catch (err) {
    res.status(500).json({ msg: err.message });
  }
});

module.exports = router;

// const express = require("express");
// const router = express.Router();
// const Bed = require("../models/Bed");
// const auth = require("../middleware/authMiddleware");
// const isAdmin = require("../middleware/isAdmin");

// // 🔥 GET ALL BEDS
// router.get("/", auth, async (req, res) => {
//   const beds = await Bed.find();
//   res.json(beds);
// });

// // 🔥 ADD BED (ADMIN ONLY)
// router.post("/", auth, isAdmin, async (req, res) => {
//   try {
//     const { bedNumber, patientName, streamUrl } = req.body;

//     const exists = await Bed.findOne({ bedNumber });
//     if (exists) {
//       return res.status(400).json({ msg: "Bed already exists" });
//     }

//     const bed = await Bed.create({
//       bedNumber,
//       patientName,
//       streamUrl,
//       hospital: "Default Hospital",
//       cameraStatus: "online",
//     });

//     res.json(bed);
//   } catch (err) {
//     res.status(500).json({ msg: err.message });
//   }
// });

// // 🔥 DELETE BED (ADMIN ONLY)
// router.delete("/:id", auth, isAdmin, async (req, res) => {
//   await Bed.findByIdAndDelete(req.params.id);
//   res.json({ msg: "Bed removed" });
// });

// module.exports = router;

// // const express = require("express");
// // const router = express.Router();

// // const {
// //   getBeds,
// //   getBedById,
// //   updateOCR,
// // } = require("../controllers/bedController");

// // const protect = require("../middlewares/authMiddleware");

// // router.post("/ocr", updateOCR);
// // router.get("/", protect, getBeds);
// // router.get("/:id", protect, getBedById);

// // module.exports = router;