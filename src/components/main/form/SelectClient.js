import React from 'react'
import { useQuery } from '@apollo/client'
import { SpinLoader } from 'components/common/Loader'
import ErrorMessage from 'components/common/ErrorMessage'
import { Select } from 'antd'
import { FormSelect } from './StyledComponents'

import { CLIENT_LIST } from 'api/queries'

const { Option } = Select

const SelectClient = ({ label, onChange }) => {
	const { loading, error, data } = useQuery(CLIENT_LIST)
	if (loading) return <SpinLoader />
	if (error) return <ErrorMessage error={error} />
	return (
		<FormSelect>
			<span>{label}</span>
			<Select
				onChange={onChange}
				showSearch
				filterOption={(input, option) =>
					option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
				}
			>
				{data.clientList.map((client, i) => {
					return (
						<Option key={'client' + i} value={client.id}>
							{client.clientName}
						</Option>
					)
				})}
			</Select>
		</FormSelect>
	)
}

export default SelectClient
