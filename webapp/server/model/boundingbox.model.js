var mongoose = require('mongoose')
var Schema = mongoose.Schema

// create a schema
var boundingBoxSchema = new Schema({
  image: { type: Schema.Types.ObjectId, ref: 'Image' },
  location_x: Number,
  location_y: Number,
  width: Number,
  height: Number,
  label: { type: String, enum: [] },
  created_at: Date,
  updated_at: Date
})

var BoundingBox = mongoose.model('BoundingBox', boundingBoxSchema)

module.exports = BoundingBox
