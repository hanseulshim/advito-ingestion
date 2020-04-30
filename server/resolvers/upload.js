import AWS from 'aws-sdk'
import { JobIngestion, AdvitoApplicationTemplateSource } from '../models'
import axios from 'axios'
const {
	ACCESS_KEY_ID,
	SECRET_ACCESS_KEY,
	BUCKET_ORIGIN,
	KEY,
	BUCKET_DEST
} = process.env
AWS.config.update({
	accessKeyId: ACCESS_KEY_ID,
	secretAccessKey: SECRET_ACCESS_KEY
})
const s3 = new AWS.S3()

export default {
	Query: {
		getJob: async (_, { jobId }) => {
			const job = await JobIngestion.query()
				.select('j.*', 't.templateName', 'a.applicationName')
				.findById(jobId)
				.alias('j')
				.leftJoin(
					'advitoApplicationTemplateSource as s',
					'j.advitoApplicationTemplateSourceId',
					's.id'
				)
				.leftJoin(
					'advitoApplicationTemplate as t',
					's.advitoApplicationTemplateId',
					't.id'
				)
				.leftJoin('advitoApplication as a', 't.advitoApplicationId', 'a.id')
			return { ...job, timestamp: new Date().getTime() }
		}
	},
	Mutation: {
		uploadFile: async (
			_,
			{
				clientId,
				sourceId,
				advitoApplicationId,
				dataStartDate,
				dataEndDate,
				fileName,
				base64,
				fileSize
			},
			{ user }
		) => {
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
					advitoApplicationTemplateSourceId: sourceId,
					dataStartDate,
					dataEndDate,
					originalFileName: fileName,
					fileExtension: 'xlsx',
					fileSize,
					isComplete: false,
					jobStatus: 'running',
					processingStartTimestamp: new Date(),
					jobNote: 0
				})

				const truncFileName =
					fileName.length > 80 ? fileName.substring(0, 80) : fileName

				const key = KEY
					? `${KEY}/${job.id}_${Date.now()}_${truncFileName}`
					: `${job.id}_${Date.now()}_${truncFileName}`

				const uploadParams = {
					Bucket: BUCKET_ORIGIN,
					Key: key,
					Body: base64Data,
					ContentEncoding: 'base64'
				}

				await Promise.all([
					s3.upload(uploadParams).promise(),
					JobIngestion.query().findById(job.id).patch({
						fileName: key
					})
				])

				axios.post(
					process.env.ENVIRONMENT === 'PROD'
						? 'https://0rihemrgij.execute-api.us-east-2.amazonaws.com/prod/validation'
						: process.env.ENVIRONMENT === 'STAGING'
						? 'https://fynpwsijxl.execute-api.us-east-2.amazonaws.com/stage/validation'
						: 'https://cjsk604dw5.execute-api.us-east-2.amazonaws.com/dev/validation',
					{
						job_ingestion_id: job.id,
						bucket_origin: BUCKET_ORIGIN,
						bucket_dest: BUCKET_DEST,
						environment: process.env.ENVIRONMENT,
						advito_application_id: advitoApplicationId
					}
				)
				return job.id
			} catch (err) {
				console.log(err)
				throw err
			}
		}
	}
}
