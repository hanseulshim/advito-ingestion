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

type S3 {
  key: String
  url: String
}

extend type Query {
  getJob(jobId: Int!): Job @auth
  getPresignedUploadUrl(fileName: String!): S3 @auth
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
    key: String!
  ): Int @auth
}
`
