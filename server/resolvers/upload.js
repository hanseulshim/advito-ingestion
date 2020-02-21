import AWS from 'aws-sdk'
const {
  AWS_ACCESS_KEY_ID,
  AWS_SECRET_ACCESS_KEY,
  AWS_S3,
  AWS_S3_KEY
} = process.env
const s3 = new AWS.S3({
  accessKeyId: AWS_ACCESS_KEY_ID,
  secretAccessKey: AWS_SECRET_ACCESS_KEY
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
          Bucket: AWS_S3,
          Key: `${AWS_S3_KEY}/${fileName}`,
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
