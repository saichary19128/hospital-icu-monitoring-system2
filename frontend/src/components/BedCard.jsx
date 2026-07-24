import { useNavigate } from "react-router-dom";

const BedCard = ({ bed, ocr }) => {

  const navigate = useNavigate();

  const getStatusColor = () => {
    if (bed.status === "critical") return "#ef4444";
    if (bed.status === "stable") return "#22c55e";
    return "#f59e0b";
  };

  return (
    <div
      onClick={() => navigate(`/stream/${bed._id}`)}
      style={styles.card}
    >

      {/* HEADER */}
      <div style={styles.header}>
        <h3 style={styles.bed}>
          Bed {bed.bedNumber}
        </h3>

        <div style={styles.connectionWrapper}>
          <div
            style={
              bed.cameraStatus === "online"
                ? styles.onlinePulse
                : styles.offlineDot
            }
          />
        </div>
      </div>

      {/* PATIENT */}
      <p style={styles.patient}>
        {bed.patientName}
      </p>

      {/* STATUS */}
      <p
        style={{
          ...styles.status,
          color: getStatusColor(),
        }}
      >
        ● {bed.status.toUpperCase()}
      </p>

      {/* LIVE VITALS */}

      <div style={styles.vitals}>

        <div style={styles.vitalBox}>
          <span style={styles.label}>HR</span>
          <span style={styles.value}>
            {ocr?.HR || "--"}
          </span>
        </div>

        <div style={styles.vitalBox}>
          <span style={styles.label}>BP</span>
          <span style={styles.value}>
            {ocr?.BP || "--"}
          </span>
        </div>

        <div style={styles.vitalBox}>
          <span style={styles.label}>SPO2</span>
          <span style={styles.value}>
            {ocr?.SPO2 || ocr?.SP02 || "--"}%
          </span>
        </div>

      </div>

      <div style={styles.footer}>

        <span>
          Camera{" "}
          <b
            style={{
              color:
                bed.cameraStatus === "online"
                  ? "#22c55e"
                  : "#ef4444",
            }}
          >
            {bed.cameraStatus}
          </b>
        </span>

        {bed.cameraStatus === "online" && (
          <span style={styles.live}>
            ● LIVE
          </span>
        )}

      </div>

    </div>
  );
};

const styles = {

  card: {
    width: "300px",
    height: "220px",
    padding: "15px",
    borderRadius: "12px",
    cursor: "pointer",
    background:
      "linear-gradient(145deg,#020617,#0f172a)",
    color: "#e2e8f0",
    boxShadow:
      "0 10px 25px rgba(0,0,0,.6)",
    border:
      "1px solid rgba(255,255,255,.08)",
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },

  bed: {
    margin: 0,
  },

  patient: {
    margin: "8px 0",
    color: "#cbd5e1",
  },

  status: {
    fontWeight: "bold",
    fontSize: "13px",
  },

  vitals: {
    display: "flex",
    justifyContent: "space-between",
    marginTop: "20px",
  },

  vitalBox: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },

  label: {
    color: "#94a3b8",
    fontSize: "14px",
  },

  value: {
    color: "#22c55e",
    fontWeight: "bold",
    fontSize: "18px",
  },

  footer: {
    marginTop: "20px",
    display: "flex",
    justifyContent: "space-between",
    fontSize: "13px",
  },

  live: {
    color: "#22c55e",
    fontWeight: "bold",
  },

  connectionWrapper: {
    display: "flex",
    alignItems: "center",
  },

  onlinePulse: {
    width: "10px",
    height: "10px",
    borderRadius: "50%",
    background: "#22c55e",
    boxShadow: "0 0 10px #22c55e",
  },

  offlineDot: {
    width: "10px",
    height: "10px",
    borderRadius: "50%",
    background: "#ef4444",
  },

};

export default BedCard;

// import { useNavigate } from "react-router-dom";

// const BedCard = ({ bed, ocr }) => {
//   const navigate = useNavigate();

//   const getStyle = () => {
//     if (bed.status === "critical") {
//       return { border: "2px solid #ef4444", background: "#fee2e2" };
//     }
//     if (bed.status === "stable") {
//       return { border: "2px solid #22c55e", background: "#dcfce7" };
//     }
//     return { border: "2px solid #f59e0b", background: "#fef3c7" };
//   };

//   const getStatusColor = () => {
//     if (bed.status === "critical") return "#ef4444";
//     if (bed.status === "stable") return "#22c55e";
//     return "#f59e0b";
//   };

//   return (
//     <div
//       onClick={() => navigate(`/stream/${bed._id}`)}
//       style={{
//         padding: "16px",
//         borderRadius: "12px",
//         width: "230px",
//         cursor: "pointer",
//         color: "#111",
//         boxShadow: "0 4px 15px rgba(0,0,0,0.15)",
//         transition: "0.2s",
//         ...getStyle(),
//       }}
//       onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.03)")}
//       onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
//     >
//       {/* 🔥 HEADER */}
//       <div style={styles.header}>
//         <h3 style={{ margin: 0 }}>Bed {bed.bedNumber}</h3>

