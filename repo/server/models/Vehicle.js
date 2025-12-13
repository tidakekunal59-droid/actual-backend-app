const mongoose = require('mongoose');

const vehicleSchema = new mongoose.Schema({
  licensePlate: { type: String, required: true, unique: true },
  model: { type: String, required: true },
  status: { type: String, enum: ['active', 'maintenance', 'retired'], default: 'active' },
  // ... other fields
}, { timestamps: true });

module.exports = mongoose.model('Vehicle', vehicleSchema);
