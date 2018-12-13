var mongoose = require("mongoose");
var Schema = mongoose.Schema;

// create a schema
var imageSchema = new Schema({
  image_names: String,
  location: String,
  boundingBox: [{ type: Schema.Types.ObjectId, ref: "BoundingBox" }],
  created_at: Date,
  updated_at: Date
});

var Images = mongoose.model("Image", imageSchema);

module.exports = Images;
