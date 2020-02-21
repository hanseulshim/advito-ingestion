import React from 'react'
import styled from 'styled-components'
import { Popover } from 'antd'
import Icon from 'components/common/Icon'
import './NavMenu.css'
import { LOGOUT } from 'api'
import { useMutation } from '@apollo/client'
import { SpinLoader } from 'components/common/Loader'
import { removeUser, getUser } from 'helper'

const LogOut = styled.span`
  color: ${props => props.theme.white};
  cursor: pointer;
  :hover {
    color: ${props => props.theme.white};
    text-decoration: underline;
  }
`

const PersonIcon = styled(Icon)`
  font-size: 1.5em;
  color: ${props => props.theme.treePoppy};
  cursor: pointer;
  :hover {
    color: ${props => props.theme.tradewind};
  }
`

const NavMenu = () => {
  const [logout, { loading, error, data }] = useMutation(LOGOUT)
  const { sessionToken = '' } = getUser()
  if (loading) return <SpinLoader />
  if (data || error) removeUser()
  return (
    <Popover
      content={
        <>
          <LogOut onClick={() => logout({ variables: { sessionToken } })}>
            Logout
          </LogOut>
        </>
      }
      trigger="click"
      placement="bottom"
    >
      <PersonIcon icon="cog" />
    </Popover>
  )
}

export default NavMenu
