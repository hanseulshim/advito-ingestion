export default `
extend type Mutation {
  uploadFile(
    clientId: Int!
    sourceId: Int!
    dataStartDate: Date!
    dataEndDate: Date!
    fileName: String!
    base64: String!
  ): Boolean!
}
`
