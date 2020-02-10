export default `
type Application {
  id: Int
  applicationName: String
}

type Template {
  id: Int
  templateName: String
  applicationName: String
  templatePath: String
}

type Source {
  id: Int
  sourceName: String
}

extend type Query {
  applicationList: [Application] @auth
  templateList(applicationId: Int): [Template] @auth
  sourceList(templateId: Int): [Source] @auth
}
`
