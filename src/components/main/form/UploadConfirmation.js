import React, { useEffect, useState } from 'react'
import { useQuery } from '@apollo/client'
import { SpinLoader } from 'components/common/Loader'
import ErrorMessage from 'components/common/ErrorMessage'
import { Modal } from 'antd'
import { CLIENT_LIST } from 'api/queries'
import { GET_PRESIGNED_UPLOAD_URL } from 'api/queries'
import XLSX from 'xlsx'
import { client } from 'index'

const UploadConfirmation = ({ visible, file, uploadFile, ...props }) => {
	const { loading, error, data } = useQuery(CLIENT_LIST)
	const [signedUrl, updateSignedUrl] = useState(null)
	const [message, setMessage] = useState('')
	const [parsingError, setError] = useState('')

	useEffect(() => {
		const setParsedFile = async () => {
			if (file) {
				try {
					const message = await parseExcel(file)
					setMessage(message)

					const result = await client.query({
						query: GET_PRESIGNED_UPLOAD_URL,
						variables: {
							fileName: file.name,
						},
						fetchPolicy: 'network-only',
						//fetch a POST with
						onError: (e) => console.log(e),
					})
					updateSignedUrl(result.data.getPresignedUploadUrl)
					setError('')
				} catch (e) {
					setError(e)
					setMessage('')
					updateSignedUrl(null)
				}
			}
		}
		setParsedFile()
	}, [file])

	const getClientName = (clientId) => {
		return data.clientList.find((client) => client.id === clientId).clientName
	}

	const bytesToMegaBytes = (bytes) => bytes / (1024 * 1024)

	const parseExcel = (file) =>
		new Promise((resolve, reject) => {
			const reader = new FileReader()
			const type = reader.readAsBinaryString ? 'binary' : 'array'
			type === 'binary'
				? reader.readAsBinaryString(file)
				: reader.readAsArrayBuffer(file)
			reader.onload = (e) => {
				var workbook = XLSX.read(e.target.result, { type })
				let arr = []

				if (workbook.SheetNames.length > 1) {
					reject(
						'The file you are trying to upload has multiple worksheets. This is not allowed.'
					)
				} else if (file.size > 10000000) {
					resolve(`You are about to upload ${file.name} with 
					${bytesToMegaBytes(file.size).toFixed(2)} MB for client
					${getClientName(props.selectedClient)}. Do you wish to continue?`)
				} else {
					workbook.SheetNames.forEach(function (sheetName) {
						var XL_row_object = XLSX.utils.sheet_to_row_object_array(
							workbook.Sheets[sheetName]
						)

						arr = [...arr, ...XL_row_object]
					})
					if (arr.length > 0) {
						resolve(`You are about to upload ${file.name} with 
						${arr.length} rows for client
						${getClientName(props.selectedClient)}. Do you wish to continue?`)
					} else reject('The file you are trying to upload is empty')
				}
			}
			reader.onerror = (error) => reject(error)
		})

	if (loading) return <SpinLoader />
	if (error) return <ErrorMessage error={error} />

	return (
		<Modal
			title="Confirm File Upload"
			visible={visible}
			okButtonProps={{
				style: {
					display: !file || parsingError || !signedUrl ? 'none' : '',
				},
				type: 'primary',
			}}
			cancelButtonProps={{ type: 'default' }}
			onOk={() => uploadFile(signedUrl)}
			{...props}
		>
			{file && message && <p>{message}</p>}
			{file && parsingError && <p>{parsingError}</p>}
			{!file && (
				<p>No file selected. Please click or drag a file to upload area</p>
			)}
		</Modal>
	)
}

export default UploadConfirmation
