import React from 'react'
import styled from 'styled-components'
import { Popover } from 'antd'
import './NavMenu.css'
import { LOGOUT } from 'api'
import { useMutation } from '@apollo/client'
import { SpinLoader } from 'components/common/Loader'
import { removeUser, getUser } from 'helper'
import { SettingFilled } from '@ant-design/icons'
import colors from 'styles/variables'
import { authClient } from 'index'

const LogOut = styled.span`
	color: ${props => props.theme.white};
	cursor: pointer;
	:hover {
		color: ${props => props.theme.white};
		text-decoration: underline;
	}
`

const NavMenu = () => {
	const [logout, { loading, error, data }] = useMutation(LOGOUT, {
		client: authClient
	})
	const { sessionToken = '' } = getUser()
	if (loading) return <SpinLoader />
	if (data || error) removeUser()
	return (
		<Popover
			content={
				<LogOut onClick={() => logout({ variables: { sessionToken } })}>
					Logout
				</LogOut>
			}
			trigger="click"
			placement="bottom"
		>
			<SettingFilled style={{ fontSize: '1.5em', color: colors.treePoppy }} />
		</Popover>
	)
}

export default NavMenu
