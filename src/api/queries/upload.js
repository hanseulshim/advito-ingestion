import gql from 'graphql-tag'

export const GET_JOB = gql`
	query getJob($jobId: Int!) {
		getJob(jobId: $jobId) {
			id
			originalFileName
			jobName
			countRows
			isComplete
			jobStatus
			jobNote
			timestamp
			processingStartTimestamp
			templateName
			applicationName
		}
	}
`

export const GET_PRESIGNED_UPLOAD_URL = gql`
	query getPresignedUploadUrl($fileName: String!) {
		getPresignedUploadUrl(fileName: $fileName) {
			key
			url
		}
	}
`
