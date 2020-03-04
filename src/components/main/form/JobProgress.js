import React from 'react'
import styled from 'styled-components'
import { useQuery } from '@apollo/client'
import { SpinLoader } from 'components/common/Loader'
import ErrorMessage from 'components/common/ErrorMessage'
import { Progress } from 'antd'
import { GET_JOB } from 'api/queries'

const Container = styled.div`
	display: flex;
	justify-content: center;
	align-items: center;
`

const JobProgress = ({
	setJobId,
	jobId,
	setSuccessMessage,
	setError,
	MessageHeading
}) => {
	const { loading, error, data, stopPolling } = useQuery(GET_JOB, {
		variables: { jobId },
		skip: !jobId,
		pollInterval: 5000,
		fetchPolicy: 'network-only'
	})
	if (loading) return <SpinLoader />
	if (error) return <ErrorMessage error={error} />
	const {
		originalFileName,
		jobName,
		countRows,
		jobStatus,
		isComplete,
		jobNote
	} = data.getJob
	if (isComplete) {
		stopPolling()
		if (jobStatus === 'done') {
			//send success
			setSuccessMessage(
				<MessageHeading>
					Your {originalFileName} has been succesfully uploaded! <br /> It
					contained {countRows} and has the job name {jobName}
				</MessageHeading>
			)
		} else if (jobStatus === 'error') {
			//send error
		}
		setJobId(null)
	}
	return (
		<Container>
			{jobStatus === 'running' && (
				<Progress type="circle" percent={jobNote ? jobNote : 0} />
			)}
		</Container>
	)
}

export default JobProgress
