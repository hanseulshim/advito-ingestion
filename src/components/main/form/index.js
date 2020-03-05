import React, { useState } from 'react'
import styled from 'styled-components'
import { Title } from 'components/common/Typography'
import { Alert, DatePicker } from 'antd'
import FileUpload from './FileUpload'
import SelectPractice from './SelectPractice'
import SelectClient from './SelectClient'
import SelectTemplate from './SelectTemplate'
import SelectSource from './SelectSource'
import JobProgress from './JobProgress'
const { RangePicker } = DatePicker

const Container = styled.div`
	width: 900px;
	padding-bottom: ${props => props.theme.verticalSpace};
`

const StyledTitle = styled(Title)`
	margin-bottom: ${props => props.theme.verticalSpace};
`

const Row = styled.div`
	display: flex;
	margin-bottom: ${props => props.theme.verticalSpace};
	justify-content: space-between;
`

const DateSelect = styled.div`
	display: flex;
	flex-direction: column;

	> span {
		text-transform: uppercase;
		margin-bottom: 2px;
		font-size: 0.85em;
	}
`

const Message = styled(Alert)`
	margin-top: 25px;
`

const MessageHeading = styled.div`
	font-weight: 400;
	font-size: 1.25em;
`

const Form = () => {
	const [inputs, setInputs] = useState({
		client: null,
		application: null,
		template: null,
		source: null,
		fileStartDate: null,
		fileEndDate: null
	})
	const [jobId, setJobId] = useState(null)
	const [successMessage, setSuccessMessage] = useState('')
	const [errorMessage, setErrorMessage] = useState('')

	const handleInputChange = (key, value) => {
		if (key === 'client') {
			setInputs(inputs => ({
				...inputs,
				[key]: value,
				application: null,
				template: null,
				source: null
			}))
			setErrorMessage('')
		} else if (key === 'application') {
			setInputs(inputs => ({
				...inputs,
				[key]: value,
				template: null,
				source: null
			}))
			setErrorMessage('')
		} else if (key === 'template') {
			setInputs(inputs => ({
				...inputs,
				[key]: value,
				source: null
			}))
			setErrorMessage('')
		} else {
			setInputs(inputs => ({
				...inputs,
				[key]: value
			}))
			if (value === 0) {
				setErrorMessage(
					<>
						<MessageHeading>Not seeing what you need?</MessageHeading>
						<div>
							<a href={'mailto:AdvitoServices@bcdtravel.eu'}>Contact I&amp;A</a>{' '}
							to add your source selection.
						</div>
					</>
				)
			} else {
				setErrorMessage('')
			}
			setSuccessMessage('')
		}
	}

	const handleDateChange = (date, dateString) => {
		setInputs(inputs => ({
			...inputs,
			fileStartDate: dateString[0],
			fileEndDate: dateString[1]
		}))
	}

	return (
		<Container>
			<StyledTitle>Ingestion Console</StyledTitle>
			<Row>
				<SelectClient
					label="Upload for Client"
					onChange={e => handleInputChange('client', e)}
				/>
				<SelectPractice
					label="Practice Area"
					variables={{ clientId: inputs.client }}
					onChange={e => handleInputChange('application', e)}
				/>
			</Row>
			<Row>
				<SelectTemplate
					label="Template"
					variables={{ applicationId: inputs.application }}
					onChange={e => handleInputChange('template', e)}
				/>
				<SelectSource
					label="Source"
					variables={{ templateId: inputs.template }}
					onChange={e => handleInputChange('source', e)}
				/>
			</Row>
			<Row>
				<DateSelect>
					<span>File Date Range</span>
					<RangePicker
						onChange={handleDateChange}
						placeholder={['Start Date', 'End Date']}
						style={{ width: '400px' }}
					/>
				</DateSelect>
			</Row>
			<FileUpload
				disabled={Object.values(inputs).some(v => v === null || v === 0)}
				inputs={inputs}
				setErrorMessage={setErrorMessage}
				setJobId={setJobId}
			/>
			{jobId && (
				<JobProgress
					setJobId={setJobId}
					jobId={jobId}
					setSuccessMessage={setSuccessMessage}
					setErrorMessage={setErrorMessage}
					MessageHeading={MessageHeading}
				/>
			)}
			{successMessage && (
				<Message message={successMessage} type="success" showIcon />
			)}
			{errorMessage && <Message message={errorMessage} type="error" showIcon />}
		</Container>
	)
}

export default Form
