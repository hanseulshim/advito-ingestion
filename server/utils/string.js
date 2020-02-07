import crypto from 'crypto'
import { SESSION, RECOVERY } from '../constants'
import moment from 'moment'

export const saltHash = (password, salt = null) => {
  const saltHashed = salt || crypto.randomBytes(16).toString('base64')
  const passwordHashed = crypto
    .createHash('sha256')
    .update(password)
    .update(saltHashed, 'base64')
    .digest('base64')
  return {
    saltHashed,
    passwordHashed
  }
}

export const generateAccessToken = (prefix = '') =>
  prefix + crypto.randomBytes(16).toString('hex')

export const getExpirationDate = type => {
  const expirationDate = moment.utc()
  if (type === SESSION) {
    expirationDate.set('hour', expirationDate.hour() + 1)
  } else if (type === RECOVERY) {
    expirationDate.set('hour', expirationDate.hour() + 24)
  }
  return expirationDate
}

export const checkValidPassword = password => {
  const errorMessages = []
  if (password.length < 8) {
    errorMessages.push('Password must be at least 8 characters long.')
  }
  if (!/\d/g.test(password)) {
    errorMessages.push('Password must have at least one number.')
  }
  if (!/[a-z]/g.test(password)) {
    errorMessages.push('Password must have at least one lowercase letter.')
  }
  if (!/[A-Z]/g.test(password)) {
    errorMessages.push('Password must have at least one uppercase letter.')
  }
  // if (!/\.|\,|\?|\/|!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\-|\+|\=|\||\~/g.test(password)) errorMessages.push('Password must have at least one special character.') // eslint-disable-line
  if (/\s/g.test(password)) {
    errorMessages.push('Password cannot have spaces or other whitespace.')
  }
  return errorMessages
}

export const validateEmail = email =>
  /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
    email
  )
