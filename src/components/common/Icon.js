import React from 'react'
import PropTypes from 'prop-types'
import styled from 'styled-components'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

const IconStyled = styled(FontAwesomeIcon)`
  color: ${props => props.info && props.theme.treePoppy};
  border: ${props => props.info && `2px solid ${props.theme.treePoppy}`};
  padding: ${props => props.info && '0.25em .6em'};
  border-radius: ${props => props.info && '100%'};
  margin-left: ${props => props.info && '1em'};
`

const Icon = ({ icon, ...style }) => {
  return <IconStyled icon={icon} {...style} />
}

Icon.propTypes = {
  icon: PropTypes.string
}

export default Icon
