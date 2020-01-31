import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import moment from 'moment-timezone'
import styled from 'styled-components'
import Time from './Time'
import advitoLogo from 'assets/advitoLogo.png'

const Container = styled.div`
  display: flex;
  align-items: flex-end;
  margin: 6em 0 3em 0;
`

const LogoContainer = styled.div`
  flex: 1;
  align-self: flex-start;
`

const TimeSupportContainer = styled.div`
  flex: 1.75;
  display: flex;
  justify-content: flex-end;
`

const TopHeader = () => {
  const location = useLocation()
  const newYork = moment().tz('America/New_York')
  const london = moment().tz('Europe/London')
  const collapse = location.pathname !== '/'
  return (
    <Container collapse={collapse}>
      <LogoContainer collapse={collapse}>
        <Link to={'/'} replace>
          <img src={advitoLogo} alt="advito logo" />
        </Link>
      </LogoContainer>
      <TimeSupportContainer>
        {!collapse && (
          <>
            <Time timeZone={newYork} zone="Washington, DC" />
            <Time timeZone={london} zone="London, UK" />
          </>
        )}
      </TimeSupportContainer>
    </Container>
  )
}

export default TopHeader
