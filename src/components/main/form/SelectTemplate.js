import React from 'react'
import { useQuery } from '@apollo/client'
import { SpinLoader } from 'components/common/Loader'
import ErrorMessage from 'components/common/ErrorMessage'
import { Select } from 'antd'
import { FormSelect } from './StyledComponents'

import { TEMPLATE_LIST } from 'api/queries'

const { Option } = Select

const SelectTemplate = ({ variables = null, label, onChange }) => {
  const { loading, error, data } = useQuery(TEMPLATE_LIST, {
    variables,
    fetchPolicy: 'network-only'
  })
  if (loading) return <SpinLoader />
  if (error) return <ErrorMessage error={error} />
  return (
    <FormSelect>
      <span>{label}</span>
      <Select onChange={onChange}>
        {data.templateList.map((template, i) => {
          return (
            <Option key={'template' + i} value={template.id}>
              {template.templateName}
            </Option>
          )
        })}
      </Select>
    </FormSelect>
  )
}

export default SelectTemplate
