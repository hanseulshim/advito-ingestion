import React from 'react'
import styled from 'styled-components'
import PropTypes from 'prop-types'

const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  margin-left: 1em;
  color: ${props => props.theme.black};
`

const HourZoneContainer = styled.div`
  display: flex;
  padding: 0 0.3em 0.45em 0;
  align-items: baseline;
`

const Hours = styled.div`
  font-size: 1.7em;
  padding-right: 0.4em;
`

const TimeZone = styled.div`
  font-size: 1.7em;
`

const Location = styled.div`
  padding-top: 0.45em;
  border-top: 1px solid ${props => props.theme.silver};
  font-size: 0.9em;
  text-align: center;
`

const Time = ({ timeZone, zone }) => (
  <Container>
    <HourZoneContainer>
      <Hours>{timeZone.format('h:mm')}</Hours>
      <TimeZone>{timeZone.format('A')}</TimeZone>
    </HourZoneContainer>
    <Location>{zone}</Location>
  </Container>
)

Time.propTypes = {
  timeZone: PropTypes.object.isRequired,
  zone: PropTypes.string.isRequired
}

export default Time
