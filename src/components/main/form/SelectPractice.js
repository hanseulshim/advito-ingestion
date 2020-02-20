import React from 'react'
import styled from 'styled-components'
import { useQuery } from '@apollo/react-hooks'
import { SpinLoader } from 'components/common/Loader'
import ErrorMessage from 'components/common/ErrorMessage'
import { Select } from 'antd'
import { FormSelect } from './StyledComponents'
import { PRACTICE_AREA_LIST } from 'api/queries'

const { Option } = Select

const SelectPractice = ({ variables = null, label, onChange }) => {
  const { loading, error, data } = useQuery(PRACTICE_AREA_LIST, {
    variables,
    fetchPolicy: 'network-only'
  })
  if (loading) return <SpinLoader />
  if (error) return <ErrorMessage error={error} />
  return (
    <FormSelect>
      <span>{label}</span>
      <Select onChange={onChange}>
        {data.practiceAreaList.map((application, i) => {
          return (
            <Option key={'application' + i} value={application.id}>
              {application.applicationName}
            </Option>
          )
        })}
      </Select>
    </FormSelect>
  )
}

export default SelectPractice
