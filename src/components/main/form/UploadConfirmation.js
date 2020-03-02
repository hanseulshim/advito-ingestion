import React from 'react'
import { useQuery } from '@apollo/client'
import { SpinLoader } from 'components/common/Loader'
import ErrorMessage from 'components/common/ErrorMessage'
import { Modal } from 'antd'
import { CLIENT_LIST } from 'api/queries'

const UploadConfirmation = ({ visible, file, ...props }) => {
  const { loading, error, data } = useQuery(CLIENT_LIST)
  if (loading) return <SpinLoader />
  if (error) return <ErrorMessage error={error} />

  const getClientName = clientId => {
    return (
      <b>{data.clientList.find(client => client.id === clientId).clientName}</b>
    )
  }

  return (
    <Modal
      title="Confirm File Upload"
      visible={visible}
      okButtonProps={{ disabled: !file }}
      {...props}
    >
      {file ? (
        <p>
          You are about to upload <b>{file.name}</b> with X rows for client{' '}
          {getClientName(props.selectedClient)}. Do you wish to continue?
        </p>
      ) : (
        <p>No file selected. Please click or drag a file to upload area</p>
      )}
    </Modal>
  )
}

export default UploadConfirmation
