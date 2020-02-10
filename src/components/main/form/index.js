import React, { useState } from 'react'
import styled from 'styled-components'
import { Title } from 'components/common/Typography'
import { Select } from 'antd'
import {
  CLIENT_LIST,
  APPLICATION_LIST,
  TEMPLATE_LIST,
  SOURCE_LIST
} from 'api/queries'
import { useQuery } from '@apollo/react-hooks'
import Loader from 'components/common/Loader'
import ErrorMessage from 'components/common/ErrorMessage'

const Container = styled.div``

const StyledTitle = styled(Title)`
  margin-bottom: ${props => props.theme.verticalSpace};
`

const Row = styled.div`
  display: flex;
  margin-bottom: ${props => props.theme.verticalSpace};
`

const FormSelect = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: 400px;
  margin-right: ${props => props.theme.horizontalSpace};
  > span {
    text-transform: uppercase;
    margin-bottom: 2px;
    font-size: 0.85em;
  }
`

const File = styled.input`
  display: block;
  margin-bottom: ${props => props.theme.verticalSpace};
`

const Upload = styled.button`
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
const { Option } = Select

const SelectClient = ({ variables = null, label, onChange }) => {
  const { loading, error, data } = useQuery(CLIENT_LIST)
  if (loading) return <Loader />
  if (error) return <ErrorMessage error={error} />
  return (
    <FormSelect>
      <span>{label}</span>
      <Select onChange={onChange}>
        {data.clientList.map((client, i) => {
          return (
            <Option key={client + i} value={client.id}>
              {client.clientName}
            </Option>
          )
        })}
      </Select>
    </FormSelect>
  )
}

const SelectPractice = ({ variables = null, label, onChange }) => {
  const { loading, error, data } = useQuery(APPLICATION_LIST)
  if (loading) return <Loader />
  if (error) return <ErrorMessage error={error} />
  return (
    <FormSelect>
      <span>{label}</span>
      <Select onChange={onChange}>
        {data.applicationList.map((application, i) => {
          return (
            <Option key={application + i} value={application.id}>
              {application.applicationName}
            </Option>
          )
        })}
      </Select>
    </FormSelect>
  )
}

const SelectTemplate = ({ variables = null, label, onChange }) => {
  const { loading, error, data } = useQuery(TEMPLATE_LIST, {
    variables
  })
  if (loading) return <Loader />
  if (error) return <ErrorMessage error={error} />
  return (
    <FormSelect>
      <span>{label}</span>
      <Select onChange={onChange}>
        {data.templateList.map((template, i) => {
          return (
            <Option key={template + i} value={template.id}>
              {template.templateName}
            </Option>
          )
        })}
      </Select>
    </FormSelect>
  )
}

const SelectSource = ({ variables = null, label, onChange }) => {
  const { loading, error, data } = useQuery(SOURCE_LIST, {
    variables
  })
  if (loading) return <Loader />
  if (error) return <ErrorMessage error={error} />
  return (
    <FormSelect>
      <span>{label}</span>
      <Select onChange={onChange}>
        {data.sourceList.map((source, i) => {
          return (
            <Option key={source + i} value={source.id}>
              {source.sourceName}
            </Option>
          )
        })}
      </Select>
    </FormSelect>
  )
}

const Form = () => {
  const [inputs, setInputs] = useState({})

  const handleInputChange = (key, value) => {
    setInputs(inputs => ({
      ...inputs,
      [key]: value
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
          onChange={e => handleInputChange('application', e)}
        />
      </Row>
      <Row>
        <SelectTemplate
          label="Template"
          variables={{ applicationId: inputs.application || null }}
          onChange={e => handleInputChange('template', e)}
        />
        <SelectSource
          label="Source"
          variables={{ templateId: inputs.template || null }}
          onChange={e => handleInputChange('source', e)}
        />
      </Row>
      <File type="file" onChange={e => handleInputChange('file', e)} />
      <Upload onClick={e => console.log}>Upload</Upload>
    </Container>
  )
}

export default Form
