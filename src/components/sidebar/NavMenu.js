import React from 'react'
import styled from 'styled-components'
import { Popover } from 'antd'
import { Link } from 'react-router-dom'
import Icon from 'components/common/Icon'
import './NavMenu.css'
import { LOGOUT } from 'api'
import { useMutation } from '@apollo/react-hooks'
import Loader from 'components/common/Loader'
import { removeUser, getUser } from 'helper'

const NavItem = styled(Link)`
  color: ${props => props.theme.white};
  margin-bottom: 1em;
  cursor: pointer;
  :hover {
    color: ${props => props.theme.white};
    text-decoration: underline;
  }
`

const LogOut = styled.span`
  color: ${props => props.theme.white};
  margin-bottom: 1em;
  cursor: pointer;
  :hover {
    color: ${props => props.theme.white};
    text-decoration: underline;
  }
`

const PersonIcon = styled(Icon)`
  font-size: 1em;
  color: ${props => props.theme.treePoppy};
  cursor: pointer;

  :hover {
    color: ${props => props.theme.tradewind};
  }
`

const navItems = [
  {
    link: '/user-profile',
    title: 'User Profile'
  },
  {
    link: '/client-setup',
    title: 'Client Setup'
  }
]

const NavMenu = () => {
  const [logout, { loading, error, data }] = useMutation(LOGOUT)
  const { sessionToken = '' } = getUser()
  if (loading) return <Loader />
  if (data || error) removeUser()
  return (
    <Popover
      content={
        <>
          {navItems.map(({ link, title }, index) => (
            <NavItem key={index} to={link}>
              {title}
            </NavItem>
          ))}
          <LogOut onClick={() => logout({ variables: { sessionToken } })}>
            Logout
          </LogOut>
        </>
      }
      trigger="click"
    >
      <PersonIcon icon="cog">Click me</PersonIcon>
    </Popover>
  )
}

export default NavMenu
