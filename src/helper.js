import history from './history'
import moment from 'moment'

export const formatDate = date => {
  return date ? moment(date).format('MMMM DD, YYYY') : ''
}

export const getToken = () => {
  if (localStorage.getItem('advito-ingestion-user')) {
    const { sessionToken } = JSON.parse(
      localStorage.getItem('advito-ingestion-user')
    )
    return sessionToken
  } else return ''
}

export const getUser = () => {
  if (localStorage.getItem('advito-ingestion-user')) {
    const user = JSON.parse(localStorage.getItem('advito-ingestion-user'))
    return { ...user }
  } else {
    return {}
  }
}

export const updateUserName = displayName => {
  if (localStorage.getItem('advito-ingestion-user')) {
    const user = JSON.parse(localStorage.getItem('advito-ingestion-user'))
    user.displayName = displayName
    localStorage.setItem('advito-ingestion-user', JSON.stringify(user))
  }
}

export const setUser = user => {
  if (localStorage.getItem('advito-ingestion-user')) {
    localStorage.removeItem('advito-ingestion-user')
  }
  localStorage.setItem('advito-ingestion-user', JSON.stringify(user))
}

export const removeUser = () => {
  localStorage.removeItem('advito-ingestion-user')
  history.push('/login')
}

// export const getApi = () => {
//   const REACT_APP_STAGE = process.env.REACT_APP_STAGE
//   return REACT_APP_STAGE === 'dev'
//     ? 'https://lfl1qiymy7.execute-api.us-east-2.amazonaws.com/dev/graphql'
//     : REACT_APP_STAGE === 'alpha'
//     ? 'https://trfrs1gzn8.execute-api.us-east-2.amazonaws.com/alpha/graphql'
//     : REACT_APP_STAGE === 'beta'
//     ? 'https://7smhjazdr2.execute-api.us-east-2.amazonaws.com/beta/graphql'
//     : REACT_APP_STAGE === 'prod'
//     ? 'https://759byqkv94.execute-api.us-east-2.amazonaws.com/prod/graphql'
//     : 'http://localhost:4000/graphql'
// }
