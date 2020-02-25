import AWS from 'aws-sdk'
import {JobIngestion} from '../models'
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
    uploadFile: async (_, { clientId, sourceId, dataStartDate, dataEndDate, fileName, base64 }, {user}) => {
      const base64Data = new Buffer.from(
        base64.replace(
          /^data:application\/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,/,
          ''
        ),
        'base64'
      )
      try {
        const job = await JobIngestion.query().insert({
          advitoUserId: user.id,
          clientId,
          advitoApplicationTemplateSourceId: sourceId === 0 ? null : sourceId,
          dataStartDate,
          dataEndDate,
          originalFileName: fileName
        })
        const params = {
          Bucket: S3,
          Key: `${S3_KEY}/${job.id}_${Date.now()}_${fileName}`,
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
