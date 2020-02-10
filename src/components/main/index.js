import React from 'react'
import styled from 'styled-components'
import Sidebar from 'components/sidebar'
import Form from './form'
import advitoLogo from 'assets/advitoLogo.png'

const MainContainer = styled.div`
  width: 100%;
  display: flex;
  height: 100%;
`

const FormContainer = styled.div`
  display: flex;
  flex: 4;
  flex-direction: column;
  padding: ${props => props.theme.verticalSpace}
    ${props => props.theme.horizontalSpace};
`

const Header = styled.div`
  margin-bottom: ${props => props.theme.verticalSpace};
`

const Main = () => (
  <>
    <MainContainer>
      <Sidebar />
      <FormContainer>
        <Header>
          <img src={advitoLogo} alt="advito logo" />
        </Header>
        <Form />
      </FormContainer>
    </MainContainer>
  </>
)

export default Main
