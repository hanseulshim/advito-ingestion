import React, { useState } from 'react'
import styled from 'styled-components'

import { Upload, Icon, message } from 'antd'

const { Dragger } = Upload

const Container = styled.div`
  margin-bottom: ${props => props.theme.verticalSpace};
`

const FileUpload = ({ disabled }) => {
  const [validation, setValidation] = useState('')

  const onFileChange = info => {
    const { status } = info.file
    if (status !== 'uploading') {
      console.log(info.file, info.fileList)
    }
    if (status === 'done') {
      //   message.success(`${info.file.name} file uploaded successfully.`)
      setValidation(
        'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'
      )
    } else if (status === 'error') {
      message.error(`${info.file.name} file upload failed.`)
    }
  }

  return (
    <Container>
      <Dragger
        disabled={disabled}
        name={'file'}
        multiple={false}
        action={'https://www.mocky.io/v2/5cc8019d300000980a055e76'}
        onChange={onFileChange}
      >
        <p className="ant-upload-drag-icon">
          <Icon type="inbox" />
        </p>
        <p className="ant-upload-text">
          Click or drag file to this area to upload
        </p>
      </Dragger>
      <div>{validation}</div>
    </Container>
  )
}

export default FileUpload
