import React from 'react'
import styled from 'styled-components'

const Container = styled.div`
  text-align: center;
  color: ${props => props.theme.alabaster};
  font-size: 0.75em;
  margin-top: 5em;
`

const Link = styled.a`
  color: ${props => props.theme.alabaster};
  text-decoration: underline;
`

const Footer = () => (
  <Container>
    <Link href="https://www.advito.com/legal/" target="_blank">
      Terms of Service
    </Link>
    {' and '}
    <Link href="https://www.advito.com/privacy-policy/" target="_blank">
      Privacy Policy
    </Link>
  </Container>
)

export default Footer
