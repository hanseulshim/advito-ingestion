import React from 'react'
import styled from 'styled-components'
import { APPLICATION_LIST, SAMPLE_TEMPLATE_LIST } from 'api/queries'
import SidebarUserInfo from './SidebarUserInfo'
import { useQuery } from '@apollo/react-hooks'
import Title from 'components/common/Typography'
import { SpinLoader } from 'components/common/Loader'
import ErrorMessage from 'components/common/ErrorMessage'

const Container = styled.div`
  background: ${props => props.theme.concrete};
  padding: ${props => props.theme.verticalSpace}
    ${props => props.theme.horizontalSpace};
  opacity: 0.95;
  flex: 1;
  min-width: 320px;
  max-width: 400px;
`

const ListContainer = styled.div`
  margin-bottom: ${props => props.theme.verticalSpace};
`

const ListTitle = styled(Title)`
  text-transform: uppercase;
`

const App = styled.span`
  display: block;
  margin-bottom: 5px;
`
const Link = styled.a`
  display: block;
  color: ${props => props.theme.steelBlue};
  margin-bottom: 5px;
`

const MyApplications = () => {
  const { loading, error, data } = useQuery(APPLICATION_LIST, {
    fetchPolicy: 'network-only'
  })
  if (loading) return <SpinLoader />
  if (error) return <ErrorMessage error={error} />
  return (
    <ListContainer>
      <ListTitle level={4}>MY APPLICATIONS</ListTitle>
      {data.applicationList.map((application, i) => {
        return <App key={'app' + i}>{application.applicationName}</App>
      })}
    </ListContainer>
  )
}

const SampleTemplates = () => {
  const { loading, error, data } = useQuery(SAMPLE_TEMPLATE_LIST, {
    fetchPolicy: 'network-only'
  })
  if (loading) return <SpinLoader />
  if (error) return <ErrorMessage error={error} />
  return (
    <ListContainer>
      <ListTitle level={4}>SAMPLE TEMPLATES</ListTitle>
      {data.sampleTemplateList.map((template, i) => {
        return (
          <Link key={'template' + i} href={template.templatePath} download>
            {template.applicationName} - {template.templateName}
          </Link>
        )
      })}
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
