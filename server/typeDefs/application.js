export default `
type Application {
  id: Int
  applicationName: String
}

type Template {
  id: Int
  templateName: String
}

extend type Query {
  applicationList: [Application] @auth
  templateList(applicationId: Int): [Template] @auth
}
`
