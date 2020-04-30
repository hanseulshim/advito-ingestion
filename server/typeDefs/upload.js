export default `
type Job {
  id: Int
  originalFileName: String
  jobName: String
  countRows: Int
  isComplete: Boolean
  jobStatus: String
  jobNote: String
  processingStartTimestamp: String
  templateName: String
  applicationName: String
  timestamp: String
}

extend type Query {
  getJob(jobId: Int!): Job
}

extend type Mutation {
  uploadFile(
    clientId: Int!
    advitoApplicationId: Int!
    sourceId: Int!
    dataStartDate: Date!
    dataEndDate: Date!
    fileName: String!
    fileSize: Int!
    base64: String!
  ): Int
}
`
