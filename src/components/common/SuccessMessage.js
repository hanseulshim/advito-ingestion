import React from 'react'
import PropTypes from 'prop-types'
import { Alert } from 'antd'

const SuccessMessage = ({ message = 'Success' }) => {
  return <Alert message={message} type="success" closable showIcon />
}

SuccessMessage.propTypes = {
  message: PropTypes.string.isRequired
}

export default SuccessMessage
