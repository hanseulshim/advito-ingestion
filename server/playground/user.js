export default {
  Mutation: {
    name: 'User Mutations',
    endpoint: '',
    headers: { sessiontoken: 'MY^PR3TTYP0NY' },
    query: `
    mutation {
      login(username: "", password: "") {
        id
        displayName
        clientId
        profilePicturePath
        sessionToken
        roleIds
      }
      logout(sessionToken: "")
      sendResetPasswordEmail(email: "")
      resetPassword(token: "", password: "", confirmPassword: "")
    }`
  }
}
