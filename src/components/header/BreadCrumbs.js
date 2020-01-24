import React from 'react'
import styled from 'styled-components'
import { Link, useLocation } from 'react-router-dom'

const Container = styled.div`
  display: flex;
  align-items: center;
  margin-top: 1em;
  margin-bottom: ${props => props.theme.verticalSpace};
`

const Spacer = styled.div`
  margin: 0 0.5em;
`

const Text = styled.div`
  color: initial;
`

const BackTo = styled(Text)`
  color: ${props => props.theme.treePoppy};
  cursor: pointer;
  &:hover {
    text-decoration: underline;
    color: ${props => props.theme.treePoppy};
  }
`

const getPath = path => {
  switch (path) {
    case 'dashboard':
      return 'Dashboard'
    case 'user-profile':
      return 'User Profile'
    case 'client-setup':
      return 'Clients'
    case 'user-access':
      return 'Advito Users'
    default:
      return ''
  }
}

const getSubPath = subpath => {
  switch (subpath) {
    case 'program-performance':
      return 'Program Performance'
    case 'net-spend-analysis':
      return 'Net Spend Analysis'
    case 'te-breakdown':
      return 'T&E Breakdown'
    case 'markets':
      return 'Markets'
    case 'savings-opportunities':
      return 'Savings Opportunities'
    case 'risk-areas':
      return 'Risk Areas'
    case 'general':
      return 'General'
    case 'divisions':
      return 'Divisions'
    case 'users':
      return 'Users'
    case 'applications':
      return 'Applications'
    default:
      return ''
  }
}

const BreadCrumbs = () => {
  const location = useLocation()
  const { pathname } = location
  const subPaths = pathname.split('/')
  const renderSubPaths = subPaths.length === 3 && subPaths[2] !== 'dashboard'

  return (
    <Container>
      <Link replace to={'/'}>
        <BackTo>{'«'} Back to Console</BackTo>
      </Link>
      <Spacer>|</Spacer>
      {renderSubPaths && !pathname.includes('client-setup') ? (
        <Link to={`/${subPaths[1]}/dashboard`}>
          <BackTo>{getPath(subPaths[1])}</BackTo>
        </Link>
      ) : renderSubPaths ? (
        <Link to={'/client-setup'}>
          <BackTo>{getPath(subPaths[1])}</BackTo>
        </Link>
      ) : (
        <Text>{getPath(subPaths[1])}</Text>
      )}
      {renderSubPaths && (
        <>
          <Spacer>|</Spacer>
          <Text>{getSubPath(subPaths[2])}</Text>
        </>
      )}
    </Container>
  )
}

export default BreadCrumbs
