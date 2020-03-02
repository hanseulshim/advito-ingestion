import React, { useEffect, useState } from 'react'
import styled from 'styled-components'
import { Upload, Icon } from 'antd'
import { useMutation } from '@apollo/client'
import { UPLOAD_FILE } from 'api/mutations'
const { Dragger } = Upload

const Container = styled.div`
	margin-bottom: ${props => props.theme.verticalSpace};
`

const UploadButton = styled.button`
	color: ${props => props.theme.treePoppy};
	border: 1px solid ${props => props.theme.treePoppy};
	background: (0, 0, 0, 0);
	border-radius: 15px;
	padding: 2px 20px;
	text-transform: uppercase;
	font-size: 0.75em;
	margin-left: 42.5%;
	cursor: pointer;
	:hover {
		background: ${props => props.theme.treePoppy};
		color: ${props => props.theme.white};
	}
`
const ErrorMessage = styled.div`
	color: ${props => props.theme.deepBlush};
`

const SuccessMessage = styled.div`
	color: ${props => props.theme.easternWind};
`

const toBase64 = file =>
	new Promise((resolve, reject) => {
		const reader = new FileReader()
		reader.readAsDataURL(file)
		reader.onload = () => resolve(reader.result)
		reader.onerror = error => reject(error)
	})

const FileUpload = ({ inputs, disabled }) => {
	const [fileList, setFile] = useState([])
	const [errorMessage, setErrorMessage] = useState('')
	const [successMessage, setSuccessMessage] = useState('')
	const [uploadFile] = useMutation(UPLOAD_FILE)

	useEffect(() => {
		if (inputs.source === 0) {
			setErrorMessage(
				'Not seeing what you need? Contact I&A to add your source selection.'
			)
			setFile([])
			setTimeout(() => {
				setErrorMessage('')
			}, 5000)
		}
	}, [inputs.source])

	const dummyRequest = ({ onSuccess }) => {
		setTimeout(() => {
			onSuccess(null)
		}, 0)
	}

	const handleFileUpload = async () => {
		try {
			const file = fileList[0].originFileObj
			const base64 = await toBase64(file)
			await uploadFile({
				variables: {
					clientId: inputs.client,
					sourceId: inputs.source,
					dataStartDate: inputs.fileStartDate,
					dataEndDate: inputs.fileEndDate,
					fileName: file.name,
					base64
				}
			})
			setSuccessMessage('File uploaded successfully.')
			setTimeout(() => {
				setFile([])
				setSuccessMessage('')
			}, 1500)
		} catch (e) {
			setErrorMessage(e.message)
			setTimeout(() => {
				setErrorMessage('')
			}, 1500)
		}
	}

	const onFileChange = async info => {
		if (info.file.status === 'removed') {
			setFile([])
		} else {
			info.file.status = 'done'
			setFile([info.file])
		}
	}

	return (
		<>
			<Container>
				<Dragger
					accept=".xlsx"
					disabled={disabled}
					multiple={false}
					customRequest={dummyRequest}
					showUploadList={{
						showDownloadIcon: false
					}}
					onChange={onFileChange}
					fileList={fileList}
				>
					<p className="ant-upload-drag-icon">
						<Icon type="inbox" />
					</p>
					<p className="ant-upload-text">
						Click or drag file to this area to upload
					</p>
				</Dragger>
				<ErrorMessage>{errorMessage}</ErrorMessage>
				<SuccessMessage>{successMessage}</SuccessMessage>
			</Container>
			<div style={{ maxWidth: '900px' }}>
				<UploadButton onClick={() => handleFileUpload()}>Upload</UploadButton>
			</div>
		</>
	)
}

export default FileUpload
