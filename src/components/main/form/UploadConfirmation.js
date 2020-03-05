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

	useEffect(() => {
		const setParsedFile = async () => {
			if (file) {
				const data = await parseExcel(file)
				setRowsArray(data)
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
			reader.readAsBinaryString(file)
			reader.onload = e => {
				var workbook = XLSX.read(e.target.result, { type: 'binary' })
				let arr = []

				workbook.SheetNames.forEach(function(sheetName) {
					var XL_row_object = XLSX.utils.sheet_to_row_object_array(
						workbook.Sheets[sheetName]
					)
					arr = [...arr, ...XL_row_object]
				})
				resolve(arr)
			}
			reader.onerror = error => reject(error)
		})

	if (loading) return <SpinLoader />
	if (error) return <ErrorMessage error={error} />
	return (
		<Modal
			title="Confirm File Upload"
			visible={visible}
			okButtonProps={{ disabled: !file, type: 'primary' }}
			cancelButtonProps={{ type: 'default' }}
			onOk={() => onOk(rowsArray.length)}
			{...props}
		>
			{file ? (
				<p>
					You are about to upload <b>{file.name}</b> with{' '}
					<b>{rowsArray.length}</b> rows for client{' '}
					{getClientName(props.selectedClient)}. Do you wish to continue?
				</p>
			) : (
				<p>No file selected. Please click or drag a file to upload area</p>
			)}
		</Modal>
	)
}

export default UploadConfirmation
