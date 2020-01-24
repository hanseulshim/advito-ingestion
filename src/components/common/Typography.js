import React from 'react'
import PropTypes from 'prop-types'
import styled from 'styled-components'
import { Typography } from 'antd'

const TitleStyled = styled.div`
  margin-bottom: 0.5em;
  font-weight: 400;
  color: ${props => props.theme.black};
`

const { Title: TitleComponent } = Typography

export const Header = ({ level = 1, children }) => (
  <TitleComponent level={level}>{children}</TitleComponent>
)

Header.propTypes = {
  level: PropTypes.number,
  children: PropTypes.string
}

export default Header

export const Title = ({ children, ...rest }) => (
  <TitleStyled {...rest}>{children}</TitleStyled>
)

Title.propTypes = {
  children: PropTypes.string
}
