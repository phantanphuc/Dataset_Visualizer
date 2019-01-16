const express = require('express')
const mongoose = require('mongoose')
const morgan = require('morgan')
const bodyParser = require('body-parser')
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
  app.use(bodyParser.json())

  app.get('/', (req, res) => res.send('Hello World!'))

  app.get('/api/images/:imageName?', async (req, res) => {
    const { imageName } = req.params
    if (_.isEmpty(imageName)) {
      const imageList = await model.Images.find({}).select('image_names')
      return res.send({ status: 'success', data: imageList })
    }

    const image = await model.Images.findOne({ image_names: imageName })
    console.log(`${__dirname}/images/404.png`)
    return res.download(_.get(image, 'location', `${__dirname}/images/404.png`))
  })

  app.post('/api/images/save', async (req, res) => {
    console.log(req.body)
    // const { imageName, boundingBox } = req.body
    for (const data in req.body) {
      console.log('vo')
      console.log(data)
      console.log(req.body[data])
      const { imageName, boundingBox } = req.body[data]

      let imageData = await model.Images.findOne({ image_names: imageName })

      if (!imageData) {
        return res.send({ status: 'image not found' })
      }

      for (const box in boundingBox) {
        const boxData = boundingBox[box]
        const savedBox = await model.BoundingBox.create({
          image: imageData,
          location_x: boxData.x,
          location_y: boxData.y,
          width: boxData.width,
          height: boxData.height,
          label: boxData.label
        })
        imageData.boundingBox.push(savedBox._id)
      }

      await imageData.save()
      console.log('done')
    }
    // let imageData = await model.Images.findOne({ image_names: imageName })

    // if (!imageData) {
    //   return res.send({ status: 'image not found' })
    // }

    // for (const box in boundingBox) {
    //   const boxData = await model.BoundingBox.create({
    //     image: imageData,
    //     location_x: box.x,
    //     location_y: box.y,
    //     width: box.width,
    //     height: box.height,
    //     label: box.label
    //   })

    //   imageData.boundingBox.push(boxData._id)
    // }

    // await imageData.save()

    res.send({ status: 'success' })
  })

  // app.get('/api/labels',async (req,res){

  // })

  app.listen(port, () => console.log(`Example app listening on port ${port}!`))
} catch (error) {
  console.log('AAAAAAAA', error)
  process.exit(1)
}
