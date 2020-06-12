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

const ErrorCount = styled.div`
	font-weight: bold;
	font-size: 1.3em;
`

const Title = styled.div`
	font-weight: 400;
	text-decoration: underline;
`

const Section = styled.div`
	margin: 10px 0;
`

const getSectionText = (key, text) => {
	if (key === 'unmaskedCreditCardData') {
		return <Title>The file contains unmasked credit card data ({text})</Title>
	}
	if (key === 'sourceCurrencyCode') {
		return (
			<Title>The file does not contain source currency code ({text})</Title>
		)
	}
	if (key === 'incorrectCharacters') {
		return (
			<Title>
				The file contains non-english characters, only the following special
				characters are allowed:`&$(),: ({text})
			</Title>
		)
	}
	if (key === 'incorrectDates') {
		return (
			<Title>
				The file contains an incorrect date format, dates should be DD-MMM-YYYY
				({text})
			</Title>
		)
	}
	if (key === 'stateShouldBeBlank') {
		return <Title>The State value should be blank ({text})</Title>
	}
	if (key === 'stateMissing') {
		return <Title>The State value is missing ({text})</Title>
	}
	if (key === 'stateInvalid') {
		return <Title>Invalid two letter State Code ({text})</Title>
	}
}

const getSectionHeader = (key, count) => {
	if (key === 'unmaskedCreditCardData') {
		return <Title key={key}>Unmasked credit card data ({count} errors)</Title>
	}
	if (key === 'sourceCurrencyCode') {
		return <Title key={key}>No source currency code ({count} errors)</Title>
	}
	if (key === 'incorrectCharacters') {
		return (
			<Title key={key}>
				Non-English or unallowed character used ({count} errors)
			</Title>
		)
	}
	if (key === 'incorrectDates') {
		return <Title key={key}>Incorrect date format ({count} errors)</Title>
	}
	if (key === 'stateShouldBeBlank') {
		return (
			<Title key={key}>
				Incorrect State value, State should be blank ({count} errors)
			</Title>
		)
	}
	if (key === 'stateMissing') {
		return (
			<Title key={key}>
				Incorrect State value, State is missing ({count} errors)
			</Title>
		)
	}
	if (key === 'stateInvalid') {
		return (
			<Title key={key}>
				Incorrect State value, State code is invalid ({count} errors)
			</Title>
		)
	}
}

const JobProgress = ({ setJobId, jobId, setMessage, MessageHeading }) => {
	const { loading, error, data, stopPolling } = useQuery(GET_JOB, {
		variables: { jobId },
		skip: !jobId,
		pollInterval: 3000,
		fetchPolicy: 'network-only'
	})
	if (loading) return <SpinLoader />
	if (error) return <ErrorMessage error={error} />
	const {
		originalFileName,
		jobName,
		countRows,
		isComplete,
		jobStatus,
		jobNote,
		processingStartTimestamp,
		templateName,
		applicationName
	} = data.getJob
	if (isComplete) {
		stopPolling()
		if (jobStatus === 'done' || jobStatus === 'ingested') {
			//send success
			setMessage({
				message: (
					<MessageHeading>
						Your {originalFileName} has been successfully uploaded! <br /> It
						contained {countRows} rows and has the job name {jobName}
					</MessageHeading>
				),
				type: 'success'
			})
		} else if (jobStatus === 'error') {
			const json = JSON.parse(jobNote)
			const errorCount = Object.values(json).reduce(
				(prev, curr) => prev + curr.length,
				0
			)
			const displayArray = []
			for (let [key, value] of Object.entries(json)) {
				const count = value.length
				if (count === 1) {
					displayArray.push(
						<Section key={key}>{getSectionText(key, value[0])}</Section>
					)
				} else if (count > 1) {
					displayArray.push(getSectionHeader(key, count))
					displayArray.push(
						...value.map((msg, index) => {
							if (index > 9) {
								return ''
							}
							return (
								<div key={Math.random()}>
									- {index === 9 ? `${msg}...` : msg}
								</div>
							)
						})
					)
				}
			}
			const emailArray = []
			for (let [key, value] of Object.entries(json)) {
				const count = value.length
				const formatKey = (key, count) => {
					if (key === 'unmaskedCreditCardData') {
						return `Unmasked credit card data (${count} errors)`
					}
					if (key === 'sourceCurrencyCode') {
						return `No source currency code (${count} errors)`
					}
					if (key === 'incorrectCharacters') {
						return `Non-English or unallowed character used (${count} errors)`
					}
					if (key === 'incorrectDates') {
						return `Incorrect date format (${count} errors)`
					}
					if (key === 'stateShouldBeBlank') {
						return `Incorrect State value, State should be blank (${count} errors)`
					}
					if (key === 'stateMissing') {
						return `Incorrect State value, State is missing (${count} errors)`
					}
					if (key === 'stateInvalid') {
						return `Incorrect State value, State code is invalid (${count} errors)`
					}
				}
				const formattedKey = formatKey(key, count)

				if (count > 0) {
					emailArray.push(
						` %0D%0A ${formattedKey} : ${[
							value.map((v) => v.replace(',', ' ')).join(', ')
						]}` + `%0D%0A`
					)
				}
			}

			const getMailTo = () => {
				const user = JSON.parse(localStorage.getItem('advito-user')).displayName

				return `mailto:AdvitoServices@bcdtravel.eu?subject= Advito I%26A Ingestion Console Assistance Request
				&body=Please provide a detailed description of your need so that we can provide prompt assistance.%0D%0A
				%0D%0A
				Username: ${user}
				%0D%0A
				Filename: ${originalFileName}
				%0D%0A
				Practice Area Selection: ${applicationName}
				%0D%0A
				Template: ${templateName}
				%0D%0A
				Date/time of ingestion attempt: ${new Date(+processingStartTimestamp)}
				%0D%0A
				Error generated: %0D%0A
				  ${emailArray.join('')}
				`
			}
			setMessage({
				message: (
					<>
						<ErrorCount>{errorCount} Errors found</ErrorCount>
						<MessageHeading>
							Your file will not be ingested due the follow errors:
						</MessageHeading>
						{displayArray}
						<br />
						<MessageHeading>
							Please resolve the errors and try uploading again.
						</MessageHeading>
						<div>
							Tried everything and still getting errors?{' '}
							<a href={getMailTo()}>Contact I&amp;A</a> within 5 days of upload
							for assistance.
						</div>
					</>
				),
				type: 'error'
			})
		} else {
			const getMailTo = () => {
				const user = JSON.parse(localStorage.getItem('advito-user')).displayName

				return `mailto:AdvitoServices@bcdtravel.eu?subject= Advito I%26A Ingestion Console Assistance Request
				&body=Please provide a detailed description of your need so that we can provide prompt assistance.%0D%0A
				%0D%0A
				Username: ${user}
				%0D%0A
				Filename: ${originalFileName}
				%0D%0A
				Practice Area Selection: ${applicationName}
				%0D%0A
				Template: ${templateName}
				%0D%0A
				Date/time of ingestion attempt: ${new Date(+processingStartTimestamp)}
				%0D%0A

				`
			}

			setMessage({
				message: (
					<>
						<ErrorCount>There was a server error.</ErrorCount>
						<MessageHeading>{jobNote}</MessageHeading>
						<div>
							Tried everything and still getting errors?{' '}
							<a href={getMailTo()}>Contact I&amp;A</a> within 5 days of upload
							for assistance.
						</div>
					</>
				),
				type: 'error'
			})
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
