import React, { useEffect, useState } from 'react'
import styled from 'styled-components'
import { Upload, Icon } from 'antd'
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

const toBase64 = file =>
  new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result)
    reader.onerror = error => reject(error)
  })

const FileUpload = ({
  inputs,
  disabled,
  setSuccessMessage,
  setErrorMessage,
  MessageHeading
}) => {
  const [fileList, setFile] = useState([])
  const [uploadFile] = useMutation(UPLOAD_FILE)
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

  const handleFileUpload = async rowCount => {
    try {
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
          rowCount,
          fileSize,
          base64
        }
      })
      toggleModal()
      setSuccessMessage(
        <MessageHeading>
          Your file {file.name} has been successfully uploaded!
        </MessageHeading>
      )
      setErrorMessage('')
    } catch (e) {
      toggleModal()
      setErrorMessage(e.message)
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
      </Container>
      <UploadConfirmation
        visible={modal}
        file={fileList.length > 0 ? fileList[0].originFileObj : null}
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
