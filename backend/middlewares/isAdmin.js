module.exports = (req, res, next) => {
  try {
    if (!req.user || req.user.role !== "admin") {
      return res.status(403).json({ msg: "Admin only access" });
    }

    next();
  } catch (err) {
    res.status(500).json({ msg: "Server error" });
  }
};