const mongoose = require("mongoose");

const bedSchema = new mongoose.Schema({
  bedNumber: {
    type: Number,
    required: true,
    unique: true, // 🔥 prevents duplicates
  },

  patientName: {
    type: String,
    default: "Unknown",
  },

  status: {
    type: String,
    enum: ["critical", "monitoring", "stable"],
    default: "monitoring",
  },

  cameraStatus: {
    type: String,
    enum: ["online", "offline"],
    default: "offline",
  },

  streamUrl: {
    type: String,
    default: "",
  },

  hospital: {
    type: String,
    required: true,
  },

  ocr: {
    heartRate: Number,
    bp: String,
    spo2: Number,
    temp: Number,
    respiratoryRate: Number,
    updatedAt: Date,
  },
});

module.exports = mongoose.model("Bed", bedSchema);


// const mongoose = require("mongoose");

// const bedSchema = new mongoose.Schema({
//   bedNumber: Number,
//   hospitalId: {
//     type: mongoose.Schema.Types.ObjectId,
//     ref: "Hospital",
//   },
//   patientName: String,

//   status: {
//     type: String,
//     enum: ["critical", "monitoring", "stable"],
//     default: "monitoring",
//   },

//   cameraStatus: {
//     type: String,
//     enum: ["online", "offline"],
//     default: "offline",
//   },

//   streamUrl: String,

//   ocr: {
//     heartRate: Number,
//     bp: String,
//     spo2: Number,
//     temp: Number,
//     respiratoryRate: Number,
//     updatedAt: Date,
//   },
//   hospital: {
//     type: String,
//     required: true,
//   }
// });

// module.exports = mongoose.model("Bed", bedSchema);