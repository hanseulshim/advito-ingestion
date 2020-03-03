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

const JobProgress = ({ jobId, setSuccess, setError }) => {
	const { loading, error, data } = useQuery(GET_JOB, {
		variables: { jobId },
		skip: !jobId,
		pollInterval: 5000,
		fetchPolicy: 'network-only'
	})
	console.log(jobId)
	if (loading) return <SpinLoader />
	if (error) return <ErrorMessage error={error} />
	const { isComplete, jobStatus, jobNote } = data.getJob
	return (
		<Container>
			{jobStatus === 'running' && (
				<Progress type="circle" percent={jobNote ? jobNote : 0} />
			)}
		</Container>
	)
}

export default JobProgress
