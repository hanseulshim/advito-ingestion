import React, { useState } from 'react'
import styled from 'styled-components'
import { Title } from 'components/common/Typography'
import { DatePicker } from 'antd'
import FileUpload from './FileUpload'
import SelectPractice from './SelectPractice'
import SelectClient from './SelectClient'
import SelectTemplate from './SelectTemplate'
import SelectSource from './SelectSource'
const { RangePicker } = DatePicker

const Container = styled.div`
  width: 900px;
  padding-bottom: ${props => props.theme.verticalSpace};
`

const StyledTitle = styled(Title)`
  margin-bottom: ${props => props.theme.verticalSpace};
`

const Row = styled.div`
  display: flex;
  margin-bottom: ${props => props.theme.verticalSpace};
  justify-content: space-between;
`

const DateSelect = styled.div`
  display: flex;
  flex-direction: column;

  > span {
    text-transform: uppercase;
    margin-bottom: 2px;
    font-size: 0.85em;
  }
`

const Form = () => {
  const initialState = {
    client: null,
    application: null,
    template: null,
    source: null,
    fileStartDate: null,
    fileEndDate: null
  }
  const [inputs, setInputs] = useState(initialState)

  const handleInputChange = (key, value) => {
    if (key === 'client') {
      setInputs(inputs => ({
        ...inputs,
        [key]: value,
        application: null,
        template: null,
        source: null
      }))
    }
    if (key === 'application') {
      setInputs(inputs => ({
        ...inputs,
        [key]: value,
        template: null,
        source: null
      }))
    } else if (key === 'template') {
      setInputs(inputs => ({
        ...inputs,
        [key]: value,
        source: null
      }))
    } else
      setInputs(inputs => ({
        ...inputs,
        [key]: value
      }))
  }

  const handleDateChange = (date, dateString) => {
    setInputs(inputs => ({
      ...inputs,
      fileStartDate: dateString[0],
      fileEndDate: dateString[1]
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
          variables={{ clientId: inputs.client || null }}
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
      <Row>
        <DateSelect>
          <span>File Date Range</span>
          <RangePicker
            onChange={handleDateChange}
            placeholder={['Start Date', 'End Date']}
            style={{ width: '400px' }}
          />
        </DateSelect>
      </Row>
      <FileUpload disabled={
        Object.values(inputs).some(v => v === null)
      } inputs={inputs} />
    </Container>
  )
}

export default Form
