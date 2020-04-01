import React, { useEffect, useState } from 'react'
import { useQuery } from '@apollo/client'
import { SpinLoader } from 'components/common/Loader'
import ErrorMessage from 'components/common/ErrorMessage'
import { Modal } from 'antd'
import { CLIENT_LIST } from 'api/queries'
import XLSX from 'xlsx'

const UploadConfirmation = ({ visible, file, onOk, ...props }) => {
	const { loading, error, data } = useQuery(CLIENT_LIST)
	const [rowsArray, setRowsArray] = useState([])
	const [parsingError, setError] = useState('')

	useEffect(() => {
		const setParsedFile = async () => {
			if (file) {
				try {
					const data = await parseExcel(file)
					setRowsArray(data)
					setError('')
				} catch (e) {
					setError(e)
					setRowsArray([])
				}
			}
		}
		setParsedFile()
	}, [file])

	const getClientName = clientId => {
		return (
			<b>{data.clientList.find(client => client.id === clientId).clientName}</b>
		)
	}

	const parseExcel = file =>
		new Promise((resolve, reject) => {
			const reader = new FileReader()
			const type = reader.readAsBinaryString ? 'binary' : 'array'
			type === 'binary'
				? reader.readAsBinaryString(file)
				: reader.readAsArrayBuffer(file)
			reader.onload = e => {
				var workbook = XLSX.read(e.target.result, { type })
				let arr = []

				if (workbook.SheetNames.length > 1) {
					reject(
						'The file you are trying to upload has multiple worksheets. This is not allowed.'
					)
				} else {
					workbook.SheetNames.forEach(function(sheetName) {
						var XL_row_object = XLSX.utils.sheet_to_row_object_array(
							workbook.Sheets[sheetName]
						)

						arr = [...arr, ...XL_row_object]
					})
					resolve(arr)
				}
			}
			reader.onerror = error => reject(error)
		})

	if (loading) return <SpinLoader />
	if (error) return <ErrorMessage error={error} />
	return (
		<Modal
			title="Confirm File Upload"
			visible={visible}
			okButtonProps={{ disabled: !file || parsingError, type: 'primary' }}
			cancelButtonProps={{ type: 'default' }}
			onOk={() => onOk(rowsArray.length)}
			{...props}
		>
			{file && rowsArray.length > 0 && (
				<p>
					You are about to upload <b>{file.name}</b> with{' '}
					<b>{rowsArray.length}</b> rows for client{' '}
					{getClientName(props.selectedClient)}. Do you wish to continue?
				</p>
			)}
			{!file && (
				<p>No file selected. Please click or drag a file to upload area</p>
			)}
			{file && parsingError && <p>{parsingError}</p>}
		</Modal>
	)
}

export default UploadConfirmation
