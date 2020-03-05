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
		}
	}
`
