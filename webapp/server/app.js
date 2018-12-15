const express = require('express')
const mongoose = require('mongoose')
const morgan = require('morgan')
const _ = require('lodash')

var model = require('./model')

const app = express()
const port = 3000

try {
  mongoose.connect(
    'mongodb://localhost:27017/imageLabeler',
    { useNewUrlParser: true }
  )

  app.use(morgan('short'))
  app.get('/', (req, res) => res.send('Hello World!'))

  app.get('/api/images/:imageName?', async (req, res) => {
    const { imageName } = req.params
    if (_.isEmpty(imageName)) {
      const imageList = await model.Images.find({}).select('image_names')
      res.send({ status: 'success', data: imageList })
    }

    const image = await model.Images.findOne({ image_names: imageName })
    res.download(_.get(image, 'location', `${__dirname}/images/404.png`))
  })
  app.listen(port, () => console.log(`Example app listening on port ${port}!`))
} catch (error) {
  console.log('AAAAAAAA', error)
  process.exit(1)
}
