import React from 'react'
import styled from 'styled-components'

import SidebarUserInfo from './SidebarUserInfo'

const Container = styled.div`
  background: ${props => props.theme.concrete};
  padding: ${props => props.theme.verticalSpace}
    ${props => props.theme.horizontalSpace};
  height: 100%;
  opacity: 0.95;
  flex: 1;
`

const Sidebar = () => {
  return (
    <Container>
      <SidebarUserInfo />
    </Container>
  )
}

export default Sidebar
