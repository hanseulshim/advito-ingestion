import React, { useEffect, useState } from 'react'
import styled from 'styled-components'
import { Upload, Button } from 'antd'
import { InboxOutlined } from '@ant-design/icons'
import { useMutation } from '@apollo/client'
import { UPLOAD_FILE } from 'api/mutations'
import UploadConfirmation from './UploadConfirmation'
const { Dragger } = Upload

const Container = styled.div`
	display: flex;
	flex-direction: column;
	margin-bottom: ${(props) => props.theme.verticalSpace};
`

const UploadButton = styled(Button)`
	margin: 25px 0;
	align-self: center;
	width: 100px;
`

const toBase64 = (file) =>
	new Promise((resolve, reject) => {
		const reader = new FileReader()
		reader.readAsDataURL(file)
		reader.onload = () => resolve(reader.result)
		reader.onerror = (error) => reject(error)
	})

const FileUpload = ({ inputs, disabled, setMessage, setJobId }) => {
	const [fileList, setFile] = useState([])
	const [uploadFile] = useMutation(UPLOAD_FILE, {
		onCompleted: ({ uploadFile }) => {
			setJobId(uploadFile)
			setFile([])
			setMessage({})
		},
	})
	const [modal, setModal] = useState(false)

	useEffect(() => {
		if (inputs.source === 0) {
			setFile([])
		}
	}, [inputs.source])

	const dummyRequest = ({ onSuccess }) => {
		setTimeout(() => {
			onSuccess(null)
		}, 0)
	}

	const toggleModal = () => {
		setModal(!modal)
	}

	const handleFileUpload = async () => {
		try {
			toggleModal()
			if (!fileList.length) return
			const file = fileList[0].originFileObj
			const fileSize = file.size
			const base64 = await toBase64(file)
			await uploadFile({
				variables: {
					clientId: inputs.client,
					sourceId: inputs.source,
					dataStartDate: inputs.fileStartDate,
					dataEndDate: inputs.fileEndDate,
					fileName: file.name,
					fileSize,
					base64,
				},
			})
		} catch (e) {
			toggleModal()
			setMessage({ message: e.message, type: 'error' })
		}
	}

	const onFileChange = async (info) => {
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
						showDownloadIcon: false,
					}}
					onChange={onFileChange}
					fileList={fileList}
				>
					<p className="ant-upload-drag-icon">
						<InboxOutlined />
					</p>
					<p className="ant-upload-text">
						Click or drag file to this area to upload
					</p>
				</Dragger>
				<UploadButton type="primary" onClick={() => toggleModal()}>
					Upload
				</UploadButton>
			</Container>
			<UploadConfirmation
				visible={modal}
				file={fileList.length > 0 ? fileList[0].originFileObj : null}
				onCancel={() => toggleModal()}
				onOk={handleFileUpload}
				selectedClient={inputs.client}
			/>
		</>
	)
}

export default FileUpload
