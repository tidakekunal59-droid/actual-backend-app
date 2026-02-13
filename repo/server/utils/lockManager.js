const mongoose = require('mongoose');

const lockSchema = new mongoose.Schema({
  resource: { type: String, required: true, unique: true },
  holder: { type: String, required: true },
  createdAt: { type: Date, default: Date.now, expires: 60 }
});

const Lock = mongoose.model('Lock', lockSchema);

module.exports = {
  acquireLock: async (resource, holder) => {
    try {
      await Lock.create({ resource, holder });
      return true;
    } catch (err) {
      if (err.code === 11000) return false;
      throw err;
    }
  },

  releaseLock: async (resource, holder) => {
    await Lock.deleteOne({ resource, holder });
  }
};
