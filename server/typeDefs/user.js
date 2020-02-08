export default `
type Login {
  id: Int
  displayName: String
  clientId: Int
  profilePicturePath: String
  sessionToken: String
  roleIds: [Int]
}

extend type Mutation {
  login(username: String!, password: String!): Login
  logout(sessionToken: String!): Boolean
  sendResetPasswordEmail(email: String!): String
  resetPassword(token: String!, password: String!, confirmPassword: String!): Boolean
}
`
