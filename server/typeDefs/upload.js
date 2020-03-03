export default `
extend type Mutation {
  uploadFile(
    clientId: Int!
    sourceId: Int!
    dataStartDate: Date!
    dataEndDate: Date!
    fileName: String!
    rowCount: Int!
    fileSize: Int!
    base64: String!
  ): Boolean!
}
`
