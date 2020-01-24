import React, { useState } from 'react'
import styled from 'styled-components'
import Icon from 'components/common/Icon'
import SidebarUserInfo from './SidebarUserInfo'

const Container = styled.div`
  background: ${props => props.theme.white};
  border: 1px solid ${props => props.theme.grayNurse};
  padding: 2.5em 4em;
  height: 100%;
  position: absolute;
  opacity: 0.95;
  width: 300px;
  z-index: 5;
  left: 0;
`

const PersonIcon = styled(Icon)`
  position: absolute;
  padding: 7px;
  font-size: 2.5em;
  background: ${props => props.theme.white};
  border: 1px solid ${props => props.theme.grayNurse};
  border-left: none;
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
  top: 3em;
  color: ${props => props.theme.treePoppy};
  cursor: pointer;
  left: 0;
`

const CloseIcon = styled(PersonIcon)`
  left: 298px;
`

const Sidebar = () => {
  const [collapse, setCollapse] = useState(true)

  return collapse ? (
    <PersonIcon icon="user" onClick={() => setCollapse(false)} />
  ) : (
    <Container>
      <CloseIcon icon="times" onClick={() => setCollapse(true)} />
      <SidebarUserInfo />
    </Container>
  )
}

export default Sidebar
