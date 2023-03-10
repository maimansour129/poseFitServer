const mongoose = require("mongoose");
const Joi = require("joi");

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
  },
  password: {
    type: String,
    required: true,
    minlength: 8,
  },
  name: {
    type: String,
    required: true,
    minlength: 2,
    maxlenght: 1024,
  },
  targetWeight: {
    type: Number,
    required: true,
  },
  // activityProgress: {
  //    type: String,
  //    required: true,
  // },
  age: {
    type: Number,
    required: true,
  },
  height: {
    type: Number,
    required: true,
  },
  weight: {
    type: Number,
    required: true,
  },
  plan: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "plan",
    required: true,
  },
});

function validateUser(user) {
  const schema = Joi.object({
    email: Joi.string().email(),
    password: Joi.string().min(8),
    name: Joi.string().min(2).max(1024),
    targetWeight: Joi.number().min(0),
    age: Joi.number().min(0),
    weight: Joi.number().min(0),
    height: Joi.number().min(0),
    plan:Joi.string().min(0)
  });

  return schema.validate(user);
}

const user = mongoose.model("User", userSchema);
module.exports = [user, validateUser];
