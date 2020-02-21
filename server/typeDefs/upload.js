export default `
extend type Mutation {
  uploadFile(fileName: String!, base64: String!): Boolean!
}
`
