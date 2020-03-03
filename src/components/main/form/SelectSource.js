import React from 'react'
import { useQuery } from '@apollo/client'
import { SpinLoader } from 'components/common/Loader'
import ErrorMessage from 'components/common/ErrorMessage'
import { Select } from 'antd'
import { FormSelect } from './StyledComponents'

import { SOURCE_LIST } from 'api/queries'

const { Option } = Select

const SelectSource = ({ variables = null, label, onChange }) => {
	const { loading, error, data } = useQuery(SOURCE_LIST, {
		variables,
		fetchPolicy: 'network-only'
	})
	if (loading) return <SpinLoader />
	if (error) return <ErrorMessage error={error} />
	return (
		<FormSelect>
			<span>{label}</span>
			<Select onChange={onChange}>
				{data.sourceList.map((source, i) => {
					return (
						<Option key={'source' + i} value={source.id}>
							{source.sourceName}
						</Option>
					)
				})}
				<Option key={'unlisted'} value={0}>
					Source not listed
				</Option>
			</Select>
		</FormSelect>
	)
}
export default SelectSource
