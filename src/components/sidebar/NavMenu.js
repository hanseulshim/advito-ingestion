import React, { useState, useEffect } from 'react'
import styled from 'styled-components'
import { Popover } from 'antd'
import './NavMenu.css'
import { LOGOUT } from 'api'
import { useMutation } from '@apollo/client'
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
	const [sessionToken, setSessionToken] = useState('')
	useEffect(() => {
		const { sessionToken } = getUser()
		setSessionToken(sessionToken)
	}, [])
	const [logout] = useMutation(LOGOUT, {
		client: authClient,
		onCompleted: () => {
			removeUser()
		}
	})
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
