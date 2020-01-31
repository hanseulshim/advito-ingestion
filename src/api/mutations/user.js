import gql from 'graphql-tag'

export const SEND_RESET_PASSWORD = gql`
  mutation sendResetPasswordEmail($appId: Int!, $email: String!) {
    sendResetPasswordEmail(appId: $appId, email: $email)
  }
`
export const LOGIN = gql`
  mutation login($username: String!, $password: String!) {
    login(username: $username, password: $password) {
      id
      displayName
      clientId
      profilePicturePath
      sessionToken
      roleIds
    }
  }
`
export const LOGOUT = gql`
  mutation logout($sessionToken: String!) {
    logout(sessionToken: $sessionToken)
  }
`
export const RESET_PASSWORD = gql`
  mutation resetPassword(
    $token: String!
    $password: String!
    $confirmPassword: String!
  ) {
    resetPassword(
      token: $token
      password: $password
      confirmPassword: $confirmPassword
    )
  }
`
