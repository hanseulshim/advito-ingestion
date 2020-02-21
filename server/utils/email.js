import AWS from 'aws-sdk'
import { EMAIL_SENDER, EMAIL_BCC } from '../constants'
import { EmailTemplate } from '../models'
const ses = new AWS.SES({
  accessKeyId: process.env.ACCESS_KEY_ID,
  secretAccessKey: process.env.SECRET_ACCESS_KEY,
  region: process.env.REGION
})

export const sendEmail = async (
  templateName,
  recipient,
  placeholders,
  applicationId,
  advitoDb
) => {
  const { emailSubject, emailBody } = await EmailTemplate.query(advitoDb)
    .where('templateName', templateName)
    .where('advitoApplicationId', applicationId)
    .first()
  let message = emailBody
  Object.keys(placeholders).forEach(key => {
    const regex = new RegExp(String.raw`\[\[${key}]]`, 'g')
    message = message.replace(regex, placeholders[key])
  })
  const params = {
    Source: EMAIL_SENDER,
    Destination: {
      ToAddresses: [recipient],
      BccAddresses: EMAIL_BCC
    },
    Message: {
      Body: {
        Html: {
          Charset: 'UTF-8',
          Data: message
        }
      },
      Subject: {
        Charset: 'UTF-8',
        Data: emailSubject
      }
    }
  }

  await ses.sendEmail(params).promise()
}
