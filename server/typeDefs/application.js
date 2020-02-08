export default `
type Application {
  id: Int
  applicationName: String
}

extend type Query {
  applicationList: [Application] @auth
}
`
