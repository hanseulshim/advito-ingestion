import React from 'react'
import styled from 'styled-components'
import { Title } from 'components/common/Typography'
import { Link } from 'react-router-dom'
// import User from 'assets/user.png'
import { getUser } from 'helper'
import NavMenu from './NavMenu'

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100px;
  margin-bottom: 3em;
`

const Avatar = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  img {
    border-radius: 50%;
    border: 1px solid ${props => props.theme.doveGray};
    width: 5em;
    vertical-align: bottom;
  }
`

const TitleContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: flex-end;
  margin-bottom: 0.75em;
`

const SideBarUserInfo = () => {
  const user = getUser()
  return (
    <Container>
      <TitleContainer>
        <Avatar>
          <Link to="/user-profile" replace>
            {/* <img src={User} alt="avatar" /> */}
          </Link>
        </Avatar>
        <NavMenu />
      </TitleContainer>
      <div>
        <Title>{user.displayName}</Title>
      </div>
    </Container>
  )
}

export default SideBarUserInfo
