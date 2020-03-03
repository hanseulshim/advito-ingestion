import React, { useState } from 'react'
import styled from 'styled-components'
import { Upload, Icon, message, Modal } from 'antd'
import { useMutation } from '@apollo/client'
import { UPLOAD_FILE } from 'api/mutations'
import UploadConfirmation from './UploadConfirmation'
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
  const [file, setFile] = useState(null)
  const [errorMessage, setErrorMessage] = useState('')
  const [successMessage, setSuccessMessage] = useState('')
  const [modal, setModal] = useState(false)
  const [uploadFile] = useMutation(UPLOAD_FILE)

  const dummyRequest = ({ file, onSuccess }) => {
    setTimeout(() => {
      onSuccess('ok')
    }, 0)
  }

  const toggleModal = () => {
    setModal(!modal)
  }

  const handleFileUpload = async rowCount => {
    try {
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
      toggleModal()
      setSuccessMessage('File uploaded successfully.')
      setTimeout(() => {
        setSuccessMessage('')
      }, 5000)
    } catch (e) {
      toggleModal()
      setErrorMessage(e.message)
      setTimeout(() => {
        setErrorMessage('')
      }, 5000)
    }
  }

  const onFileChange = async info => {
    const { status } = info.file
    if (status === 'done') {
      setFile(info.file.originFileObj)
    } else if (status === 'error') {
      message.error(`${info.file.name} file upload failed.`)
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
          onChange={onFileChange}
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
      <UploadConfirmation
        visible={modal}
        file={file}
        onCancel={() => toggleModal()}
        onOk={handleFileUpload}
        selectedClient={inputs.client}
      />
      <div style={{ maxWidth: '900px' }}>
        <UploadButton onClick={() => toggleModal()}>Upload</UploadButton>
      </div>
    </>
  )
}

export default FileUpload
