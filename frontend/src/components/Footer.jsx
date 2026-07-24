const Footer = () => {
  return (
    <div
      style={{
        padding: "12px",
        background: "#0e0d0d",
        borderTop: "1px solid #6c5656",
        textAlign: "center",
        fontSize: "14px",
        color: "#3e3838",
      }}
    >
      <div style={{ color: 'white' }}>
        Hospital ICU Monitoring System ©{new Date().getFullYear()}
        <p> All Rights Reserved by MedDev Team.</p>
      </div>
    </div>
  );
};

export default Footer;