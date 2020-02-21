import AWS from 'aws-sdk'
const {
  ACCESS_KEY_ID,
  SECRET_ACCESS_KEY,
  S3,
  S3_KEY
} = process.env
const s3 = new AWS.S3({
  accessKeyId: ACCESS_KEY_ID,
  secretAccessKey: SECRET_ACCESS_KEY
})

export default {
  Mutation: {
    uploadFile: async (_, { fileName, base64 }) => {
      const base64Data = new Buffer.from(
        base64.replace(
          /^data:application\/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,/,
          ''
        ),
        'base64'
      )
      try {
        const params = {
          Bucket: S3,
          Key: `${S3_KEY}/${fileName}`,
          Body: base64Data,
          ContentEncoding: 'base64'
        }
        await s3.upload(params).promise()
        return true
      } catch (err) {
        console.log(err);
        throw err
      }
    }
  }
}
