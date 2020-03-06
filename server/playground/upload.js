export default {
	Query: {
		name: 'Job Queries',
		endpoint: '',
		headers: { sessiontoken: 'MY^PR3TTYP0NY' },
		query: `
     {
      getJob(jobId: null) {
        id
        originalFileName
        jobName
        countRows
        isComplete
        jobStatus
        jobNote
        timestamp
      }
    }`
	}
}
