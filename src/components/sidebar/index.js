import React from 'react'
import styled from 'styled-components'
import { APPLICATION_LIST } from 'api/queries'
import SidebarUserInfo from './SidebarUserInfo'
import { useQuery } from '@apollo/react-hooks'
import Title from 'components/common/Typography'
import Loader from 'components/common/Loader'
import ErrorMessage from 'components/common/ErrorMessage'

const Container = styled.div`
  background: ${props => props.theme.concrete};
  padding: ${props => props.theme.verticalSpace}
    ${props => props.theme.horizontalSpace};
  height: 100%;
  opacity: 0.95;
  flex: 1;
`

const ListContainer = styled.div``

const MyApplications = () => {
  const { loading, error, data } = useQuery(APPLICATION_LIST)
  if (loading) return <Loader />
  if (error) return <ErrorMessage error={error} />
  return (
    <ListContainer>
      <Title level={4}>My Applications</Title>
      {data.applicationList.map((application, i) => {
        return <p>{application.applicationName}</p>
      })}
    </ListContainer>
  )
}

const SampleTemplates = () => {
  // const { loading, error, data } = useQuery(APPLICATION_LIST)
  // if (loading) return <Loader />
  // if (error) return <ErrorMessage error={error} />
  return (
    <ListContainer>
      <Title level={4}>Sample Templates</Title>
      {/* {data.applicationList.map((application, i) => {
        return <p>{application.applicationName}</p>
      })} */}
    </ListContainer>
  )
}

const Sidebar = () => {
  return (
    <Container>
      <SidebarUserInfo />
      <MyApplications />
      <SampleTemplates />
    </Container>
  )
}

export default Sidebar