//         {/* CONNECTION ICON */}
//         <div style={styles.connection}>
//           {bed.cameraStatus === "online" ? (
//             <div style={styles.onlineDot}></div>
//           ) : (
//             <div style={styles.offlineDot}></div>
//           )}
//         </div>
//       </div>

//       {/* PATIENT */}
//       <p style={styles.patient}>{bed.patientName}</p>

//       {/* STATUS */}
//       <p style={{ color: getStatusColor(), fontWeight: "bold" }}>
//         ● {bed.status.toUpperCase()}
//       </p>

//       {/* 🔥 OCR DATA */}
//       <div style={styles.vitals}>
//         <p>❤️ HR: {ocr?.heartRate ?? "--"} bpm</p>
//         <p>🩸 BP: {ocr?.bp ?? "--"}</p>
//         <p>🫁 SPO2: {ocr?.spo2 ?? "--"}%</p>
//       </div>

//       {/* CAMERA STATUS */}
//       <p style={styles.camera}>
//         Camera:{" "}
//         <span
//           style={{
//             color: bed.cameraStatus === "online" ? "#22c55e" : "#ef4444",
//             fontWeight: "bold",
//           }}
//         >
//           {bed.cameraStatus.toUpperCase()}
//         </span>
//       </p>

//       {/* LIVE INDICATOR */}
//       {bed.cameraStatus === "online" && (
//         <p style={styles.live}>● LIVE</p>
//       )}
//     </div>
//   );
// };

// const styles = {
//   header: {
//     display: "flex",
//     justifyContent: "space-between",
//     alignItems: "center",
//   },

//   patient: {
//     margin: "6px 0",
//     fontWeight: "600",
//   },

//   vitals: {
//     fontSize: "16px",
//     marginTop: "6px",
//     lineHeight: "1.4",
//   },

//   camera: {
//     marginTop: "8px",
//     fontSize: "14px",
//   },

//   live: {
//     color: "#22c55e",
//     fontWeight: "bold",
//     marginTop: "6px",
//   },

//   connection: {
//     display: "flex",
//     alignItems: "center",
//   },

//   onlineDot: {
//     width: "10px",
//     height: "10px",
//     borderRadius: "50%",
//     background: "#22c55e",
//     boxShadow: "0 0 8px #22c55e",
//   },

//   offlineDot: {
//     width: "10px",
//     height: "10px",
//     borderRadius: "50%",
//     background: "#ef4444",
//   },
// };

// export default BedCard;

// import { useNavigate } from "react-router-dom";


// const BedCard = ({ bed, ocr }) => {
//   const navigate = useNavigate();

//   const getStyle = () => {
//     if (bed.status === "critical") {
//       return { border: "2px solid red", background: "#cd7777" };
//     }
//     if (bed.status === "stable") {
//       return { border: "2px solid green", background: "#e6f9ec" };
//     }
//     return { border: "2px solid orange", background: "#fff7e6" };
//   };

//   console.log("BED OCR:", bed.bedNumber, ocr); // 🔍 DEBUG

//   return (
//     <div
//       onClick={() => navigate(`/stream/${bed._id}`)}
//       style={{
//         padding: "14px",
//         borderRadius: "10px",
//         width: "220px",
//         cursor: "pointer",
//         color: "black",
//         ...getStyle(),
//       }}
//     >
//       {/* HEADER */}
//       <div style={{ display: "flex", justifyContent: "space-between" }}>
//         <h3>Bed {bed.bedNumber}</h3>
//         <span>{bed.cameraStatus === "online" ? "📶" : "❌"}</span>
//       </div>

//       <p><b>{bed.patientName}</b></p>

//       <p>
//         {bed.status === "critical" && "🔴 Critical"}
//         {bed.status === "stable" && "🟢 Stable"}
//         {bed.status === "monitoring" && "🟡 Monitoring"}
//       </p>

//       {/* 🔥 OCR DATA DISPLAY */}
//       <p>❤️(HR): {ocr?.heartRate ?? "--"} bpm</p>
//       <p>🩸(BP): {ocr?.bp ?? "--"}</p>
//       <p>🫁(SPO2): {ocr?.spo2 ?? "--"}%</p>
//       {/* <p>🌬️(RR): {ocr?.respiratoryRate ?? "--"}</p> */}

//       <p>Camera: {bed.cameraStatus}</p>

//       {bed.cameraStatus === "online" && (
//         <p style={{ color: "green", fontWeight: "bold" }}>● LIVE</p>
//       )}
//     </div>
//   );
// };

// export default BedCard;